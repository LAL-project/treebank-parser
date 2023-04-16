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
This is a helper module to make code more readable when classifying lines.

This module only has one method that returns the type of line among three different types:
- blank line
- comment line	
- word lines

See https://universaldependencies.org/format.html for more details on the type
of lines that a CoNLL-formatted text can have.
"""

blank = 0
comment = 1
word = 2

def classify(line):
	"""
	Classifies the line passed as parameter.
	
	Parameters
	==========
	- line : the line to be classified. Must be a string type.
	
	Returns
	=======
	Returns the classification of the line as either:
		
	- blank   : for blank lines
	- comment : for comment lines
	- word    : for word lines
	"""
        
	assert(isinstance(line, str))
	
	if line == "\n" or line == "": return blank
	if line[0] == "#": return comment
	return word

def type_as_string(t):
	"""
	Converts a line type to a string.
	
	Parameters
	==========
	- `t` : type of line. One of line_type.blank, line_type.comment, line_type.word.
	
	Returns
	=======
	Returns a string "blank", "comment", "word" dependening on the type.
	The type must be valid.
	"""
	if t == blank: return "blank"
	if t == comment: return "comment"
	if t == word: return "word"
	assert(False)

if __name__ == "__main__":
	# TESTS
	line_sample1 = "# asdf"
	line_sample2 = ""
	line_sample3 = "\n"
	# an actual line taken from the UD treebank for Catalan
	line_sample4 = "2	Privada	Privada	PROPN	_	_	1	flat	1:flat	_"
	
	assert( classify(line_sample1) == comment )
	assert( classify(line_sample2) == blank )
	assert( classify(line_sample3) == blank )
	assert( classify(line_sample4) == word )
