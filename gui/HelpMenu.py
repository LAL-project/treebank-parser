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

from PySide2.QtWidgets import QMenu

from gui.utils.MyOut import MyOut

from treebank_parser import LAL_check

class HelpMenu(QMenu):
	def __init__(self, parent=None):
		super(HelpMenu, self).__init__(parent)
		self.triggered.connect(self.process_trigger)
		self.m_main = parent.parentWidget()

	def check_LAL_is_reachable(self):
		MyOut.info("Checking if LAL can be imported...")
		res = LAL_check.LAL_check()
		if res[0] != 0:
			MyOut.error(res[1])
		else:
			MyOut.info("    LAL can be imported successfully.")

	def process_trigger(self, action):
		if action.text() == "How to":
			# open pop up with a small set of instructions.
			print("Pressed how to")
			self.m_main.popup__how_to.show()
			pass
		elif action.text() == "About":
			# open pop up with info regarding repository, authorship, ...
			self.m_main.popup__about.show()
			pass
		elif action.text() == "Is LAL reachable?":
			self.check_LAL_is_reachable()
		else:
			print(f"Unhandled action {action.text()}")
