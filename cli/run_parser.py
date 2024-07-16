################################################################################
#
#   Treebank parser -- A small application that parses a treebank and converts
#   it into a collection of head vectors.
#
#   Copyright (C) 2021 - 2024
#
#   This file is part of Linear Arrangement Library. To see the full code
#   visit the webpage:
#       https://github.com/LAL-project/treebank-parser.git
#
#   treebank-parser is free software: you can redistribute it
#   and/or modify it under the terms of the GNU Affero General Public License
#   as published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   treebank-parser is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with Linear Arrangement Library.  If not, see <http://www.gnu.org/licenses/>.
#
#   Contact:
#
#       Lluís Alemany Puig (lluis.alemany.puig@upc.edu)
#           LQMC (Lingüística Quantitativa, Matemàtica i Computacional)
#           Webpage: https://lqmc.upc.edu/
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
#
################################################################################

import logging

from treebank_parser import treebank_formats, output_log, treebank_collection_parser
from treebank_parser.conllu import action_type as conllu_action_type
from treebank_parser.stanford import action_type as stanford_action_type
from treebank_parser.head_vector import action_type as head_vector_action_type

def make_actions_list(args):
	r"""
	Returns a list of all the actions as strings for display purposes
	"""
	
	if args.treebank_format == treebank_formats.CoNLLU_key_str:
		if args.RemovePunctuationMarks:
			yield conllu_action_type.RemovePunctuationMarks_key_str
		if args.RemoveFunctionWords:
			yield conllu_action_type.RemoveFunctionWords_key_str
		if args.DiscardSentencesShorter != -1:
			yield conllu_action_type.DiscardSentencesShorter_key_str
		if args.DiscardSentencesLonger != -1:
			yield conllu_action_type.DiscardSentencesLonger_key_str
		if args.ChunkSyntacticDependencyTree != None:
			yield f"{conllu_action_type.ChunkTree_key_str} -- {args.ChunkSyntacticDependencyTree}"
	
	elif args.treebank_format == treebank_formats.Stanford_key_str:
		if args.RemovePunctuationMarks:
			yield stanford_action_type.RemovePunctuationMarks_key_str
		if args.DiscardSentencesShorter != -1:
			yield stanford_action_type.DiscardSentencesShorter_key_str
		if args.DiscardSentencesLonger != -1:
			yield stanford_action_type.DiscardSentencesLonger_key_str
		if args.ChunkSyntacticDependencyTree != None:
			yield f"{stanford_action_type.ChunkTree_key_str} -- {args.ChunkSyntacticDependencyTree}"

	elif args.treebank_format == treebank_formats.head_vector_key_str:
		if args.DiscardSentencesShorter != -1:
			yield head_vector_action_type.DiscardSentencesShorter_key_str
		if args.DiscardSentencesLonger != -1:
			yield head_vector_action_type.DiscardSentencesLonger_key_str
		if args.ChunkSyntacticDependencyTree != None:
			yield f"{head_vector_action_type.ChunkTree_key_str} -- {args.ChunkSyntacticDependencyTree}"


def configure_logging(args):
	# configure logging
	logging.basicConfig(
		level = logging.DEBUG,
		format = "[%(levelname)s] %(asctime)s : %(message)s",
		datefmt = '%Y-%m-%d %H:%M:%S'
	)

	if args.verbose != None:
		if args.verbose == 0:
			logging.disable(logging.WARNING)
		elif args.verbose == 1:
			logging.disable(logging.INFO)
		elif args.verbose == 2:
			logging.disable(logging.DEBUG)
		else:
			logging.disable(logging.NOTSET)

	# Print some debugging information regarding parameters
	if not args.quiet:
		print("--------------------------------------")

		if args.input_treebank_file is not None:
			print(f"Treebank file to be parsed: '{args.input_treebank_file}'")
			print(f"Head vector file to create: '{args.output}'")
			print(f"Keep consistency among sentences? {args.consistency_in_sentences}")
		else:
			print(f"Treebank collection to be parsed: '{args.input_treebank_collection}'")
			print(f"Head vector colleciton file to create: '{args.output}'")

		print(f"Input file's format: '{args.treebank_format}'")
		print(f"Verbosity level: '{args.verbose}'")
		logging.critical("Critical messages will be shown.")
		logging.error("Error messages will be shown.")
		logging.warning("Warning messages will be shown.")
		logging.info("Info messages will be shown.")
		logging.debug("Debug messages will be shown.")
	
	output_log.info = logging.info
	output_log.debug = logging.debug
	output_log.warning = logging.warning
	output_log.error = logging.error
	output_log.critical = logging.critical

def run(args, lal_module):
	# Run the treebank parser with the configuration encoded in 'args'.
	# 'args' is the object returned by a call to the method 'parse_args'
	# of an object of type argparse.ArgumentParser.
	
	# construct a list with all the actions
	actions = list(make_actions_list(args))

	if not args.quiet:
		print(f"Actions to be performed ({len(actions)}):", actions)
		print("--------------------------------------")

	proceed_to_run_parser = True
	if args.treebank_format == treebank_formats.CoNLLU_key_str:
		from treebank_parser.conllu import parser
	elif args.treebank_format == treebank_formats.head_vector_key_str:
		from treebank_parser.head_vector import parser
	elif args.treebank_format == treebank_formats.Stanford_key_str:
		from treebank_parser.stanford import parser
	else:
		logging.error(f"Unhandled format '{args.treebank_format}'")
		proceed_to_run_parser = False

	if not proceed_to_run_parser: return

	if args.input_treebank_file is not None:
		p = parser.parser(args.input_treebank_file, args.output, args, lal_module)
		p.parse()
		p.dump_contents()

	if args.input_treebank_collection is not None:
		treebank_collection_parser.parse_treebank_collection(
			parser.parser,
			args.input_treebank_collection,
			args.output,
			args,
			lal_module
		)
