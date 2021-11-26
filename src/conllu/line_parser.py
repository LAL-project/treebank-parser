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
This file contains just one class `line_parser` and some tests.

The `line_parser` class parses the contents of a line in a CoNLLU-formatted file.
"""

class line_parser:
	r"""
	This class implements an algorithm to parse word lines from the Conll-U format.
	The full details of this format can be found here: https://universaldependencies.org/format.html
	"""
	
	# PUBLIC
	
	def __init__(self, line_str, line_number = 0):
		r"""
		Initialises the line parser with a string object representing a word line.
		
		This method stores a hard copy of the line. If the line contains an endline
		character, the line is copied without it.
		
		Default-initializes the field-separating character with a tabulator character '\t'.
		
		Parameters
		==========
		- `line_str` : the line to be parsed as a string
		- `line_number` : the line number of the file at which this line was found
		"""
		
		assert(isinstance(line_str, str))
		
		# The line to be parsed
		if line_str[-1] == "\n": self._line_str = line_str[:-1]
		else: self._line_str = line_str
		
		# keep the line number where it was found
		self._line_number = line_number
		
		# Word index, integer starting at 1 for each new sentence; may be a range
		# for multiword tokens; may be a decimal number for empty nodes (decimal
		# numbers can be lower than 1 but must be greater than 0).
		self._ID = ""
		# Word form or punctuation symbol.
		self._FORM = ""	
		# Lemma or stem of word form.
		self._LEMMA = ""
		# Universal part-of-speech tag.
		self._UPOS = ""
		# Language-specific part-of-speech tag; underscore if not available.
		self._XPOS = ""
		# List of morphological features from the universal feature inventory
		# or from a defined language-specific extension; underscore if not available.
		self._FEATS = ""
		# Head of the current word, which is either a value of ID or zero (0).
		self._HEAD = ""
		# Universal dependency relation to the HEAD (root iff HEAD = 0) or a
		# defined language-specific subtype of one.
		self._DEPREL = ""
		# Enhanced dependency graph in the form of a list of head-deprel pairs.
		self._DEPS = ""
		# Any other annotation.
		self._MISC = ""
		
		# Default separator for fields in word lines
		self._sep = '\t'
	
	def set_separator(self, sep):
		r"""
		Sets the field separator character in word lines. The character must be
		a string (str).
		"""
		assert(isinstance(sep, str))
		self._sep = sep
	
	def parse_line(self):
		r"""
		Parses the line this object was initialized with.
		"""
		list_of_fields = self._line_str.split(self._sep)
		self._ID = list_of_fields[0]
		self._FORM = list_of_fields[1]
		self._LEMMA = list_of_fields[2]
		self._UPOS = list_of_fields[3]
		self._XPOS = list_of_fields[4]
		self._FEATS = list_of_fields[5]
		self._HEAD = list_of_fields[6]
		self._DEPREL = list_of_fields[7]
		self._DEPS = list_of_fields[8]
		self._MISC = list_of_fields[9]
	
	def get_line(self):
		r"""
		Returns the line the parser was initialized with.
		"""
		return self._line_str
	def get_ID(self):
		r"""
		Returns the contents of the ID field of the line
		"""
		return self._ID
	def get_FORM(self):
		r"""
		Returns the contents of the FORM field of the line
		"""
		return self._FORM
	def get_LEMMA(self):
		r"""
		Returns the contents of the LEMMA field of the line
		"""
		return self._LEMMA
	def get_UPOS(self):
		r"""
		Returns the contents of the UPOS field of the line
		"""
		return self._UPOS
	def get_XPOS(self):
		r"""
		Returns the contents of the XPOS field of the line
		"""
		return self._XPOS
	def get_FEATS(self):
		r"""
		Returns the contents of the FEATS field of the line
		"""
		return self._FEATS
	def get_HEAD(self):
		r"""
		Returns the contents of the HEAD field of the line
		"""
		return self._HEAD
	def get_DEPREL(self):
		r"""
		Returns the contents of the DEPREL field of the line
		"""
		return self._DEPREL
	def get_DEPS(self):
		r"""
		Returns the contents of the DEPS field of the line
		"""
		return self._DEPS
	def get_MISC(self):
		r"""
		Returns the contents of the MISC field of the line
		"""
		return self._MISC
	
	def get_line_number(self):
		r"""
		Returns the line number of this line within the line it was found at.
		"""
		return self._line_number
	
	def is_punctuation_mark(self):
		r"""
		Returns whether or not this token is a punctuation mark.
		"""
		return self.get_UPOS() == "PUNCT"
	
	def is_function_word(self):
		r"""
		Returns whether or not this token is a function word.
		
		A word is a function word if it's UPOS is one of the following values:
			ADP, AUX, CCONJ, DET, NUM, PART, PRON, SCONJ
		
		This criterion is copied from function 'isFunctionWord' from the file
			https://github.com/lluisalemanypuig/optimality-syntactic-dependency-distances/blob/master/processing_of_treebanks_and_tests/LabelledDependencyStructure.java
		"""
		return self.get_UPOS() in ["ADP","AUX","CCONJ","DET","NUM","PART","PRON","SCONJ"]
	
	def __repr__(self):
		return f"({self.get_line_number()}) \
			ID: '{self.get_ID()}'\
			\t FORM: '{self.get_FORM()}'\
			\t LEMMA: '{self.get_LEMMA()}'\
			\t UPOS: '{self.get_UPOS()}'\
			\t XPOS: '{self.get_XPOS()}'\
			\t FEATS: '{self.get_FEATS()}'\
			\t HEAD: '{self.get_HEAD()}'\
			\t DEPREL: '{self.get_DEPREL()}'\
			\t DEPS: '{self.get_DEPS()}'\
			\t MISC: '{self.get_MISC()}'"

if __name__ == "__main__":
	# TESTS
	def print_contents(lp):
		print(lp.get_line())
		print(f"    ID:     '{lp.get_ID()}'")
		print(f"    FORM:   '{lp.get_FORM()}'")
		print(f"    LEMMA:  '{lp.get_LEMMA()}'")
		print(f"    UPOS:   '{lp.get_UPOS()}'")
		print(f"    XPOS:   '{lp.get_XPOS()}'")
		print(f"    FEATS:  '{lp.get_FEATS()}'")
		print(f"    HEAD:   '{lp.get_HEAD()}'")
		print(f"    DEPREL: '{lp.get_DEPREL()}'")
		print(f"    DEPS:   '{lp.get_DEPS()}'")
		print(f"    MISC:   '{lp.get_MISC()}'")
	
	def parse_line(l, ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC):
		lp = line_parser(l)
		lp.parse_line()
		print_contents(lp)
		
		assert( lp.get_ID() == ID )
		assert( lp.get_FORM() == FORM )
		assert( lp.get_LEMMA() == LEMMA )
		assert( lp.get_UPOS() == UPOS )
		assert( lp.get_XPOS() == XPOS )
		assert( lp.get_FEATS() == FEATS )
		assert( lp.get_HEAD() == HEAD )
		assert( lp.get_DEPREL() == DEPREL )
		assert( lp.get_DEPS() == DEPS )
		assert( lp.get_MISC() == MISC )
	
	line01 = "16	Firal	Firal	PROPN	_	_	15	flat	15:flat	_"
	line02 = "17	durant	durant	ADP	sps00	_	21	case	21:case	_"
	line03 = "18	els	el	DET	da0mp0	Definite=Def|Gender=Masc|Number=Plur|PronType=Art	21	det	21:det	_"
	line04 = "19	primers	primer	ADJ	ao0mp0	Gender=Masc|Number=Plur|NumType=Ord	18	amod	18:amod	_"
	line05 = "20	cinc	cinc	NUM	dn0cp0	Number=Plur|NumType=Card	18	nummod	18:nummod	_"
	line06 = "21	mesos	mes	NOUN	ncmp000	Gender=Masc|Number=Plur	12	nmod	12:nmod	_"
	line07 = "22	de	de	ADP	sps00	_	24	case	24:case	_"
	line08 = "23	l'	el	DET	da0cs0	Definite=Def|Number=Sing|PronType=Art	24	det	24:det	SpaceAfter=No"
	line09 = "24	any	any	NOUN	ncms000	Gender=Masc|Number=Sing	21	nmod	21:nmod	SpaceAfter=No"
	line10 = "25	.	.	PUNCT	fp	PunctType=Peri	7	punct	7:punct	_"
	
	parse_line(line01, "16", "Firal", "Firal", "PROPN", "_", "_", "15", "flat", "15:flat", "_")
	parse_line(line02, "17", "durant", "durant", "ADP", "sps00", "_", "21", "case", "21:case", "_")
	parse_line(line03, "18", "els", "el", "DET", "da0mp0", "Definite=Def|Gender=Masc|Number=Plur|PronType=Art", "21", "det", "21:det", "_")
	parse_line(line04, "19", "primers", "primer", "ADJ", "ao0mp0", "Gender=Masc|Number=Plur|NumType=Ord", "18", "amod", "18:amod", "_")
	parse_line(line05, "20", "cinc", "cinc", "NUM", "dn0cp0", "Number=Plur|NumType=Card", "18", "nummod", "18:nummod", "_")
	parse_line(line06, "21", "mesos", "mes", "NOUN", "ncmp000", "Gender=Masc|Number=Plur", "12", "nmod", "12:nmod", "_")
	parse_line(line07, "22", "de", "de", "ADP", "sps00", "_", "24", "case", "24:case", "_")
	parse_line(line08, "23", "l'", "el", "DET", "da0cs0", "Definite=Def|Number=Sing|PronType=Art", "24", "det", "24:det", "SpaceAfter=No")
	parse_line(line09, "24", "any", "any", "NOUN", "ncms000", "Gender=Masc|Number=Sing", "21", "nmod", "21:nmod", "SpaceAfter=No")
	parse_line(line10, "25", ".", ".", "PUNCT", "fp", "PunctType=Peri", "7", "punct", "7:punct", "_")
