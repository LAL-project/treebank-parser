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

def add_arguments_main_parser(parser):
	r"""
	Adds the necessary arguments to the main CLI parser (not for the
	subcommands).
	"""
	parser.add_argument(
		'--laldebug',
		default = False,
		action = 'store_true',
		required = False,
		help = f"Use the debug compilation of LAL ('import laldebug as lal'). The script will run more slowly, but errors will be more likely to be caught. Default: 'import lal'."
	)

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

	return parser
