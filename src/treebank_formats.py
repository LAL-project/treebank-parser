######################################################################
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
######################################################################

r"""
The different formats that can be parsed.

Formats
=======
- `CoNLLU`: CoNLL-U format (see https://universaldependencies.org/format.html)
"""

CoNLLU = 0

format_key_str = {
	CoNLLU : "CoNLLU",
}

aciton_meaning_str = {
	CoNLLU : "CoNLL-U",
}

def get_all_formats_int():
	r"""
	Return all formats as integers.
	"""
	return [CoNLLU]

#--------------------------------------------------------------------------
def get_format_key_str(a):
	r"""
	Return an format's key strings.
	"""
	return format_key_str[a]
def get_all_formats_key_str():
	r"""
	Return all formats as key strings.
	"""
	return format_key_str.values()

#--------------------------------------------------------------------------
def get_format_meaning_str(a):
	r"""
	Return an format's meaning strings.
	"""
	return aciton_meaning_str[a]
def get_all_formats_meaning_str():
	r"""
	Return all formats as meaning strings.
	"""
	return aciton_meaning_str.values()

if __name__ == "__main__":
	# TESTS
	assert( len(get_all_formats_int()) == len(get_all_formats_key_str()) )
	assert( len(get_all_formats_key_str()) == len(get_all_formats_meaning_str()) )
