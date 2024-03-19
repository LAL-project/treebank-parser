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

from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QBrush, QColor


class ActionsTableItem(QTableWidgetItem):
	r"""
	This class is used to add to every item (except widgets) in the Actions Table
	the attribute key, which points us to the global value that points to the
	actual action.
	"""
	
	def __init__(self, key, text):
		super(ActionsTableItem, self).__init__(text)
		self.setText(text)
		self.m_key = key
		self.m_default_color = self.background()
		self.m_contains_error = False

	def set_key(self, key):
		self.m_key = key

	def key(self):
		return self.m_key
	
	def contains_error(self):
		return m_contains_error
	
	def set_color_error(self):
		self.setBackground(QBrush(QColor(255,0,0)))
		self.m_contains_error = True

	def set_color_ok(self):
		self.setBackground(self.m_default_color)
		self.m_contains_error = False
