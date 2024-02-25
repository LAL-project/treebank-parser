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

from treebank_parser import type_strings

r"""
This module encodes the types of actions that can be performed in the processing
of a Stanford-formatted treebank.

Each action is performed on every syntactic dependency tree.

Action types
============
- `RemovePunctuationMarks` : remove punctuation signs
- `DiscardSentencesShorter` : discard sentences shorter than a given amount of words
- `DiscardSentencesLonger` : discard sentences longer than a given amount of words
- `ChunkTree` : chunks a tree using the specified recipe

Actions can be retrieved as 'key' strings for the command line interface, and
also as 'help' strings with a self explanatory message (useful for, e.g., error
messages, help messages from command line).

Members of this module
======================
- `action_key_str`: a dictionary relating each action type (listed above) with
a so-called `key` string. These are particularly useful to design the command
line interface so that users can pass actions as parameters.

- `action_help_str`: a dictionary relating each action type (listed above) with
a so-called `help` string. These strings are more useful in displaying messages
on the command line for users to read.

- `action_text_str`: a dictionary relating each action type (listed above) with
a short self-contained string similar to human text.

- `action_type_param_str`: a dictionary relating each action type to its parameter
type. If an action has no parameter associated, the type is None.
"""

RemovePunctuationMarks = 0
DiscardSentencesShorter = 2
DiscardSentencesLonger = 3
ChunkTree = 4

# -------------------------------------------------------------------------

action_key_str = {
	RemovePunctuationMarks: "RemovePunctuationMarks",
	DiscardSentencesShorter: "DiscardSentencesShorter",
	DiscardSentencesLonger: "DiscardSentencesLonger",
	ChunkTree: "ChunkSyntacticDependencyTree",
}

RemovePunctuationMarks_key_str = action_key_str[RemovePunctuationMarks]
DiscardSentencesShorter_key_str = action_key_str[DiscardSentencesShorter]
DiscardSentencesLonger_key_str = action_key_str[DiscardSentencesLonger]
ChunkTree_key_str = action_key_str[ChunkTree]

# -------------------------------------------------------------------------

action_help_str = {
	RemovePunctuationMarks: "Remove punctuation marks from each sentence. A punctuation mark is identified by the dependency type 'punct'.",
	DiscardSentencesShorter: "Discard sentences whose length (in words) is less than or equal to (<=) a given length. This is applied *after* removing punctuation marks and/or function words.",
	DiscardSentencesLonger: "Discard sentences whose length (in words) is greater than or equal to (>=) a given length. This is applied *after* removing punctuation marks and/or function words.",
	ChunkTree: "Chunks a syntactic dependency tree using the specified algorithm. This is applied only to those sentences that have not been discarded.",
}

RemovePunctuationMarks_help_str = action_help_str[RemovePunctuationMarks]
DiscardSentencesShorter_help_str = action_help_str[DiscardSentencesShorter]
DiscardSentencesLonger_help_str = action_help_str[DiscardSentencesLonger]
ChunkTree_help_str = action_help_str[ChunkTree]

# ------------------------------------------------------------------------------

action_text_str = {
	RemovePunctuationMarks: "Remove Punctuation Marks",
	DiscardSentencesShorter: "Discard Sentences Shorter",
	DiscardSentencesLonger: "Discard Sentences Longer",
	ChunkTree: "Chunk syntactic dependency tree",
}

RemovePunctuationMarks_text_str = action_text_str[RemovePunctuationMarks]
DiscardSentencesShorter_text_str = action_text_str[DiscardSentencesShorter]
DiscardSentencesLonger_text_str = action_text_str[DiscardSentencesLonger]
ChunkTree_text_str = action_text_str[ChunkTree]

# ------------------------------------------------------------------------------

action_type_param_str = {
	RemovePunctuationMarks: type_strings.None_type_str,
	DiscardSentencesShorter: type_strings.Integer_type_str,
	DiscardSentencesLonger: type_strings.Integer_type_str,
	ChunkTree: type_strings.Choice_type_str,
}

RemovePunctuationMarks_param_str = action_type_param_str[RemovePunctuationMarks]
DiscardSentencesShorter_param_str = action_type_param_str[DiscardSentencesShorter]
DiscardSentencesLonger_param_str = action_type_param_str[DiscardSentencesLonger]
ChunkTree_param_str = action_type_param_str[ChunkTree]

# -------------------------------------------------------------------------

ChunkTree_choice_Anderson = 0
ChunkTree_choice_Macutek = 1

ChunkTree_choices_str = {
	ChunkTree_choice_Anderson: "Anderson",
	ChunkTree_choice_Macutek: "Macutek",
}

ChunkTree_choice_Anderson_str = ChunkTree_choices_str[ChunkTree_choice_Anderson]
ChunkTree_choice_Macutek_str = ChunkTree_choices_str[ChunkTree_choice_Macutek]

action_choices_list = {
	RemovePunctuationMarks: [],
	DiscardSentencesShorter: [],
	DiscardSentencesLonger: [],
	ChunkTree: list(ChunkTree_choices_str.values()),
}

RemovePunctuationMarks_choice_list = action_choices_list[RemovePunctuationMarks]
DiscardSentencesShorter_choice_list = action_choices_list[DiscardSentencesShorter]
DiscardSentencesLonger_choice_list = action_choices_list[DiscardSentencesLonger]
ChunkTree_choice_list = action_choices_list[ChunkTree]
