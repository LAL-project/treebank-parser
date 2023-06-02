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
This script contains functions that create an argument parser object.

This object is to be used by the main command line interface.
"""

import argparse

from treebank_parser import treebank_formats as formats
from treebank_parser.conllu import action_type as conllu_action_type

from cli.argument_parser_CoNLLU import add_arguments_CoNLLU_parser
from cli.argument_parser_head_vector import add_arguments_head_vector_parser

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
		'--lal',
		default = False,
		action = 'store_true',
		required = False,
		help = f"Use the debug compilation of LAL ('import lal'). The script will run more slowly, but errors will be more likely to be caught. Default: 'import laloptimized as lal'."
	)
	parser.add_argument(
		'--quiet',
		default = False,
		action = 'store_true',
		required = False,
		help = f"Disable non-logging messages."
	)

def create_format_subparsers(subparser):
	r"""
	Adds to the subparser the necessary subparsers 
	"""
	# create a subparser for CoNLL
	parser_CoNLLU = subparser.add_parser(
		name = formats.CoNLLU_key_str,
		description = formats.CoNLLU_descr_str,
		help = formats.CoNLLU_help_str
	)
	add_arguments_CoNLLU_parser(parser_CoNLLU)
	
	# create a subparser for head vector
	parser_head_vector = subparser.add_parser(
		name = formats.head_vector_key_str,
		description = formats.head_vector_descr_str,
		help = formats.head_vector_help_str
	)
	add_arguments_head_vector_parser(parser_head_vector)

# ------------------------------------------------------------------------------

def create_parser():
	r"""
	Create an object of type argparse.ArgumentParser.
	"""

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

	return parser
