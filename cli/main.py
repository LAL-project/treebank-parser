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

	python3 cli/main.py --help
	python3 cli/main.py -h

or simply

	python3 cli/main.py

to read the usage of this script. Run with

	python3 cli/main.py FORMAT --help

Usage examples:

	python3 cli/main.py -i catalan.conllu -o catalan.heads --lal CoNLLU
	python3 cli/main.py -i catalan.conllu -o catalan.heads --verbose 2 --lal CoNLLU
	python3 cli/main.py -i catalan.conllu -o catalan.heads --verbose 2 --lal CoNLLU --RemoveFunctionWords
	python3 cli/main.py -i catalan.conllu -o catalan.heads --verbose 2 --lal CoNLLU --RemoveFunctionWords --DiscardSentencesShorter 3
"""

import sys

# set up paths before actual cli's start up
import os
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()) + "/..")
del os, pathlib
# finish setting up path


import logging

import argument_parser
from treebank_parser import treebank_formats
from treebank_parser.conllu import action_type as conllu_action_type

def make_actions_list(args):
	r"""
	Returns a list of all the actions as strings for display purposes
	"""
	
	if args.treebank_format == treebank_formats.CoNLLU_key_str:
		if args.RemovePunctuationMarks:
			yield conllu_action_type.RemovePunctuationMarks_key_str
		if args.RemoveFunctionWords:
			yield conllu_action_type.RemoveFunctionWords_key_str
		if args.DiscardSentencesShorter:
			yield conllu_action_type.DiscardSentencesShorter_key_str
		if args.DiscardSentencesLonger:
			yield conllu_action_type.DiscardSentencesLonger_key_str


# create the parser object
parser = argument_parser.create_parser()

# construct list with all cli arguments
args = []
if len(sys.argv) == 1:
	# this is needed to avoid 'TypeError' exception
	args = parser.parse_args(["--help"])
if len(sys.argv) == 2:
	if sys.argv[1] == "--help" or sys.argv[1] == "-h":
		args = parser.parse_args(["--help"])
	else:
		args = parser.parse_args(sys.argv[1:])
else:
	args = parser.parse_args(sys.argv[1:])

# Run the treebank parser with the configuration encoded in 'args'.
# 'args' is the object returned by a call to the method 'parse_args'
# of an object of type argparse.ArgumentParser.

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

if not args.quiet:
	print(f"Actions to be performed ({len(actions)}):", actions)
	print("--------------------------------------")

proceed_to_run_parser = True
if args.treebank_format == treebank_formats.CoNLLU_key_str:
	from treebank_parser.conllu import parser
else:
	logging.error(f"Unhandled format '{args.format}'")
	proceed_to_run_parser = False

if proceed_to_run_parser:
	# the treebank format was handled correctly
	p = parser.parser(args)
	p.parse()
	p.dump_contents()