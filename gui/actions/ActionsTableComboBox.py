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
#           LQMC (Lingüística Quantitativa, Matemàtica i Computacional)
#           Webpage: https://lqmc.upc.edu/
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
#
################################################################################

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QComboBox

from gui.utils.MyOut import MyOut


class ActionsTableComboBox(QComboBox):
	r"""
	This class is used to create a combobox inside the Actions Table.
	The goal is to be able to run, automatically, a check of its value every
	time it changes (due to an interaction with the user).
	"""
	
	def __init__(self, key, option_text, row, column):
		r"""
		parameters:
		- key: as usual
		- option_text: description of the action, used only to display error
		  messages
		- row, column: location of this widget in the table
		"""
		super(ActionsTableComboBox, self).__init__()
		
		self.currentIndexChanged.connect(self.contents_combobox_changed)
		self.m_key = key
		
		self.m_default_palette = self.palette()
		self.m_row = row
		self.m_column = column
		self.m_just_created = True
		self.m_option = option_text

	def row(self): return self.m_row
	def column(self): return self.m_column

	def set_key(self, key):
		self.m_key = key

	def key(self): return self.m_key
	def option(self): return self.m_option
	
	def contents_combobox_changed(self):
		if self.m_just_created:
			self.m_just_created = False
			return
			
		if self.currentText() == "":
			# in this case the selection is empty and that is not allowed.
			palette = self.palette()
			palette.setColor(QPalette.Button, QColor(255, 0, 0))
			self.setPalette(palette)
			MyOut.error(f"Choice for '{self.option()}' cannot be empty.")
			MyOut.log_separator()
		
		else:
			self.setPalette(self.m_default_palette)

	def text(self):
		return self.currentText()
	
	def check_value(self):
		if self.text() == "":
			MyOut.error(f"Choice for '{self.option()}' cannot be empty.")
			MyOut.log_separator()
			return False
		
		return True
