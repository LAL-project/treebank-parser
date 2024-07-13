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
This is a helper module to make code more readable when classifying lines.

This module only has one method that returns the type of line among three different types:
- blank line: `Blank` and `Blank_str`
- comment line: `Comment` and `Comment_str`
- token lines: `Token` and `Token_str`

See https://universaldependencies.org/format.html for more details on the type
of lines that a CoNLL-formatted text can have.
"""

Blank = 0
Comment = 1
Token = 2

Blank_str = "Blank"
Comment_str = "Comment"
Token_str = "Word"

def type_as_parameter(t):
	"""
	Converts a type of line to a string (`str`) object.
	
	Parameters
	==========
	- t : One of `Blank`, `Comment`, `Word`.
	
	Returns
	=======
	Returns a string object representing each line type:
		
	- `Blank`   : `Blank_str`
	- `Comment` : `Comment_str`
	- `Token`   : `Token_str`
	"""

	if t == Blank: return Blank_str
	if t == Comment: return Comment_str
	if t == Token: return Token_str
	assert(False)

def classify(line: str):
	"""
	Classifies the line passed as parameter.
	
	Parameters
	==========
	- line : the line to be classified. Must be a string (`str`) type.
	
	Returns
	=======
	Returns the classification of the line as either:
		
	- Blank      : for blank lines
	- Comment    : for comment lines
	- Token      : for token lines
	"""
	
	assert(isinstance(line, str))
	
	# corner case
	if line == "": return Blank

	# detect comment lines and simplify finding blank lines
	if line[0] == "#": return Comment

	# detect complex blank lines (spaces + tabs combined)
	if line == "\n": return Blank
	if all(map(lambda x: x == " " or x == "\t", line[:-1])): return Blank

	return Token

def classify_str(line: str):
	"""
	Converts a line type to a string.
	
	Parameters
	==========
	- line : the line to be classified. Must be a string (`str`) type.
	
	Returns
	=======
	Returns a string "Blank", "Comment", or "Token" dependening on the type.
	The type must be valid.
	"""
	t = classify(line)
	if t == Blank: return Blank_str
	if t == Comment: return Comment_str
	if t == Token: return Token_str
	assert(False)

if __name__ == "__main__":
	# TESTS
	line_sample = "# asdf"
	assert( classify(line_sample) == Comment )
	assert( classify_str(line_sample) == Comment_str )

	line_sample = ""
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	line_sample = "    "
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	line_sample = "    \n"
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	line_sample = "\t\t\t\n"
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	line_sample = " \t \t \t \n"
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	line_sample = "\t"
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	line_sample = "\n"
	assert( classify(line_sample) == Blank )
	assert( classify_str(line_sample) == Blank_str )

	# an actual line taken from the UD treebank for Catalan
	line_sample = "2	Privada	Privada	PROPN	_	_	1	flat	1:flat	_"
	assert( classify(line_sample) == Token )
	assert( classify_str(line_sample) == Token_str )
