######################################################################
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
#       Lluís Alemany Puig (lalemany@cs.upc.edu)
#           LARCA (Laboratory for Relational Algorithmics, Complexity and Learning)
#           CQL (Complexity and Quantitative Linguistics Lab)
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
# 
######################################################################

r"""
This file defines basic functions for printing
- information messages,
- debug messages,
- warning messages,
- error messages, and
- critical messages.

These functions are stored in variables which are then used by the treebank
parser library. These can be overridden by users of the treebank parser library.
"""

def _print_info(s):
	print(f"INFO : {s}")

def _print_debug(s):
	print(f"DEBUG : {s}")

def _print_warning(s):
	print(f"WARNING : {s}")

def _print_error(s):
	print(f"ERROR : {s}")

def _print_critical(s):
	print(f"CRITICAL : {s}")

info = _print_info
debug = _print_debug
warning = _print_warning
error = _print_error
critical = _print_critical
