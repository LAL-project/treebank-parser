################################################################################
#
#   Treebank parser -- A small application that parses a treebank and converts
#   it into a collection of head vectors.
#
#   Copyright (C) 2021-2023
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
First, find the treebank input file using the appropriate 'select'\n\
button to the right of the intreface. Then, select the output file.\n\
You can give any name you want to this file.\n\
\n\
After this, select the correct format of the input treebank file. If\n\
the input file is in CoNLL-U format, then choose 'CoNLL-U' in the dropdown\n\
button below 'Choose a format'. A list of actions will appear next to\n\
that button. Select the action(s) you want to be performed on the treebank\n\
and then click 'Add' so that it actually takes effect. The meaning of every\n\
action will appear if you hover the mouse over them in a tooltip text.\n\
If any action needs a value associated to it, the table next to it will\n\
indicate in its third column the data type of the value (e.g., 'Integer').\n\
Fill the cell in the second column with an appropriate value of the\n\
corresponding data type. If an action does not need a value, the third\n\
column will be empty\n\
\n\
Once all the actions have been chosen, you can click 'Run' to actually\n\
transform the input treebank file into a head vector file. Optionally,\n\
you can tell the parser to use a debug compilation of the Linear Arrangement\n\
Library by checking the checkbox 'Use laldebug'.\n\
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
