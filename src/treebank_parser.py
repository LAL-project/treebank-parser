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
The main CLI of the treebank parser project.

Run with

	python3 treebank_parser.py --help

to read the usage of this script.

"""

import argparse
import logging

import action_type
import treebank_formats as formats

# ******************************************************************************
# ******************************** Start CLI ***********************************
# ******************************************************************************

# Parse arguments

parser = argparse.ArgumentParser(
	description = 'Parse a CoNLL-formatted file and extract the sentences as head vectors.'
)
parser.add_argument(
	'-i', '--inputfile',
	metavar = 'infile',
	type = str,
	required = True,
	help = 'Name of the input treebank file to be parsed.'
)
parser.add_argument(
	'-o', '--outputfile',
	metavar = 'outfile',
	type = str,
	required = True,
	help = 'Name of the output .heads file.'
)
parser.add_argument(
	'-f', '--format',
	metavar = 'format',
	type = str,
	required = True,
	choices = formats.get_all_formats_key_str(),
	help = f"The format of the input treebank. Choices: {formats.get_all_formats_key_str()}"
)
parser.add_argument(
	'--verbose',
	default = 0,
	type = int,
	required = False,
	help =
	"Output logging messages showing the progress of the script. The higher the\
debugging level the more messages will be displayed. \
Default level: 0 -- display only 'error' and 'critical' messages. \
Debugging levels: \
* 1 -- messages from 0 and 'warning' messages; \
* 2 -- messages from 1 and 'info' messages; \
* 3 -- messages from 2 and 'debug' messages;\
"
)
parser.add_argument(
	'--laldebug',
	default = False,
	action = 'store_true',
	required = False,
	help = f"Use the debug compilation of LAL (import laldebug as lal). The script will run more slowly, but errors will be more likely to be caught. Default: import lal."
)
parser.add_argument(
	'--actions',
	metavar = 'action',
	default = "",
	choices = action_type.get_all_actions_key_str(),
	type = str,
	required = False,
	nargs = '*',
	help = f"Type of actions to be run on the input data for every tree. Actions are not applied in any particular order. Choices: {action_type.get_all_actions_key_str()}."
)
args = parser.parse_args()

# configure logging

logging.basicConfig(
	level = logging.DEBUG,
	format = "[%(levelname)s] %(asctime)s : %(message)s",
	datefmt = '%Y-%m-%d %H:%M:%S'
)
if args.verbose != None:
	if args.verbose == 0:
		logging.disable(logging.WARNING)
	elif args.verbose == 1:
		logging.disable(logging.INFO)
	elif args.verbose == 2:
		logging.disable(logging.DEBUG)
	else:
		logging.disable(logging.NOTSET)

# Print some debugging information regarding parameters

print("--------------------------------------")
print(f"File to be parsed:   '{args.inputfile}'")
print(f"File to create:      '{args.outputfile}'")
print(f"Input file's format: '{args.format}'")
print(f"Verbosity level:     '{args.verbose}'")
logging.critical("Critical messages will be shown.")
logging.error("   Error messages will be shown.")
logging.warning(" Warning messages will be shown.")
logging.info("    Info messages will be shown.")
logging.debug("   Debug messages will be shown.")
print(f"Actions to be performed ({len(args.actions)}):", args.actions)
for action in action_type.get_all_actions_int():
	meaning = action_type.get_action_meaning_str(action)
	key = action_type.get_action_key_str(action)
	print(f"    {meaning}?", key in args.actions)
print("--------------------------------------")

if args.format == formats.get_format_key_str(formats.CoNLLU):
	import conllu.parser
	p = conllu.parser.CoNLLU_parser(args)
	p.parse()
	p.dump_contents()
else:
	logging.error(f"Unhandled format '{args.format}'")
