################################################################################
# 
#   Treebank parser -- A small application that parses a treebank and converts
#   it into a collection of head vectors.
# 
#   Copyright (C) 2021-2023
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
	python3 cli/main.py -i catalan.conllu -o catalan.heads --verbose 2 CoNLLU --RemoveFunctionWords
	python3 cli/main.py -i catalan.conllu -o catalan.heads --verbose 2 CoNLLU --RemoveFunctionWords --DiscardSentencesShorter 3
"""

import sys
import logging

# set up paths before actual cli's start up
import os
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()) + "/..")
del os, pathlib
# finish setting up path

import argument_parser

from treebank_parser.conllu import action_type as conllu_action_type

from cli import run_parser

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

# configure logging
run_parser.configure_logging(args)

if args.lal:
	import lal
else:
	import laloptimized as lal

from treebank_parser import version_lal
r = version_lal.is_version_of_LAL_correct(lal)
if not r[0]:
	logging.critical(r[1])
	exit(1)

run_parser.run(args, lal)
