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
Parser of CoNLLU-formatted files.

This module contains a single class `CoNLLU_parser`.
"""

import logging

import action_type
from conllu.line_parser import line_parser
import conllu.line_type as line_type

class CoNLLU_parser:
	r"""
	This class implements a parsing algorithm for CoNLLU-formatted files. It uses
	the modules `conllu.line_parser` and `conllu.line_type` to easily parse the
	file.
	
	This class basically implements the algorithms to convert each syntactic
	dependency tree into an object of type `lal.graphs.rooted_tree` and convert
	each tree into a head vector.
	
	This class also applies some preprocessing specified by the user via arguments
	(see main CLI).
	"""
	
	def _has_action(self, action):
		r"""
		Is the given action `action` in the arguments?
		"""
		return action_type.get_action_key_str(action) in self._args.actions
	
	def _finish_reading_tree(self):
		r"""
		This function is used to convert the contents of the member 'current_tree'
		into an object of type lal.graphs.rooted_tree.
		
		This function then applies the actions passed as parameters (removal of punctuation
		marks, function words, ...).
		
		Finally, the function converts whatever is left from applying the actions into
		a head vector, which is then stored in the variable 'head_vector_collection'.
		"""
		
		# retrieve the head vector
		head_vector = []
		for key,word in self._current_tree.items():
			head_int = int(word.get_HEAD())
			head_vector.append(head_int)
		
		# make the lal.graphs.rooted_tree() object
		rt = self._lal.graphs.from_head_vector_to_rooted_tree(head_vector)
		
		# -- apply actions --
		
		num_removed = 0
		for idx, word in self._current_tree.items():
			for f in self._action_functions:
				# word does not meet criterion
				if not f(word): continue
				
				# calculate the (actual) id of the word to be removed
				word_id = int(word.get_ID()) - num_removed - 1
				
				logging.debug(f"Remove {word_id}. Original ID: {word.get_ID()}")
				logging.debug(f"Tree has root? {rt.has_root()}.")
				
				if rt.has_root() and rt.get_root() == word_id:
					logging.error(f"Removing the root may lead to critical errors.")
					logging.error(f"    It is strongly suggested to rerun the program with '--laldebug'.")
				
				logging.debug(f"Tree has {rt.get_num_nodes()}. Word to be removed: {word_id=}")
				if word_id >= rt.get_num_nodes():
					logging.critical(f"Trying to remove a non-existent vertex. The program should crash now.")
					logging.critical(f"    Please, rerun the program with '--laldebug --verbose 3' for further debugging.")
				
				# remove the node
				rt.remove_node(word_id, True)
				
				# accumulate amount of removed to calculate future ids
				num_removed += 1
		
		# -- store the head vector --
		
		if rt.get_num_nodes() > 0:
			if not rt.is_rooted_tree():
				logging.critical(f"Trying to produce a head vector of a graph that:")
				logging.critical(f"    is a tree?  {rt.is_tree()}")
				logging.critical(f"    has a root? {rt.has_root()}")
			
			hv = str(rt.get_head_vector()).replace('(', '').replace(')', '').replace(',', '')
			self._head_vector_collection.append(hv)
			
			self._current_tree.clear()
			self._reading_tree = False
	
	def __init__(self, args):
		r"""
		Initialises the CoNLL-U parser with the arguments passed as parameter.
		"""
		self._current_tree = {}
		self._reading_tree = False
		self._head_vector_collection = []
		self._args = args
		self._tree_starts_at = 0 # the file line number where the current tree starts
		
		# utilities for logging
		self._donotknow_msg = "Do not know how to process this. This line will be ignored."
		
		# import correct build of LAL
		if self._args.laldebug:
			import laldebug as lal
			self._lal = lal
		else:
			import lal
			self._lal = lal
		
		# make lambdas for all actions passed as parameter
		self._action_functions = []
		
		# Remove punctuation marks
		if self._has_action(action_type.RemovePunctuationMarks):
			self._action_functions.append( lambda w: w.is_punctuation_mark() )
		
		# Remove function words
		if self._has_action(action_type.RemoveFunctionWords):
			self._action_functions.append( lambda w: w.is_function_word() )
	
	def parse(self):
		r"""
		Open the input file and read its contents.
		The sentences in CoNLL-U format are stored in the member variable
		'head_vector_collection' in the form of head vectors.
		"""
		
		linenumber = 1
		with open(self._args.inputfile, 'r') as f:
			for line in f:
				type_of_line = line_type.classify(line)
				
				if type_of_line == line_type.comment:
					# do nothing...
					pass
				
				elif type_of_line == line_type.blank:
					if self._reading_tree:
						# a blank line after having started a tree
						# indicates the end of the tree
						self._finish_reading_tree()
				
				elif type_of_line == line_type.word:
					# this line has actual information about the tree.
					if not self._reading_tree:
						self._reading_tree = True
						logging.debug(f"Start reading tree at line {linenumber}")
					
					lp = line_parser(line, linenumber)
					lp.parse_line()
					
					ignore = False
					
					# check if line is to be ignored or not
					if '-' in lp.get_ID():
						ignore = True
					elif '.' in lp.get_ID():
						ignore = True
					
					if not ignore:
						lineid = lp.get_ID()
						self._current_tree[lineid] = lp
				
				linenumber += 1
			
			# Finished reading file.
			# If there was some tree being read, store it.
			if self._reading_tree: self._finish_reading_tree()
	
	def dump_contents(self):
		r"""
		Dump all the head vectors to the output file.
		"""
		
		with open(self._args.outputfile, 'w') as f:
			for hv in self._head_vector_collection:
				f.write(hv + '\n')
