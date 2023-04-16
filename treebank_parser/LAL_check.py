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

def LAL_check():
	r"""
	This method checks if LAL is reachable. Also checks if the version of LAL in
	use is suitable for this version of treebank-parser.
	
	This method returns a pair of error code and error message.
	
	- If LAL is not reachable ('import lal' failed), returns 1,
	- If the version of LAL imported is not correct, returns 2,
	- If LAL (debug) is not reachable ('import laldebug' failed), returns 3,
	- If the version of LAL (debug) imported is not correct, returns 4.
	"""
	
	try:
		import lal
		if lal.version.major != '99.99':
			errmsg = f"Version of LAL {lal.version.major} is not compatible with this version of treebank-parser. Version needed: =99.99 (development version)"
			return (2, errmsg)
		
		del lal
	except ModuleNotFoundError:
		return (1, "LAL could not be imported: 'import lal' failed.")
		
	try:
		import laldebug as lal
		if lal.version.major != '99.99':
			errmsg = f"Version of LAL (debug) {lal.version.major} is not compatible with this version of treebank-parser. Version needed: =99.99 (development version)"
			return (4, errmsg)
		
		del lal
	except ModuleNotFoundError:
		return (3, "LAL (debug) could not be imported: 'import laldebug' failed.")
	
	return (0, "")
