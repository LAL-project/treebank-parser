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
#           LQMC (Lingüística Quantitativa, Matemàtica i Computacional)
#           Webpage: https://lqmc.upc.edu/
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
#
######################################################################

r"""
Parser of CoNLLU-formatted files.

This module contains a single class `parser`.
"""

import time

from treebank_parser.generic_parser import generic_parser
from treebank_parser.conllu import line_parser
from treebank_parser.conllu import line_type
import treebank_parser.output_log as tbp_logging

class parser(generic_parser):
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
	def _location(self):
		return f"At sentence {self.m_sentence_number} of ID '{self.m_sentence_id}' (starting at line {self.m_sentence_starting_line})"

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
		for token in self.m_sentence_tokens:
			if token.get_iHEAD() is not None:
				head_vector.append(token.get_iHEAD())

			else:
				tbp_logging.error(self._location())
				tbp_logging.error(f"    At token {token.get_line_number()}")
				tbp_logging.error(f"    Within line: '{token.get_line()}'")
				tbp_logging.error(f"    Head: '{token.get_HEAD()}'")
				tbp_logging.error(f"    {self.m_donotknow_msg}")
				tbp_logging.error(f"    Head ID is not an integer value")
				return None

		# ensure there aren't errors in the head vector (do this with LAL)
		tbp_logging.debug("    Checking mistakes in head vector...")
		err_list = self.LAL_module.io.check_correctness_head_vector(head_vector)
		if len(err_list) > 0:
			tbp_logging.error(self._location())
			tbp_logging.error(f"There were errors within head vector '{head_vector}'")
			for err in err_list:
				tbp_logging.error(f"    {err}")
			tbp_logging.error(self.m_donotknow_msg)
			return None
		
		# make the lal.graphs.rooted_tree() object
		tbp_logging.debug(f"Make a rooted tree from the head vector {head_vector=}")
		rt = self.LAL_module.graphs.from_head_vector_to_rooted_tree(head_vector)
		
		tbp_logging.debug(f"The graph has {rt.get_num_nodes()} nodes")
		tbp_logging.debug(f"The graph has {rt.get_num_edges()} edges")
		tbp_logging.debug(f"Is the graph a rooted tree? {rt.is_rooted_tree()}")

		return rt
	
	def _should_remove_token(self, token):
		return any(map(lambda f: f(token), self.m_token_discard_functions))

	def _remove_words_tree(self, rt):
		r"""
		This function applies the actions passed as parameters (removal of
		punctuation marks, function words, ...).
		"""
		
		n = rt.get_num_nodes()
		
		if len(self.m_token_discard_functions) == 0:
			# nothing to do
			return rt
		
		total_deleted = 0
		tree_vertices__to__tokens = dict( [ (x,x) for x in range(0,n) ] )

		for token in reversed(self.m_sentence_tokens):

			# if word does not meet any criteria for removal
			if not self._should_remove_token(token): continue

			# calculate the (actual) id of the word to be removed
			token_id = int(token.get_ID()) - 1

			# update mapping of actual vertices of the tree to tokens in the sentence
			total_deleted += 1
			for u in range(token_id, n - total_deleted):
				tree_vertices__to__tokens[u] = tree_vertices__to__tokens[u + 1]

			tbp_logging.debug(f"Tree has {rt.get_num_nodes()} nodes. Word to be removed: {token_id=}")
			tbp_logging.debug(f"Remove {token_id}. Original ID: {token.get_ID()} -- '{token.get_FORM()}'")
			tbp_logging.debug(f"Tree has root? {rt.has_root()}.")
			
			going_to_remove_root = False
			if rt.has_root() and rt.get_root() == token_id:
				tbp_logging.warning(self._location())
				tbp_logging.warning(f"    Going to remove the root of the tree.")
				tbp_logging.warning(f"    This may make the structure become a forest.")
				going_to_remove_root = True
			
			if token_id >= rt.get_num_nodes():
				tbp_logging.critical(self._location())
				tbp_logging.critical(f"    Going to remove a non-existent vertex. The program should crash now.")
				tbp_logging.critical(f"    Rerun the program with '--lal --verbose 3' for further debugging.")
			
			if going_to_remove_root:
				# The root is going to be removed. We need to find a root for the
				# rest of the tree. This is going to be the first child that is
				# not to be removed.

				tbp_logging.debug(f"Search over children of {token_id}")
				
				new_root = None
				for u in rt.get_out_neighbors(token_id):
					tbp_logging.debug(f"Child {u}")
					token_u = self.m_sentence_tokens[tree_vertices__to__tokens[u]]
					if not self._should_remove_token(token_u):
						new_root = u
						tbp_logging.debug(f"New root is {new_root=}")
						break
				
				if new_root is None: tbp_logging.debug("No new root was found...")

				rt.remove_node(token_id, False)

				if new_root is not None:
					if new_root > token_id:
						new_root = new_root - 1
						tbp_logging.debug(f"Since we have removed a vertex, the new root index is {new_root=}")

					if new_root < rt.get_num_nodes():
						rt.set_root(new_root)

			else:
				# reattach the children of this token to this token's parent when
				# the token is a punctuation mark
				join_children = self.m_sentence_tokens[token_id].is_punctuation_mark()

				tbp_logging.debug(f"Remove token while joining its parent to its children? {join_children}")
				rt.remove_node(token_id, join_children)

		tbp_logging.debug("All actions have been applied")

		if not rt.is_rooted_tree():
			tbp_logging.debug("The tree resulting from applying all actions is not a rooted tree.")
			tbp_logging.debug(f"Number of vertices: {rt.get_num_nodes()}")
			tbp_logging.debug(f"Number of edges: {rt.get_num_edges()}")
			tbp_logging.debug(f"Has root? {rt.has_root()}")

		return rt

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
		self.m_sentence_id = "Unknown ID"
		self.m_sentence_tokens.clear()

	def _finish_reading_sentence(self):
		tbp_logging.debug(self._location())
		tbp_logging.debug("Building the tree...")
		
		rt = self._build_full_tree()
		if rt is None: return
		if not rt.is_rooted_tree():
			tbp_logging.error("The tree is not a rooted tree. Ignored.")
			return

		tbp_logging.debug("Remove words if needed...")
		rt = self._remove_words_tree(rt)
		
		tbp_logging.debug("Store the head vector...")
		self._store_tree(rt)

	def __init__(self, input_file, output_file, args, lal_module):
		r"""
		Initialises the CoNLL-U parser with the arguments passed as parameter.
		"""

		super().__init__(input_file, output_file, args, lal_module)
		
		# only the non-multiword tokens and the non-empty tokens
		self.m_sentence_tokens = []
		# current sentence ID to easily locate the sentence in the file
		self.m_sentence_id = ""
		self.m_sentence_number = 0
		self.m_sentence_starting_line = 0
	
	def parse(self):
		r"""
		Open the input file and read its contents. Transform the contents into
		trees and store them as head vectors in 'm_head_vector_collection'.
		"""
		
		with open(self.m_input_file, 'r', encoding = "utf-8") as f:
			tbp_logging.info(f"Input file {self.m_input_file} has been opened correctly.")

			reading_sentence = False
			linenumber = 1
			
			begin_time = time.perf_counter()

			for line in f:
				type_of_line = line_type.classify(line)
				
				if type_of_line == line_type.Comment:
					# nothing to do...
					if line.find("sent_id") != -1:
						tbp_logging.debug(f"Going to split line '{line[:-1]}'")
						if line.find('=') != -1:
							self.m_sentence_id = line.split('=')[1].strip()
				
				elif type_of_line == line_type.Blank:
					# a blank line found while reading a sentence signals the end
					# of the sentence in the file

					if reading_sentence:
						tbp_logging.debug(f"Finished reading sentence")
						self._finish_reading_sentence()
						self._reset_state()
						reading_sentence = False
				
				elif type_of_line == line_type.Token:
					# This line has actual information about the sentence.

					if not reading_sentence:
						# here we start reading a new sentence
						reading_sentence = True
						self.m_sentence_starting_line = linenumber
						self.m_sentence_number += 1
						tbp_logging.debug(self._location())
						tbp_logging.debug(f"Start reading sentence")
					
					token = line_parser.line_parser(line, linenumber)
					token.parse()
					
					if not token.is_multiword_token() and not token.is_empty_token():
						self.m_sentence_tokens.append(token)
				
				linenumber += 1
			
			# Finished reading file. If there was some sentence being read, process it.
			if reading_sentence:
				tbp_logging.debug("Finished reading the last sentence")
				self._finish_reading_sentence()
				self._reset_state()
			
			end_time = time.perf_counter()
			
			tbp_logging.info(f"Finished parsing the whole input file {self.m_input_file}.")
			tbp_logging.info(f"    In {end_time - begin_time:.3f} s.")
