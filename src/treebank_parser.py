################################################################################
# 
#   Treebank parser -- A small application that parses a treebank and converts
#   it into a collection of head vectors.
# 
#   Copyright (C) 2021
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
#       Lluís Alemany Puig (lalemany@cs.upc.edu)
#           LARCA (Laboratory for Relational Algorithmics, Complexity and Learning)
#           CQL (Complexity and Quantitative Linguistics Lab)
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
# 
################################################################################

r"""
The main CLI of the treebank parser project.

Run with

	python3 treebank_parser.py --help

to read the usage of this script. Run with

	python3 treebank_parser.py FORMAT --help

to see the help of the corresponding treebank format FORMAT. Choose FORMAT
from the choices shown in the first 'help' command.
"""

import argparse
import logging
import sys

import treebank_formats as formats

import conllu.action_type

def add_arguments_main_parser(parser):
	r"""
	Adds the necessary arguments to the main CLI parser (not for the
	subcommands).
	"""
	parser.add_argument(
		'-i', '--inputfile',
		metavar = 'infile',
		type = str,
		required = True,
		help = 'Name of the input treebank file to be parsed.'
	)
	parser.add_argument(
		'-o', '--outputfile',
		metavar = 'outfile',
		type = str,
		required = True,
		help = 'Name of the output .heads file.'
	)
	parser.add_argument(
		'--verbose',
		default = 0,
		type = int,
		required = False,
		help =
		"Output logging messages showing the progress of the script. The higher the\
	debugging level the more messages will be displayed. \
	Default level: 0 -- display only 'error' and 'critical' messages. \
	Debugging levels: \
	* 1 -- messages from 0 plus 'warning' messages; \
	* 2 -- messages from 1 plus 'info' messages; \
	* 3 -- messages from 2 plus 'debug' messages;\
	"
	)
	parser.add_argument(
		'--laldebug',
		default = False,
		action = 'store_true',
		required = False,
		help = f"Use the debug compilation of LAL ('import laldebug as lal'). The script will run more slowly, but errors will be more likely to be caught. Default: 'import lal'."
	)

def add_arguments_CoNLLU_parser(parser):
	r"""
	Adds the necessary arguments to `parser` for CoNLL-U-formatted treebanks.
	"""
	
	# remove function words
	parser.add_argument(
		'--' + conllu.action_type.RemoveFunctionWords_str,
		default = False,
		action = 'store_true',
		required = False,
		help = conllu.action_type.RemoveFunctionWords_help_str
	)
	
	# remove punctuation marks
	parser.add_argument(
		'--' + conllu.action_type.RemovePunctuationMarks_str,
		default = False,
		action = 'store_true',
		required = False,
		help = conllu.action_type.RemovePunctuationMarks_help_str
	)
	
	# discard short sentences
	parser.add_argument(
		'--' + conllu.action_type.DiscardSentencesShorter_str,
		default = -1,
		type = int,
		metavar = "length_in_words",
		required = False,
		help = conllu.action_type.DiscardSentencesShorter_help_str
	)
	
	# discard short sentences
	parser.add_argument(
		'--' + conllu.action_type.DiscardSentencesLonger_str,
		default = -1,
		type = int,
		metavar = "length_in_words",
		required = False,
		help = conllu.action_type.DiscardSentencesLonger_help_str
	)

def create_format_subparsers(subparser):
	r"""
	Adds to the subparser the necessary subparsers 
	"""
	# create a subparser for CoNLL
	parser_CoNLLU = subparser.add_parser(
		name = formats.CoNLLU_str,
		description = formats.CoNLLU_descr_str,
		help = formats.CoNLLU_help_str
	)
	add_arguments_CoNLLU_parser(parser_CoNLLU)

# ------------------------------------------------------------------------------

def make_actions_list(args):
	r"""
	Returns a list of all the actions as integers
	"""
	
	if args.treebank_format == formats.CoNLLU_str:
		if args.RemovePunctuationMarks:
			yield conllu.action_type.RemovePunctuationMarks_str
		if args.RemoveFunctionWords:
			yield conllu.action_type.RemoveFunctionWords_str

# ******************************************************************************
# ******************************** Start CLI ***********************************
# ******************************************************************************

parser = argparse.ArgumentParser(
	description = 'Parse a treebank file and extract the sentences as head vectors.\
	The format of the treebank file is specified with a positional parameter (see\
	the list of positional arguments within "{}" below).'
)
add_arguments_main_parser(parser)

# add a subparser for the treebank format.
subparsers = parser.add_subparsers(
	help = 'Choose a format command for the input treebank file.',
	required = True,
	dest = 'treebank_format'
)

# create the necessary subparsers for every treebank format implemented
create_format_subparsers(subparsers)

# Parse arguments

args = []
if len(sys.argv) != 1:
	args = parser.parse_args()
else:
	# this is needed to avoid 'TypeError' exception
	args = parser.parse_args(["--help"])

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

print("--------------------------------------")
print(f"File to be parsed:   '{args.inputfile}'")
print(f"File to create:      '{args.outputfile}'")
print(f"Input file's format: '{args.treebank_format}'")
print(f"Verbosity level:     '{args.verbose}'")
logging.critical("Critical messages will be shown.")
logging.error("   Error messages will be shown.")
logging.warning(" Warning messages will be shown.")
logging.info("    Info messages will be shown.")
logging.debug("   Debug messages will be shown.")

# construct a list with all the actions
actions = list(make_actions_list(args))

print(f"Actions to be performed ({len(actions)}):", actions)
"""
for action in action_type.get_all_actions_int():
	meaning = action_type.get_action_meaning_str(action)
	key = action_type.get_action_key_str(action)
	print(f"    {meaning}?", key in args.actions)
"""
print("--------------------------------------")

if args.treebank_format == formats.CoNLLU_str:
	import conllu.parser
	p = conllu.parser.CoNLLU_parser(args)
	p.parse()
	p.dump_contents()
else:
	logging.error(f"Unhandled format '{args.format}'")
