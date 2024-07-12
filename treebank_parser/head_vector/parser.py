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

This module contains a single class `CoNLLU_parser`.
"""

import time

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
	
	def _make_head_vector(self, line, linenumber):
		# retrieve the head vector from the lines while ensuring
		# that all heads are numerical
		head_vector = []
		for head in line.split(' '):
			try:
				head_int = int(head)
			
			except Exception as e:
				tbp_logging.error(f"At line {linenumber}")
				tbp_logging.error(f"    Head: '{head}'")
				tbp_logging.error(f"    Line: '{line}'")
				tbp_logging.error(f"    Exception: '{e}'")
				return None
			
			head_vector.append(head_int)
		
		return head_vector

	def _build_tree(self, head_vector):
		r"""
		This function is used to convert the contents of the member 'current_tree'
		into an object of type lal.graphs.rooted_tree.
		
		This function then applies the actions passed as parameters (removal of punctuation
		marks, function words, ...).
		
		Finally, the function converts whatever is left from applying the actions into
		a head vector, which is then stored in the variable 'head_vector_collection'.
		"""
		
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

	def _store_head_vector(self, rt):
		
		# -- store the head vector --
		
		if not rt.is_rooted_tree():
			# 'rt' is not a valid rooted tree. We do not know how to store this
			# as a head vector.
			tbp_logging.warning(f"This graph is not a rooted tree. Ignored.")
			self.m_head_vector_collection.append(None)
		
		elif not self._should_discard_tree(rt):
			# The rooted tree should not be discarded. Its number of vertices
			# (words) is 1 or more and is not too short, nor too long.
			
			for f in self.m_sentence_postprocess_functions:
				rt = f(rt)
			
			# Store the head vector of this rooted tree
			hv = str(rt.get_head_vector()).replace('(', '').replace(')', '').replace(',', '')
			self.m_head_vector_collection.append(hv)
		
		else:
			self.m_head_vector_collection.append(None)
	
	def _make_sentence_remove_functions(self, args):
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
			if args.ChunkSyntacticDependencyTree == "Macutek":
				self.m_sentence_postprocess_functions.append(
					lambda rt: self.LAL_module.linarr.chunk_syntactic_dependency_tree(rt, Macutek)
				)

	def __init__(self, input_file, output_file, args, lal_module):
		r"""
		Initialises the CoNLL-U parser with the arguments passed as parameter.
		"""
		self.m_head_vector_collection = []
		self.m_input_file = input_file
		self.m_output_file = output_file
		
		# utilities for logging
		self.m_donotknow_msg = "Do not know how to process this. This line will be ignored."
		
		# keep LAL module
		self.LAL_module = lal_module
		
		# make all functions
		self._make_sentence_remove_functions(args)
		self._make_sentence_postprocess_functions(args)
	
	def get_num_sentences(self):
		r"""
		Returns the number of sentences parsed.
		"""
		return len(self.m_head_vector_collection)
	
	def is_sentence_ok(self, i):
		r"""
		Returns true if the i-th sentence was not discarded.
		"""
		return self.m_head_vector_collection[i] is not None
	
	def parse(self):
		r"""
		Open the input file and read its contents.
		The sentences in CoNLL-U format are stored in the member variable
		'head_vector_collection' in the form of head vectors.
		"""
		
		linenumber = 1
		with open(self.m_input_file, 'r') as f:
			tbp_logging.info(f"Input file {self.m_input_file} has been opened correctly.")
			
			begin = time.perf_counter()
			for line in f:
				
				head_vector = self._make_head_vector(line, linenumber)
				if head_vector is not None:
					rt = self._build_tree(head_vector)
					self._store_head_vector(rt)
				
				linenumber += 1
			
			end = time.perf_counter()
			
			tbp_logging.info(f"Finished parsing the whole input file {self.m_input_file}.")
			tbp_logging.info(f"    In {end - begin:.3f} s.")
	
	def dump_contents(self):
		r"""
		Dump all the head vectors to the output file.
		"""
		
		with open(self.m_output_file, 'w') as f:
			tbp_logging.info(f"Output file {self.m_output_file} has been opened correctly.")
			tbp_logging.info(f"    Dumping data...")
			
			begin = time.perf_counter()
			for hv in filter(lambda s: s is not None, self.m_head_vector_collection):
				f.write(hv + '\n')
			end = time.perf_counter()
			
			tbp_logging.info(f"Finished writing the head vectors into {self.m_output_file}.")
			tbp_logging.info(f"    In {end - begin:.3f} s.")
	
	def dump_contents_conditionally(self, condition):
		r"""
		Dump all the head vectors to the output file conditioned to the values in
		`condition`, which is just an array of as many Boolean values as values
		in `self.m_head_vector_collection`.

		pre: condition[i] must be false if self.m_head_vector_collection[i] is None
		"""
		
		with open(self.m_output_file, 'w') as f:
			tbp_logging.info(f"Output file {self.m_output_file} has been opened correctly.")
			tbp_logging.info(f"    Dumping data...")
			
			begin = time.perf_counter()
			for i in range(0, len(self.m_head_vector_collection)):
				if condition[i]:
					hv = self.m_head_vector_collection[i]
					f.write(hv + '\n')
			end = time.perf_counter()
			
			tbp_logging.info(f"Finished writing the head vectors into {self.m_output_file}.")
			tbp_logging.info(f"    In {end - begin:.3f} s.")
