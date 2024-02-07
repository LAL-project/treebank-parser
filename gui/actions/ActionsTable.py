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

from PySide2.QtWidgets import QTableWidget

from typing import cast

from gui.actions.ActionsTableItem import ActionsTableItem
from gui.actions.ActionsTableComboBox import ActionsTableComboBox
from gui.utils.MyOut import MyOut
from treebank_parser import type_strings


def msg_non_numeric_value(item_text, col_text):
	return f"The value '{item_text}' for option '{col_text}' has to be an integer numerical value."

def msg_nonvalid_numeric_value(item_text, col_text):
	return f"The value '{item_text}' for option '{col_text}' is not valid: it has to be a positive integer."

class ActionsTable(QTableWidget):
	
	def __init__(self, parent=None):
		super(ActionsTable, self).__init__(parent)
		self.itemChanged.connect(self.contents_item_changed)
		self.m_just_checked = False

	def check_integer_value(self, item0, item1, item2):
		# clear selection to avoid a "recursive" call to this method
		self.clearSelection()
		
		item1_text = item1.text()
		try:
			numerical_value = int(item1_text)
		except ValueError:
			numerical_value = None

		if (numerical_value is None) or (numerical_value is not None and numerical_value < 0):
			# paint the background
			item1.set_color_error()
			# option text
			item0_text = item0.text()

			if numerical_value is None:
				MyOut.error(msg_non_numeric_value(item1_text, item0_text))
			elif numerical_value < 0:
				MyOut.error(msg_nonvalid_numeric_value(item1_text, item0_text))

			MyOut.log_separator()
			return False
		
		# repaint the background to 'Ok' colour
		item1.set_color_ok()
			
		return True
	
	def check_choice_value(self, item0, item1, item2):
		return cast(ActionsTableComboBox, item1).check_value()

	def check_value(self, item0, item1, item2):
		self.m_just_checked = True
		
		# nothing to do for 'None'
		if item2.text() == type_strings.None_type_str:
			return True
		
		# check for Integer values.
		if item2.text() == type_strings.Integer_type_str:
			return self.check_integer_value(item0, item1, item2)
		
		# check for Choice values.
		if item2.text() == type_strings.Choice_type_str:
			return self.check_choice_value(item0, item1, item2)
		
		# unhandled type :(
		print("Internal error: Unhandled value type '{item2.text()}'")
		return False

	def check_all_items_value(self):
		self.m_just_checked = True
		
		for r in range(0, self.rowCount()):
			item0 = self.item(r, 0)
			
			item1 = self.item(r, 1)
			if item1 is None:
				item1 = self.cellWidget(r, 1)
			
			item2 = self.item(r, 2)
			
			if not self.check_value(item0, item1, item2):
				return False
		
		return True

	def contents_item_changed(self, item1):
		if self.m_just_checked:
			self.m_just_checked = False
			return
		
		# This method is also called when the items are created. Unfortunately,
		# when the item at column 0 is created, the other two have not been created
		# yet. When the item (or widget) at column 1 is created, the second still
		# needs to be created. The issue with this is that we need the item at
		# column 2 to know what to do when checking for correctness of item 1...
		
		if item1.column() != 1:
			# this item is not the one we want to keep track of
			return
		
		item0 = self.item(item1.row(), 0)
		item2 = self.item(item1.row(), 2)
		
		if item0 is None or item2 is None:
			# then this item has not yet been created, nothing to do
			return
		
		if item2.text() == type_strings.Choice_type_str:
			item1 = cast(ActionsTableComboBox, item1)
		else:
			item1 = cast(ActionsTableItem, item1)

		print( "An item's value was changed by the user")
		print(f"    original option:   '{item0.text()}'")
		print(f"    item's key:        '{item0.key()}'")
		print(f"    item's row:        '{item0.row()}'")
		print(f"    item's col:        '{item0.column()}'")
		print(f"    item's value:      '{item1.text()}'")
		print(f"    item's value type: '{item2.text()}'")

		# no need to inspect the returned value
		self.check_value(item0, item1, item2)

