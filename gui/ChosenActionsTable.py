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
from PySide2.QtGui import QBrush, QColor

from typing import cast

from gui.ChosenActionsTableItem import ChosenActionsTableItem
from gui.utils.MyOut import MyOut
from treebank_parser import type_strings


def msg_non_numeric_value(item_text, col_text):
	return f"The value '{item_text}' for option '{col_text}' has to be a numerical value."


def msg_nonvalid_numeric_value(item_text, col_text):
	return f"The value '{item_text}' for option '{col_text}' is not valid: it has to be a positive integer."


class ChosenActionsTable(QTableWidget):
	edit_cell = 0
	regular_check = 1

	def __init__(self, parent=None):
		super(ChosenActionsTable, self).__init__(parent)
		self.itemChanged.connect(self.contents_item_changed)

	def check_integer_value(self, col0, item, col2, origin):
		item_txt = item.text()
		try:
			numeric_value = int(item_txt)
		except ValueError:
			numeric_value = None

		# clear selection to avoid a "recursive" call to this method
		self.clearSelection()

		if (numeric_value is None) or (numeric_value is not None and numeric_value < 0):
			# paint the background
			item.setBackground(QBrush(QColor(255,0,0)))
			# option text
			col0_text = col0.text()

			# log appropriate error messages depending on the origin
			if origin == ChosenActionsTable.edit_cell:
				MyOut.error("When editing a cell in the chosen actions table")

			if numeric_value is None:
				MyOut.error(msg_non_numeric_value(item_txt, col0_text))
			elif numeric_value < 0:
				MyOut.error(msg_nonvalid_numeric_value(item_txt, col0_text))

			MyOut.log_separator()
			return False

		# successful check: set the background back to normal
		item.setBackground(QBrush(QColor(255,255,255)))
		return True

	def check_value(self, col0, item, col2, origin):
		# nothing to do for 'None'
		if col2.text() == type_strings.None_type_str:
			return True
		# check for Integer values.
		if col2.text() == type_strings.Integer_type_str:
			return self.check_integer_value(col0, item, col2, origin)

		# unhandled type :(
		print("Internal error: Unhandled value type '{col2.text()}'")
		return False

	def check_all_items_value(self):
		reg_check = ChosenActionsTable.regular_check
		for r in range(0, self.rowCount()):
			col0 = self.item(r, 0)
			col1 = self.item(r, 1)
			col2 = self.item(r, 2)
			if not self.check_value(col0, col1, col2, reg_check):
				return False
		return True

	def contents_item_changed(self, item):
		item = cast(ChosenActionsTableItem, item)

		# we want to process only those cases of edited items
		# that have been edited by the user, not by other parts
		# of the program. If currentItem() is not "None" then
		# ther has been some item edited by the user.
		if not item.isSelected():
			return

		col0 = self.item(item.row(), 0)
		col2 = self.item(item.row(), 2)

		print( "An item's value was changed by the user")
		print(f"    original option:   '{col0.text()}'")
		print(f"    item's key:        '{item.key()}'")
		print(f"    item's row:        '{item.row()}'")
		print(f"    item's col:        '{item.column()}'")
		print(f"    item's value:      '{item.text()}'")
		print(f"    item's value type: '{col2.text()}'")

		# no need to inspect the returned value
		self.check_value(col0, item, col2, ChosenActionsTable.edit_cell)

