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

import time
import treebank_parser.output_log as tbp_logging

class generic_parser:

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

	def _store_tree(self, rt):
		r"""
		This function converts whatever is left from applying the actions into
		a head vector, which is then stored in the variable 'm_head_vector_collection'.
		"""
		
		if not rt.is_rooted_tree():
			# 'rt' is not a valid rooted tree. We do not know how to store this
			# as a head vector.
			tbp_logging.warning(f"This graph is not a rooted tree. Ignored.")
			self.m_head_vector_collection.append(None)
		
		elif not self._should_discard_tree(rt):
			# The rooted tree should not be discarded. Its number of vertices
			# (words) is 1 or more and is not too short, nor too long.

			tbp_logging.debug("Apply postprocess functions to the tree")

			if not rt.check_normalized():
				rt.normalize()

			# apply sentence postprocess functions
			for f in self.m_sentence_postprocess_functions:
				rt = f(rt)

			tbp_logging.debug("Transform into a head vector and store it")

			# Store the head vector of this rooted tree
			hv = str(rt.get_head_vector()).replace('(', '').replace(')', '').replace(',', '')
			self.m_head_vector_collection.append(hv)
		
		else:
			self.m_head_vector_collection.append(None)

	def _make_token_discard_functions(self, args):
		raise NotImplementedError("You need to define a '_make_token_discard_functions' method!")
		
	def _make_sentence_discard_functions(self, args):
		raise NotImplementedError("You need to define a '_make_sentence_discard_functions' method!")

	def _make_sentence_postprocess_functions(self, args):
		raise NotImplementedError("You need to define a '_make_sentence_postprocess_functions' method!")

	def __init__(self, input_file, output_file, args, lal_module):

		# all the head vectors to dump into the output file
		self.m_head_vector_collection = []

		# input and output files
		self.m_input_file = input_file
		self.m_output_file = output_file
		
		# utilities for logging
		self.m_donotknow_msg = "Do not know how to process this. This line will be ignored."
		
		# keep LAL module
		self.LAL_module = lal_module
		
		# make all discard and postprocess functions
		self.m_token_discard_functions = []
		self._make_token_discard_functions(args)
		self.m_sentence_discard_functions = []
		self._make_sentence_discard_functions(args)
		self.m_sentence_postprocess_functions = []
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
		raise NotImplementedError("You need to define a 'parse' method!")

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