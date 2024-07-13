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
#       Lluís Alemany Puig (lluis.alemany.puig@upc.edu)
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

# -------------------------------------------------------------------------

r"""
The integer value for 'CoNLL-U' format
"""
CoNLLU = 0
r"""
The integer value for 'head vector' format
"""
head_vector = 1
r"""
The integer value for 'Stanford' format
"""
Stanford = 2

# -------------------------------------------------------------------------

r"""
The string used to represent each treebank format in the CLI.
"""
treebankformat_key_str = {
	CoNLLU: "CoNLL-U",
	head_vector: "Head-Vector",
	Stanford: "Stanford",
}

CoNLLU_key_str = treebankformat_key_str[CoNLLU]
head_vector_key_str = treebankformat_key_str[head_vector]
Stanford_key_str = treebankformat_key_str[Stanford]

# -------------------------------------------------------------------------

r"""
The string used to represent each treebank format in the GUI.
"""
treebankformat_text_str = {
    CoNLLU: "CoNLL-U",
    head_vector: "Head Vector",
    Stanford: "Stanford",
}

CoNLLU_text_str = treebankformat_text_str[CoNLLU]
head_vector_text_str = treebankformat_text_str[head_vector]
Stanford_text_str = treebankformat_text_str[Stanford]

# -------------------------------------------------------------------------

r"""
The description of what each treebank format is. This is used by the CLI and the GUI.
"""
treebankformat_description_str = {
	CoNLLU:
		"The parser of a CoNLL-U-formatted file. This command has special\
		mandatory and optional parameters. These are listed below.",
	head_vector:
		"The parser of a head vector-formatted file. This command has special\
		mandatory and optional parameters. These are listed below.",
	Stanford:
		"The parser of a Stanford-formatted file. This command has special\
		mandatory and optional parameters. These are listed below.",
}

CoNLLU_descr_str = treebankformat_description_str[CoNLLU]
head_vector_descr_str = treebankformat_description_str[head_vector]
Stanford_descr_str = treebankformat_description_str[Stanford]

# -------------------------------------------------------------------------

r"""
Used in the CLI to briefly describe what each treebank format is.
"""
treebankformat_help_str = {
	CoNLLU:
		"Command to parse a CoNLL-U-formatted file. For further information\
		on this format's detailed specification, see https://universaldependencies.org/format.html.",
	head_vector:
		"Command to parse a head vector-formatted file. For further information\
		on this format's detailed specification, see https://cqllab.upc.edu/lal/data-formats/.",
	Stanford:
		"Command to parse a Stanford-formatted file. For further information\
		on this format's detailed specification, see https://nlp.stanford.edu/software/stanford-dependencies.html.",
}

CoNLLU_help_str = treebankformat_help_str[CoNLLU]
head_vector_help_str = treebankformat_help_str[head_vector]
Stanford_help_str = treebankformat_help_str[Stanford]

# -------------------------------------------------------------------------

if __name__ == "__main__":
	# TESTS
	print("Testing...")
	assert( len(treebankformat_key_str) == len(treebankformat_description_str) )
	assert( len(treebankformat_description_str) == len(treebankformat_help_str) )
