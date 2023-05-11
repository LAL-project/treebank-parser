######################################################################
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
######################################################################

r"""
The different formats that can be parsed.

Formats
=======
- `CoNLL-U`: CoNLL-U format (see https://universaldependencies.org/format.html)
- `Head Vector`: head vector format (see https://cqllab.upc.edu/lal/data-formats/)
"""

CoNLLU = 0
head_vector = 1

# -------------------------------------------------------------------------

format_key_str = {
	CoNLLU: "CoNLL-U",
	head_vector: "Head-Vector",
}

CoNLLU_key_str = format_key_str[CoNLLU]
head_vector_key_str = format_key_str[head_vector]

# -------------------------------------------------------------------------

format_text_str = {
    CoNLLU: "CoNLL-U",
    head_vector: "Head-Vector",
}

CoNLLU_text_str = format_text_str[CoNLLU]
head_vector_text_str = format_text_str[head_vector]

# -------------------------------------------------------------------------

format_description_str = {
	CoNLLU:
		"The parser of a CoNLL-U-formatted file. This command has special\
		mandatory and optional parameters. These are listed below.",
	head_vector:
		"The parser of a head vector-formatted file. This command has special\
		mandatory and optional parameters. These are listed below.",
}

CoNLLU_descr_str = format_description_str[CoNLLU]
head_vector_descr_str = format_description_str[head_vector]

# -------------------------------------------------------------------------

format_help_str = {
	CoNLLU:
		"Command to parse a CoNLL-U-formatted file. For further information\
		on this format's detailed specification, see https://universaldependencies.org/format.html.",
	head_vector:
		"Command to parse a head vector-formatted file. For further information\
		on this format's detailed specification, see https://cqllab.upc.edu/lal/data-formats/.",
}

CoNLLU_help_str = format_help_str[CoNLLU]
head_vector_help_str = format_help_str[head_vector]

# -------------------------------------------------------------------------

if __name__ == "__main__":
	# TESTS
	print("Testing...")
	assert( len(format_key_str) == len(format_description_str) )
	assert( len(format_description_str) == len(format_help_str) )
