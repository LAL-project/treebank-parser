################################################################################
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
#           LARCA (Laboratory for Relational Algorithmics, Complexity and Learning)
#           CQL (Complexity and Quantitative Linguistics Lab)
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
# 
################################################################################

r"""
This script contains functions that create an argument parser object for the CoNLL-U format.
"""

import argparse

from treebank_parser import treebank_formats as formats
from treebank_parser.conllu import action_type as action_type

class OneTimeOptionalArgument(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if getattr(namespace, self.dest) is None:
			setattr(namespace, self.dest, values)
		else:
			parser.error(f"Optional argument '{option_string}' can be specified at most once.")


def add_arguments_CoNLLU_parser(parser):
	r"""
	Adds the necessary arguments to `parser` for CoNLL-U-formatted treebanks.
	"""
	
	# remove function words
	parser.add_argument(
		'--' + action_type.RemoveFunctionWords_key_str,
		default = False,
		action = 'store_true',
		required = False,
		help = action_type.RemoveFunctionWords_help_str
	)
	
	# remove punctuation marks
	parser.add_argument(
		'--' + action_type.RemovePunctuationMarks_key_str,
		default = False,
		action = 'store_true',
		required = False,
		help = action_type.RemovePunctuationMarks_help_str
	)

	# discard short sentences
	parser.add_argument(
		'--' + action_type.DiscardSentencesShorter_key_str,
		default = -1,
		type = int,
		metavar = "length_in_words",
		required = False,
		help = action_type.DiscardSentencesShorter_help_str
	)
	
	# discard long sentences
	parser.add_argument(
		'--' + action_type.DiscardSentencesLonger_key_str,
		default = -1,
		type = int,
		metavar = "length_in_words",
		required = False,
		help = action_type.DiscardSentencesLonger_help_str
	)
	
	# chunk tree
	parser.add_argument(
		'--' + action_type.ChunkTree_key_str,
		required = False,
		type = str,
		choices = action_type.ChunkTree_choice_list,
		help = action_type.ChunkTree_help_str,
		action = OneTimeOptionalArgument
	)

