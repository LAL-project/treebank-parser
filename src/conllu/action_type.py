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
This module encodes the types of actions that can be performed in the processing
of a CoNLL-U-formatted treebank.

Each action is performed on every syntactic dependency tree.

Action types
============
- `RemovePunctuationMarks` : remove punctuation signs
- `RemoveFunctionWords` : remove function words

Actions can be retrieved as 'key' strings for the command line interface,
and also as 'help' strings with a self explanatory message (useful for,
    e.g., error messages, help messages from command line).

Members of this module
======================
- `action_key_str`: a dictionary relating each action type (listed above) with
a so-called `key` string. These are particularly useful to design the command
line interface so that users can pass actions as parameters.
- `action_help_str`: a dictionary relating each action type (listed above) with
a so-called `help` string. These strings are more useful in displaying messages
on the command line for users to read.
"""

RemovePunctuationMarks = 0
RemoveFunctionWords = 1

action_key_str = {
	RemovePunctuationMarks : "RemovePunctuationMarks",
	RemoveFunctionWords : "RemoveFunctionWords",
}

action_help_str = {
	RemovePunctuationMarks : "Remove punctuation marks from each sentence.",
	RemoveFunctionWords : "Remove function words from each sentence.",
}

#--------------------------------------------------------------------------

RemovePunctuationMarks_str = action_key_str[RemovePunctuationMarks]
RemoveFunctionWords_str = action_key_str[RemoveFunctionWords]

RemovePunctuationMarks_help_str = action_help_str[RemovePunctuationMarks]
RemoveFunctionWords_help_str = action_help_str[RemoveFunctionWords]

#--------------------------------------------------------------------------

if __name__ == "__main__":
	# TESTS
	print("Testing...")
	assert( len(action_key_str) == len(action_help_str) )
	
