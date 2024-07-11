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
#       Lluís Alemany Puig (lalemany@cs.upc.edu)
#           LARCA (Laboratory for Relational Algorithmics, Complexity and Learning)
#           CQL (Complexity and Quantitative Linguistics Lab)
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
#
################################################################################

HOW_TO_STR = "\
How to use this GUI:\n\
\n\
First, find the treebank input file (when working with a single treebank) or the\n\
treebank collection main file (when working with a treebank collection) by using\n\
the appropriate 'select' button to the right of the interface in the appropriate\n\
tab. Then, select the output file or directory.\n\
\n\
After this, select the correct format of the input treebank file. If the input\n\
file is in CoNLL-U format, then choose 'CoNLL-U' in the dropdown button below\n\
'Choose a format'. A list of actions will appear next to that button. Select the\n\
action(s) you want to be performed on the treebank and then click 'Add' so that\n\
it actually takes effect. The meaning of every action will appear if you hover\n\
the mouse over them in a tooltip text. If any action needs a value associated to\n\
it, the table next to it will indicate in its third column the data type of the\n\
value (e.g., 'Integer'). Fill the cell in the second column with an appropriate\n\
value of the corresponding data type. If an action does not need a value, the\n\
third column will be empty\n\
\n\
Once all the actions have been chosen, you can click 'Run' to actually transform\n\
the input treebank file into a head vector file.\n\
\n\
Optionally, the GUI can be run with either the release or the debug distribution\n\
of LAL. The build of LAL that will be run can be seen in the checkboxes next to\n\
the 'Run' button. Finally, you can set up the verbosity level of the messages\n\
displayed while parsing the trebank. Hover the mouse over the 'Logging messages\n\
level' to see what value works best for you.\
"


ABOUT_STR = "\
Treebank parser GUI\n\
\n\
A small Graphical User Interface of the treebank parser,\n\
a utility to convert a treebank in a fancy format (CoNLL-U, ...)\n\
to the head vector format using the Linear Arrangement Library.\n\
\n\
Authors:\n\
Lluís Alemany Puig (lluis.alemany.puig@upc.edu)\n\
\n\
The code of this gui was downloaded from:\n\
https://github.com/LAL-project/treebank-parser.git\n\
\n\
The code of the Linear Arrangement Library was downloaded from:\n\
https://github.com/LAL-project/linear-arrangement-library.git\
"
