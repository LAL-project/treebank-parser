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
Parser of CoNLLU-formatted files.

This module contains a single class `parser`.
"""

import time

from treebank_parser.conllu import line_parser
from treebank_parser.conllu import line_type
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
		to the functions in `self.m_sentence_discard_functions`.
		
		Parameters
		==========
		- `rt`: rooted tree.
		"""
		if rt.get_num_nodes() == 0: return True
		return any(map(lambda f: f(rt), self.m_sentence_discard_functions))
	
	def _build_tree(self):
		r"""
		This function is used to convert the contents of the member 'm_current_tree'
		into an object of type `lal.graphs.rooted_tree`.
		"""
		
		# retrieve the head vector from the lines while ensuring
		# that all heads are numerical
		head_vector = []
		for token in self.m_current_tree_tokens:
			try:
				head_int = int(token.get_HEAD())
				
			except Exception as e:
				tbp_logging.error(f"At line {token.get_line_number()}")
				tbp_logging.error(f"    Head: '{token.get_HEAD()}'")
				tbp_logging.error(f"    Within line: '{token.get_line()}'")
				tbp_logging.error(f"    {self.m_donotknow_msg}")
				tbp_logging.error(f"    Exception: '{e}'")
				return
			
			head_vector.append(head_int)
		
		# make sure there aren't errors in the head vector (do this with LAL)
		tbp_logging.info("Checking mistakes in head vector...")
		err_list = self.LAL_module.io.check_correctness_head_vector(head_vector)
		if len(err_list) > 0:
			
			tbp_logging.error(f"There were errors within head vector '{head_vector}'")
			for err in err_list:
				tbp_logging.error(f"    {err}")
				
			tbp_logging.error(self.m_donotknow_msg)
			return
		
		# make the lal.graphs.rooted_tree() object
		tbp_logging.debug(f"make a rooted tree from the head vector {head_vector=}")
		rt = self.LAL_module.graphs.from_head_vector_to_rooted_tree(head_vector)
		
		tbp_logging.debug(f"the graph has {rt.get_num_nodes()} nodes")
		tbp_logging.debug(f"the graph has {rt.get_num_edges()} edges")
		tbp_logging.debug(f"Is the graph a rooted tree? {rt.is_rooted_tree()}")

		return rt
	
	def _join_multiword_tokens(self, rt):

		#return any(map( lambda x: id in x[0], self.m_multiword_tokens))



		return rt
	
	def _remove_words_tree(self, rt):
		r"""
		This function applies the actions passed as parameters (removal of punctuation
		marks, function words, ...).
		"""
		
		if len(self.m_word_discard_functions) == 0:
			# nothing to do
			return rt
		
		for token in reversed(self.m_current_tree_tokens):

			if not any(map(lambda f: f(token), self.m_word_discard_functions)):
				# word does not meet any criterion for removal
				continue
			
			# calculate the (actual) id of the word to be removed
			token_id = int(token.get_ID()) - 1
			
			tbp_logging.debug(f"Remove {token_id}. Original ID: {token.get_ID()} -- '{token.get_FORM()}'")
			tbp_logging.debug(f"Tree has root? {rt.has_root()}.")
			
			if rt.has_root() and rt.get_root() == token_id:
				tbp_logging.warning(f"Removing the root of the tree.")
				tbp_logging.warning(f"This will make the structure become a forest.")
			
			tbp_logging.debug(f"Tree has {rt.get_num_nodes()} nodes. Word to be removed: {token_id=}")
			if token_id >= rt.get_num_nodes():
				tbp_logging.critical(f"Trying to remove a non-existent vertex. The program should crash now.")
				tbp_logging.critical(f"    Please, rerun the program with '--lal --verbose 3' for further debugging.")
			
			# remove the node
			rt.remove_node(token_id)
		
		tbp_logging.debug("All actions have been applied")

		if not rt.check_normalised():
			rt.normalise()
		return rt

	def _store_head_vector(self, rt):
		r"""
		This function converts whatever is left from applying the actions into
		a head vector, which is then stored in the variable 'm_head_vector_collection'.
		"""
		
		if not rt.is_rooted_tree():
			# 'rt' is not a valid rooted tree. We do not know how to store this
			# as a head vector.
			tbp_logging.warning(f"This graph is not a rooted tree. Ignored.")
		
		elif not self._should_discard_tree(rt):
			# The rooted tree should not be discarded. Its number of vertices
			# (words) is 1 or more and is not too short, nor too long.
			
			tbp_logging.debug("Apply postprocess functions to the tree")

			# apply sentence postprocess functions
			for f in self.m_sentence_postprocess_functions:
				rt = f(rt)

			tbp_logging.debug("Transform into a head vector and store it")

			# Store the head vector of this rooted tree
			hv = str(rt.get_head_vector()).replace('(', '').replace(')', '').replace(',', '')
			self.m_head_vector_collection.append(hv)

	def _make_word_discard_functions(self, args):
		# make lambdas for all actions applied on a word
		self.m_word_discard_functions = []
		
		# Remove punctuation marks
		if args.RemovePunctuationMarks:
			self.m_word_discard_functions.append( lambda w: w.is_punctuation_mark() )
		# Remove function words
		if args.RemoveFunctionWords:
			self.m_word_discard_functions.append( lambda w: w.is_function_word() )
		
	def _make_sentence_discard_functions(self, args):
		# make lambdas for all actions that discard sentences
		self.m_sentence_discard_functions = []
		
		# Discard short sentences
		if args.DiscardSentencesShorter != -1:
			self.m_sentence_discard_functions.append(
				lambda rt: rt.get_num_nodes() <= args.DiscardSentencesShorter
			)
		# Discard long sentences
		if args.DiscardSentencesLonger != -1:
			self.m_sentence_discard_functions.append(
				lambda rt: rt.get_num_nodes() >= args.DiscardSentencesLonger
			)
		
	def _make_sentence_postprocess_functions(self, args):
		# make lambdas for postprocessing sentences
		self.m_sentence_postprocess_functions = []
		
		# Discard short sentences
		if args.ChunkSyntacticDependencyTree != None:
			Anderson = self.LAL_module.linarr.algorithms_chunking.Anderson
			Macutek = self.LAL_module.linarr.algorithms_chunking.Macutek
			
			if args.ChunkSyntacticDependencyTree == "Anderson":
				self.m_sentence_postprocess_functions.append(
					lambda rt: self.LAL_module.linarr.chunk_syntactic_dependency_tree(rt, Anderson)
				)
			elif args.ChunkSyntacticDependencyTree == "Macutek":
				self.m_sentence_postprocess_functions.append(
					lambda rt: self.LAL_module.linarr.chunk_syntactic_dependency_tree(rt, Macutek)
				)
	
	def _reset_state(self):
		self.m_current_tree_tokens.clear()
		self.m_multiword_tokens.clear()

	def _finish_reading_tree(self):
		tbp_logging.debug("Build the tree...")
		rt = self._build_tree()

		tbp_logging.debug("Remove words if needed...")
		if not self.m_split_multiword_tokens:
			rt = self._join_multiword_tokens(rt)
		rt = self._remove_words_tree(rt)
		
		tbp_logging.debug("Store the head vector...")
		self._store_head_vector(rt)

	def __init__(self, args, lal_module):
		r"""
		Initialises the CoNLL-U parser with the arguments passed as parameter.
		"""
		self.m_current_tree_tokens = []
		self.m_multiword_tokens = [] # pairs of (array of ints, line)
		self.m_head_vector_collection = []
		self.m_input_file = args.inputfile
		self.m_output_file = args.outputfile
		
		# utilities for logging
		self.m_donotknow_msg = "Do not know how to process this. This line will be ignored."
		
		# keep LAL module
		self.LAL_module = lal_module
		
		# make all discard and postprocess functions
		self._make_word_discard_functions(args)
		self._make_sentence_discard_functions(args)
		self._make_sentence_postprocess_functions(args)
		self.m_split_multiword_tokens = args.SplitMultiwordTokens
	
	def parse(self):
		r"""
		Open the input file and read its contents. Transform the contents into trees
		and store them as head vectors in 'm_head_vector_collection'.
		"""
		
		with open(self.m_input_file, 'r', encoding = "utf-8") as f:
			tbp_logging.info(f"Input file {self.m_input_file} has been opened correctly.")

			reading_tree = False
			linenumber = 1
			
			begin_time = time.perf_counter()

			for line in f:
				type_of_line = line_type.classify(line)
				
				if type_of_line == line_type.Comment:
					# nothing to do...
					pass
				
				elif type_of_line == line_type.Blank:
					# a blank line found while reading a tree singals
					# the end of the tree in the file

					if reading_tree:
						tbp_logging.debug("Finished reading tree")
						self._finish_reading_tree()
						self._reset_state()
						reading_tree = False
				
				elif type_of_line == line_type.Token:
					# This line has actual information about the tree.

					if not reading_tree:
						# here we start reading a new tree
						reading_tree = True
						tbp_logging.debug(f"Start reading tree at line {linenumber}")
					
					token = line_parser.line_parser(line, linenumber)
					token.parse()
					
					if not self.m_split_multiword_tokens and token.is_multiword_token():
						begin_range, end_range = token.get_ID().split("-")
						begin_range = int(begin_range)
						end_range = int(end_range)
						to_append = ([x for x in range(begin_range, end_range + 1)], token)
						self.m_multiword_tokens.append(to_append)

					if not token.is_multiword_token() and not token.is_empty_token():
						self.m_current_tree_tokens.append(token)
				
				linenumber += 1
			
			tbp_logging.debug("Finished reading file")

			# Finished reading file. If there was some tree being read, process it.
			if reading_tree:
				tbp_logging.debug("Finished reading the last tree")
				self._finish_reading_tree()
				self._reset_state()
			
			end_time = time.perf_counter()
			
			tbp_logging.info(f"Finished parsing the whole input file {self.m_input_file}.")
			tbp_logging.info(f"    In {end_time - begin_time:.3f} s.")
	
	def dump_contents(self):
		r"""
		Dump all the head vectors to the output file.
		"""
		
		with open(self.m_output_file, 'w') as f:
			tbp_logging.info(f"Output file {self.m_output_file} has been opened correctly.")
			tbp_logging.info(f"    Dumping data...")
			
			begin_time = time.perf_counter()
			for hv in self.m_head_vector_collection:
				f.write(hv + '\n')
			end_time = time.perf_counter()
			
			tbp_logging.info(f"Finished writing the head vectors into {self.m_output_file}.")
			tbp_logging.info(f"    In {end_time - begin_time:.3f} s.")
