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
This file contains just one class `line_parser` and some tests.

The `line_parser` class parses the contents of a line in a Stanford-formatted file.
"""

import treebank_parser.output_log as tbp_logging

class line_parser:
	
	def _split_unit(self, unit):
		j = len(unit) - 1
		while j > 0 and unit[j] != '-':
			j -= 1
		return unit[0:j], unit[j+1:]
	
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
		
		# The line to be parsed. It contains a dependency
		if line_str[-1] == "\n": self.m_line_str = line_str[:-1]
		else: self.m_line_str = line_str
		
		# keep the line number where it was found
		self.m_line_number = line_number
		
		# word type, as given in the stanford dependencies file
		self.m_dependency_type = ""
		# the string that corresponds to the parent word
		self.m_parent_word = ""
		# the ID of the parent word
		self.m_parent_id = -1
		# the string that corresponds to the dependent word
		self.m_dependent_word = ""
		# the ID of the dependent word
		self.m_dependent_id = -1
	
	def parse_line(self):
		r"""
		Parses the line this object was initialized with.
		"""
		left_paren = self.m_line_str.find('(')
		right_paren = self.m_line_str.find(')')
		
		self.m_dependency_type = self.m_line_str[:left_paren]
		contents = self.m_line_str[left_paren + 1 : right_paren]
		
		parent, dependent = contents.split(',')
		
		self.m_parent_word, self.m_parent_id = self._split_unit(parent)
		self.m_dependent_word, self.m_dependent_id = self._split_unit(dependent)
		if self.m_dependent_word[0] == " ":
			self.m_dependent_word = self.m_dependent_word[1:]
		
		try:
			self.m_parent_id = int(self.m_parent_id)
			
		except BaseException as e:
			self.m_parent_id = None
			tbp_logging.critical(f"Integer conversion of parent word index failed.")
			tbp_logging.critical(f"At line {self.m_line_number}")
			tbp_logging.critical(f"At line {self.m_line_str}")
		
		try:
			self.m_dependent_id = int(self.m_dependent_id)
			
		except BaseException as e:
			self.m_dependent_id = None
			tbp_logging.critical(f"Integer conversion of dependent word index failed.")
			tbp_logging.critical(f"At line {self.m_line_number}")
			tbp_logging.critical(f"At line {self.m_line_str}")
	
	def get_dependency_type(self):
		r"""
		Returns the type of dependency.
		"""
		return self.m_dependency_type
	
	def get_parent_id(self):
		r"""
		Returns the ID of the parent word in the dependency.
		"""
		return self.m_parent_id
	
	def get_dependent_id(self):
		r"""
		Returns the ID of the dependent word in the dependency.
		"""
		return self.m_dependent_id
	
	def get_parent_word(self):
		r"""
		Returns the word of the parent word in the dependency.
		"""
		return self.m_parent_word
	
	def get_dependent_word(self):
		r"""
		Returns the word of the dependent word in the dependency.
		"""
		return self.m_dependent_word
	
	def is_punctuation_mark(self):
		r"""
		Returns whether or not the dependent word in the dependency is a
		punctuation mark. A word is a punctuation mark if its word type is
		'punct'.
		"""
		return self.get_dependency_type() == "punct"
	
	def __repr__(self):
		return f"({self.get_line_number()}) \
			type: '{self.get_dependency_type()}'\
			\t parent: '{self.get_parent_word()} ({self.get_parent_id()})\
			\t dependent: '{self.get_dependent_word()} ({self.get_dependent_id()})"
	
	def get_line(self):
		r"""
		Returns the line the parser was initialized with.
		"""
		return self.m_line_str

if __name__ == "__main__":
	# TESTS
	def print_contents(lp):
		print(lp.get_line())
		print(f"    word type:       '{lp.get_dependency_type()}'")
		print(f"    parent word:     '{lp.get_parent_word()}'")
		print(f"    parent index:    '{lp.get_parent_index()}'")
		print(f"    dependent word:  '{lp.get_dependent_word()}'")
		print(f"    dependent index: '{lp.get_dependent_index()}'")
	
	def parse_line(l, lineno, dependency_type, par_word, par_idx, dep_word, dep_idx):
		lp = line_parser(l, lineno)
		lp.parse_line()
		print_contents(lp)
		
		assert( lp.get_dependency_type() == dependency_type )
		assert( lp.get_parent_word() == par_word )
		assert( lp.get_parent_id() == par_idx )
		assert( lp.get_dependent_word() == dep_word )
		assert( lp.get_dependent_id() == dep_idx )
	
	line01 = "case(一-3, 在-1)"
	line02 = "dep(一-3, 过去-2)"
	line03 = "nmod:prep(实现-7, 一-3)"
	line04 = "mark:clf(一-3, 年-4)"
	line05 = "punct(实现-7, ，-5)"
	line06 = "nsubj(实现-7, 我们-6)"
	line07 = "root(ROOT-0, 实现-7)"
	line08 = "aux:asp(实现-7, 了-8)"
	line09 = "amod(进步-11, 了不起-9)"
	line10 = "case(了不起-9, 的-10)"
	line11 = "conj(成就-15, 进步-11)"
	line12 = "cc(成就-15, 和-12)"
	line13 = "amod(成就-15, 非凡-13)"
	line14 = "case(非凡-13, 的-14)"
	line15 = "dobj(实现-7, 成就-15)"
	line16 = "punct(实现-7, 。-16)"
	
	parse_line(line01,  1, "case", "一", 3, "在", 1)
	parse_line(line02,  2, "dep", "一", 3, "过去", 2)
	parse_line(line03,  3, "nmod:prep", "实现", 7, "一", 3)
	parse_line(line04,  4, "mark:clf", "一", 3, "年", 4)
	parse_line(line05,  5, "punct", "实现", 7, "，", 5)
	parse_line(line06,  6, "nsubj", "实现", 7, "我们", 6)
	parse_line(line07,  7, "root", "ROOT", 0, "实现", 7)
	parse_line(line08,  8, "aux:asp", "实现", 7, "了", 8)
	parse_line(line09,  9, "amod", "进步", 11, "了不起", 9)
	parse_line(line10, 10, "case", "了不起", 9, "的", 10)
	parse_line(line11, 11, "conj", "成就", 15, "进步", 11)
	parse_line(line12, 12, "cc", "成就", 15, "和", 12)
	parse_line(line13, 13, "amod", "成就", 15, "非凡", 13)
	parse_line(line14, 14, "case", "非凡", 13, "的", 14)
	parse_line(line15, 15, "dobj", "实现", 7, "成就", 15)
	parse_line(line16, 16, "punct", "实现", 7, "。", 16)
