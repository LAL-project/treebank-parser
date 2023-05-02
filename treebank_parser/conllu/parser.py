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
Parser of CoNLLU-formatted files.

This module contains a single class `CoNLLU_parser`.
"""

import time

from treebank_parser.conllu import line_parser
from treebank_parser.conllu import line_type
from treebank_parser.conllu import action_type
import treebank_parser.output_log as tbp_logging

class parser:
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
	
	def _should_discard_tree(self, rt):
		r"""
		Returns whether or not a rooted tree `rt` should be discarded according
		to the functions in `self._sentence_action_functions`.
		
		Parameters
		==========
		- `rt`: rooted tree.
		"""
		if rt.get_num_nodes() == 0: return True
		for f in self._sentence_action_functions:
			if f(rt): return True
		return False
	
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
		tbp_logging.debug(f"make a rooted tree from the head vector {head_vector=}")
		rt = self.LAL_module.graphs.from_head_vector_to_rooted_tree(head_vector)
		
		tbp_logging.debug(f"the graph has {rt.get_num_nodes()} nodes")
		tbp_logging.debug(f"the graph has {rt.get_num_edges()} edges")
		tbp_logging.debug(f"Is the graph a rooted tree? {rt.is_rooted_tree()}")
		
		# -- apply actions --
		
		num_removed = 0
		for idx, word in self._current_tree.items():
			for f in self._word_action_functions:
				# word does not meet criterion for removal
				if not f(word): continue
				
				# calculate the (actual) id of the word to be removed
				word_id = int(word.get_ID()) - num_removed - 1
				
				tbp_logging.debug(f"Remove {word_id}. Original ID: {word.get_ID()}")
				tbp_logging.debug(f"Tree has root? {rt.has_root()}.")
				
				if rt.has_root() and rt.get_root() == word_id:
					tbp_logging.warning(f"Removing the root of the tree.")
					tbp_logging.warning(f"This will make the structure become a forest.")
				
				tbp_logging.debug(f"Tree has {rt.get_num_nodes()} nodes. Word to be removed: {word_id=}")
				if word_id >= rt.get_num_nodes():
					tbp_logging.critical(f"Trying to remove a non-existent vertex. The program should crash now.")
					tbp_logging.critical(f"    Please, rerun the program with '--laldebug --verbose 3' for further debugging.")
				
				# remove the node
				rt.remove_node(word_id, True)
				
				# accumulate amount of removed to calculate future ids
				num_removed += 1
				
				# no need to evaluate more functions
				break
		
		tbp_logging.debug("All actions have been applied")
		
		# -- store the head vector --
		
		if not rt.is_rooted_tree():
			# 'rt' is not a valid rooted tree. We do not know how to store this
			# as a head vector.
			tbp_logging.warning(f"This graph is not a rooted tree. Ignored.")
		
		elif not self._should_discard_tree(rt):
			# The rooted tree should not be discarded. Its number of vertices
			# (words) is 1 or more and is not too short, nor too long.
			
			# Store the head vector of this rooted tree
			hv = str(rt.get_head_vector()).replace('(', '').replace(')', '').replace(',', '')
			self._head_vector_collection.append(hv)
		
		# it is ¡very! important to reset the state of the parser:
		# clear the current tree's contents and finish reading the tree.
		self._current_tree.clear()
		self._reading_tree = False
		
		rt.clear()
	
	def __init__(self, args, lal_module):
		r"""
		Initialises the CoNLL-U parser with the arguments passed as parameter.
		"""
		self._current_tree = {}
		self._reading_tree = False
		self._head_vector_collection = []
		self._tree_starts_at = 0 # the file line number where the current tree starts
		self._input_file = args.inputfile
		self._output_file = args.outputfile
		
		# utilities for logging
		self._donotknow_msg = "Do not know how to process this. This line will be ignored."
		
		# keep LAL module
		self.LAL_module = lal_module
		
		# make lambdas for all actions applied on a word
		self._word_action_functions = []
		
		# Remove punctuation marks
		if args.RemovePunctuationMarks:
			self._word_action_functions.append( lambda w: w.is_punctuation_mark() )
		# Remove function words
		if args.RemoveFunctionWords:
			self._word_action_functions.append( lambda w: w.is_function_word() )
		
		# make lambdas for all actions applied on a sentence
		self._sentence_action_functions = []
		
		# Discard short sentences
		if args.DiscardSentencesShorter != -1:
			self._sentence_action_functions.append(
				lambda rt: rt.get_num_nodes() <= args.DiscardSentencesShorter
			)
		# Discard long sentences
		if args.DiscardSentencesLonger != -1:
			self._sentence_action_functions.append(
				lambda rt: rt.get_num_nodes() >= args.DiscardSentencesLonger
			)
	
	def parse(self):
		r"""
		Open the input file and read its contents.
		The sentences in CoNLL-U format are stored in the member variable
		'head_vector_collection' in the form of head vectors.
		"""
		
		linenumber = 1
		with open(self._input_file, 'r') as f:
			tbp_logging.info(f"Input file {self._input_file} has been opened correctly.")
			
			begin = time.perf_counter()
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
						tbp_logging.debug(f"Start reading tree at line {linenumber}")
					
					lp = line_parser.line_parser(line, linenumber)
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
			end = time.perf_counter()
			
			tbp_logging.info(f"Finished parsing the whole input file {self._input_file}.")
			tbp_logging.info(f"    In {end - begin:.3f} s.")
	
	def dump_contents(self):
		r"""
		Dump all the head vectors to the output file.
		"""
		
		with open(self._output_file, 'w') as f:
			tbp_logging.info(f"Output file {self._output_file} has been opened correctly.")
			
			begin = time.perf_counter()
			for hv in self._head_vector_collection:
				f.write(hv + '\n')
			end = time.perf_counter()
			
			tbp_logging.info(f"Finished writing the head vectors into {self._output_file}.")
			tbp_logging.info(f"    In {end - begin:.3f} s.")
