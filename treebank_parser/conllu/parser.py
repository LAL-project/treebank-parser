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

import itertools
import time

from treebank_parser.conllu import line_parser
from treebank_parser.conllu import line_type
import treebank_parser.output_log as tbp_logging

class multiword_token:
	r"""
	Auxiliary class to store information about multiword tokens. A multiword token
	is a token that contains multiple tokens. For example, 'del' is a multiword
	token with ID, say, 4-5, whose tokens are 'de' (with ID '4') and 'el' (with
	ID '5').

	- `m_token_ids`: all the token IDs that are part of this multiword token
	   (e.g., 'del').
	- `m_parent_ids`: all the IDs of the parents of the individual tokens.
	- `m_rooted_tree`: the rooted tree made up of the edges among words in this
	   multiword token
	- `m_token`: the original token object (e.g., 'del', 4-5).
	"""

	def __init__(self):
		self.m_word_ids = []
		self.m_parent_ids = []
		self.m_unique_parent_ids = []
		
		self.m_normalized_to_word_id = {}
		self.m_rooted_tree = None

		self.m_token = None

	def is_function_multitoken_word(self, tokens):
		return all(map(
			lambda t : tokens[t - 1].is_function_word(),
			self.m_word_ids))

	def set_parent_ids(self, pids):
		self.m_parent_ids = pids
		self.m_unique_parent_ids = list(set(self.m_parent_ids))

	def get_parent_ids(self): return self.m_parent_ids
	def get_unique_parent_ids(self): return list(set(self.m_parent_ids))

	def has_unique_parent(self): return len(self.m_unique_parent_ids) == 1

	def set_token(self, t): self.m_token = t
	def get_token(self): return self.m_token

	def set_word_ids(self, ids): self.m_word_ids = ids
	def get_word_ids(self): return self.m_word_ids

	def get_rooted_tree(self): return self.m_rooted_tree
	def set_rooted_tree(self, rt, normalized_to_word_id):
		self.m_rooted_tree = rt
		self.m_normalized_to_word_id = normalized_to_word_id
	
	def get_word_id_of_tree_vertex(self, u):
		return self.m_normalized_to_word_id.get(u)

	def __repr__(self):
		return f"word ids: '{self.m_word_ids}', parent ids: '{self.m_parent_ids}'"

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
	
	def _is_part_of_multiword_token(self, id):
		r"""
		Is the token with id `id` part of a multiword token?
		"""
		idx = self.m_word_to_multiword_token.get(id)
		if idx is None:
			return (False, idx)
		return (True, idx)

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
	
	def _build_full_tree(self):
		r"""
		This function is used to convert the contents of the member 'm_current_tree'
		into an object of type `lal.graphs.rooted_tree`. This function uses all
		tokens in self.m_current_tree_tokens, which are all the tokens in the
		sentence, excluding multiword tokens (1-2, 8-10, ...) and empty tokens
		(1.1, 5.1, ...)
		"""
		
		# construct the head vector from the lines while ensuring
		# that all heads are numerical
		head_vector = []
		for token in self.m_current_tree_tokens:
			if token.get_iHEAD() is not None:
				head_vector.append(token.get_iHEAD())

			else:
				tbp_logging.error(f"In sentence '{self.m_current_sentence_id}', at token {token.get_line_number()}")
				tbp_logging.error(f"    Within line: '{token.get_line()}'")
				tbp_logging.error(f"    Head: '{token.get_HEAD()}'")
				tbp_logging.error(f"    {self.m_donotknow_msg}")
				tbp_logging.error(f"    Head ID is not an integer value")
				return None

		# ensure there aren't errors in the head vector (do this with LAL)
		tbp_logging.info("Checking mistakes in head vector...")
		err_list = self.LAL_module.io.check_correctness_head_vector(head_vector)
		if len(err_list) > 0:
			
			tbp_logging.error(f"In sentence '{self.m_current_sentence_id}'")
			tbp_logging.error(f"There were errors within head vector '{head_vector}'")
			for err in err_list:
				tbp_logging.error(f"    {err}")
				
			tbp_logging.error(self.m_donotknow_msg)
			return None
		
		# make the lal.graphs.rooted_tree() object
		tbp_logging.debug(f"make a rooted tree from the head vector {head_vector=}")
		rt = self.LAL_module.graphs.from_head_vector_to_rooted_tree(head_vector)
		
		tbp_logging.debug(f"the graph has {rt.get_num_nodes()} nodes")
		tbp_logging.debug(f"the graph has {rt.get_num_edges()} edges")
		tbp_logging.debug(f"Is the graph a rooted tree? {rt.is_rooted_tree()}")

		return rt
	
	def _remove_words_tree(self, rt):
		r"""
		This function applies the actions passed as parameters (removal of
		punctuation marks, function words, ...).
		"""
		
		if len(self.m_token_discard_functions) == 0:
			# nothing to do
			return rt
		
		for token in reversed(self.m_current_tree_tokens):

			if not any(map(lambda f: f(token), self.m_token_discard_functions)):
				# word does not meet any criterion for removal
				continue
			
			# calculate the (actual) id of the word to be removed
			token_id = int(token.get_ID()) - 1
			
			tbp_logging.debug(f"Remove {token_id}. Original ID: {token.get_ID()} -- '{token.get_FORM()}'")
			tbp_logging.debug(f"Tree has root? {rt.has_root()}.")
			
			if rt.has_root() and rt.get_root() == token_id:
				tbp_logging.warning(f"In sentence '{self.m_current_sentence_id}'")
				tbp_logging.warning(f"    Removing the root of the tree.")
				tbp_logging.warning(f"    This will make the structure become a forest.")
			
			tbp_logging.debug(f"Tree has {rt.get_num_nodes()} nodes. Word to be removed: {token_id=}")
			if token_id >= rt.get_num_nodes():
				tbp_logging.critical(f"In sentence '{self.m_current_sentence_id}'")
				tbp_logging.critical(f"    Trying to remove a non-existent vertex. The program should crash now.")
				tbp_logging.critical(f"    Please, rerun the program with '--lal --verbose 3' for further debugging.")
			
			# remove the node -- connect the children of the node with its parent
			rt.remove_node(token_id)
		
		tbp_logging.debug("All actions have been applied")

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

			if not rt.check_normalised():
				rt.normalise()

			# apply sentence postprocess functions
			for f in self.m_sentence_postprocess_functions:
				rt = f(rt)

			tbp_logging.debug("Transform into a head vector and store it")

			# Store the head vector of this rooted tree
			hv = str(rt.get_head_vector()).replace('(', '').replace(')', '').replace(',', '')
			self.m_head_vector_collection.append(hv)

	def _update_multiword_tokens_info(self, rt):
		r"""
		Updates all the necessary information of multiword tokens for adequate
		removal in later stages.
		"""

		for t in self.m_multiword_tokens:
			word_ids = t.get_word_ids()
			
			parent_ids = []
			for w in word_ids:
				wtoken = self.m_current_tree_tokens[w - 1]
				head_int = wtoken.get_iHEAD()
				assert(head_int is not None)
				parent_ids.append( head_int )

			t.set_parent_ids(parent_ids)

			if not t.has_unique_parent():
				min_word_id = min(word_ids)
				normalized_to_word_id = {}
				for w in word_ids:
					normalized_to_word_id[w - min_word_id] = w

				# make edges among the words in this multitoken word
				edges = []
				for u, v in itertools.product(word_ids, repeat=2):
					nu = u - min_word_id
					nv = v - min_word_id
					if nu != nv and rt.has_edge(u - 1, v - 1):
						edges.append( (nu, nv) )
				
				N = len(word_ids)
				rt2 = self.LAL_module.graphs.rooted_tree(N)
				rt2.add_edges(edges)
				
				# retrieve all roots and see if there is only one
				roots = []
				for u in range(0, N):
					if rt2.get_in_degree(u) == 0:
						roots.append(u)
				if len(roots) == 1:
					rt2.set_root(roots[0])
				
				t.set_rooted_tree(rt2, normalized_to_word_id)
	
	def _remove_word_of_a_multiword_token(self, token):
		r"""
		Returns True if a token that is part of a multiword token (e.g., token
		with id, say, '4' and the sentence has a multiword token, say, 4-6) is
		to be removed from the tree.
		"""

		token_id = int(token.get_ID())

		(is_part, idx) = self._is_part_of_multiword_token(token_id)
		if not is_part:
			return False

		multiword_token = self.m_multiword_tokens[idx]
		all_word_ids_in_multiword = multiword_token.get_word_ids()
		assert( token_id in all_word_ids_in_multiword )

		if self.m_remove_function_words:
			# If any of the words in this multiword token is a function word then
			# *all* the tokens have to be removed. So, the token also has to
			# be removed even if it is not a function word itself.
			if multiword_token.is_function_multitoken_word(self.m_current_tree_tokens):
				return True

		if multiword_token.has_unique_parent():
			# In this case, all the words in the multiword token have the same
			# parent. Here we can safely discard a token if it *not* the first
			# in the range.
			if token_id != all_word_ids_in_multiword[0]:
				return True
		else:
			# In this case, there is more than one parent in the multiword token.
			# There are two scenarios concerning the tree we can make with the
			# syntactic dependencies among the words in the multiword token:
			# 1. The tree is an actual rooted tree (unique root, connected): like
			#    a catena.
			# 2. The tree is not a rooted tree (missing edges -> more than one root)
			
			rt = multiword_token.get_rooted_tree()
			assert(rt is not None)

			# Case 1: It is completely safe to remove this token if it is not the
			# root of the tree we can make with the (head,dependent) relationships
			# among the words in the multiword token.
			if rt.is_rooted_tree():
				root = rt.get_root()
				id_not_to_remove = multiword_token.get_word_id_of_tree_vertex(root)
				return token_id != id_not_to_remove

			# Case 2: we are going to keep the first token in the sequence, but
			# this will potentially lead to errors.
			tbp_logging.warning(f"In sentence '{self.m_current_sentence_id}'")
			tbp_logging.warning(f"    Multiword token '{token.get_FORM()}' has multiple parents.")
			tbp_logging.warning(f"    We keep the first token, but this may lead to errors.")
			if token_id != all_word_ids_in_multiword[0]:
				return True
			
		return False

	def _make_token_discard_functions(self, args):
		
		# Remove punctuation marks
		if args.RemovePunctuationMarks:
			self.m_token_discard_functions.append(
				lambda token: token.is_punctuation_mark()
			)
		
		# Remove function words
		if args.RemoveFunctionWords:
			self.m_remove_function_words = True
			self.m_token_discard_functions.append(
				lambda token: token.is_function_word()
			)
		
		# Remove all tokens that are part of a multiword token except one
		if args.SplitMultiwordTokens:
			self.m_join_multiword_tokens = False
		else:
			self.m_join_multiword_tokens = True
			self.m_token_discard_functions.append(
				lambda token: self._remove_word_of_a_multiword_token(token)
			)

	def _make_sentence_discard_functions(self, args):
		
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
		
		# Chunk sentences according to a single algorithm
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
		self.m_current_sentence_id = "Unknown ID"
		self.m_current_tree_tokens.clear()
		self.m_multiword_tokens.clear()
		self.m_word_to_multiword_token.clear()

	def _finish_reading_tree(self):
		tbp_logging.info(f"In sentence '{self.m_current_sentence_id}'")
		tbp_logging.info("    Building the tree...")
		rt = self._build_full_tree()
		if rt is None:
			return

		tbp_logging.info("    Remove words if needed...")
		if self.m_join_multiword_tokens:
			self._update_multiword_tokens_info(rt)

		rt = self._remove_words_tree(rt)
		
		tbp_logging.info("    Store the head vector...")
		self._store_head_vector(rt)

	def __init__(self, args, lal_module):
		r"""
		Initialises the CoNLL-U parser with the arguments passed as parameter.
		"""
		
		# only the non-multiword tokens and the non-empty tokens
		self.m_current_tree_tokens = []
		# current sentence ID to easily locate the sentence in the file
		self.m_current_sentence_id = "Unknown ID"
		
		# only the multiword tokens (1-2, 8-10, ...)
		self.m_multiword_tokens = []
		self.m_word_to_multiword_token = {}

		# all the head vectors to dump into the output file
		self.m_head_vector_collection = []
		# input and output files
		self.m_input_file = args.inputfile
		self.m_output_file = args.outputfile

		self.m_remove_function_words = False
		self.m_join_multiword_tokens = True
		
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
	
	def parse(self):
		r"""
		Open the input file and read its contents. Transform the contents into
		trees and store them as head vectors in 'm_head_vector_collection'.
		"""
		
		with open(self.m_input_file, 'r', encoding = "utf-8") as f:
			tbp_logging.info(f"Input file {self.m_input_file} has been opened correctly.")

			tree_number = 0
			reading_tree = False
			linenumber = 1
			
			begin_time = time.perf_counter()

			for line in f:
				type_of_line = line_type.classify(line)
				
				if type_of_line == line_type.Comment:
					# nothing to do...
					if line.find("sent_id") != -1:
						self.m_current_sentence_id = line.split('=')[1].strip()
					pass
				
				elif type_of_line == line_type.Blank:
					# a blank line found while reading a tree singals
					# the end of the tree in the file

					if reading_tree:
						tbp_logging.debug(f"Finished reading tree {tree_number}")
						self._finish_reading_tree()
						self._reset_state()
						reading_tree = False
				
				elif type_of_line == line_type.Token:
					# This line has actual information about the tree.

					if not reading_tree:
						# here we start reading a new tree
						reading_tree = True
						tree_number += 1
						tbp_logging.debug(f"Start reading tree {tree_number} at line {linenumber}")
					
					token = line_parser.line_parser(line, linenumber)
					token.parse()
					
					if self.m_join_multiword_tokens and token.is_multiword_token():
						begin_range, end_range = token.get_ID().split("-")
						begin_range = int(begin_range)
						end_range = int(end_range)

						to_append = multiword_token()
						to_append.set_word_ids([x for x in range(begin_range, end_range + 1)])
						to_append.set_token(token)

						L = len(self.m_multiword_tokens)
						for i in range(begin_range, end_range + 1):
							self.m_word_to_multiword_token[ i ] = L
						
						self.m_multiword_tokens.append(to_append)

					if not token.is_multiword_token() and not token.is_empty_token():
						self.m_current_tree_tokens.append(token)
				
				linenumber += 1
			
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
