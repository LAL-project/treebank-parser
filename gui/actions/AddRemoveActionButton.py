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

from PySide2.QtWidgets import QPushButton, QListWidget, QTableWidget, QComboBox
from PySide2.QtCore import Qt

from typing import cast

from gui.actions.ActionListItem import ActionListItem
from gui.actions.ActionsTableItem import ActionsTableItem
from gui.actions.ActionsTableComboBox import ActionsTableComboBox
from gui.utils import action_type_module
from treebank_parser import type_strings


class AddRemoveActionButton(QPushButton):
	def __init__(self, parent=None):
		super(AddRemoveActionButton, self).__init__(parent)

	def set_treebankFormatSelector(self, treebankFormatSelector):
		self.m_treebankFormatSelector = treebankFormatSelector

	def set_type(self, type):
		self.m_type = type
		if type == "add_action":
			self.clicked.connect(self.add_action)
		elif type == "remove_action":
			self.clicked.connect(self.remove_action)
		else:
			print(f"Internal error: wrong type for AddRemoveActionButton button '{type}'")
			pass

	def add_action(self):
		print("Adding available action to chosen actions list...")
		parent = self.parentWidget()

		# retrieve current selection in the available actions list
		availableActionList = parent.findChild(QListWidget, "availableActionList")
		assert(availableActionList is not None)

		selected_item = cast(ActionListItem, availableActionList.currentItem())
		selected_index = availableActionList.currentRow()

		# if no item is selected, there is nothing to do
		if selected_item is None:
			print("    Nothing was selected, so adding nothing.")
			return

		# add current selection in the available actions list
		chosenActionTable = parent.findChild(QTableWidget, "chosenActionTable")
		assert(chosenActionTable is not None)

		print( "    We are adding:")
		print(f"        text in item           '{selected_item.text()}'")
		print(f"        key in item            '{selected_item.key()}'")
		print(f"        index of item in list  '{selected_index}'")
		print(f"        actions chosen so far  '{chosenActionTable.rowCount()}'")

		action_module = action_type_module.get_action_type_module(self.m_treebankFormatSelector.currentText())
		assert(action_module is not None)

		type_text = action_module.action_type_param_str[selected_item.key()]
		print(f"    type of action's parameter '{type_text}'")

		# add a row to the table
		current_row = chosenActionTable.rowCount()
		chosenActionTable.insertRow(chosenActionTable.rowCount())

		# ----------------------------
		# add the items
		
		# item0: item with a self-explanatory text for the action
		# item1: item/widget to input the parameter for the action
		# item2: item with a self-explanatory text for the type of this action's
		#        value
		
		if type_text == type_strings.None_type_str or type_text == type_strings.Integer_type_str:
			item0 = ActionsTableItem(selected_item.key(), selected_item.text())
			item1 = ActionsTableItem(selected_item.key(), "")
			item2 = ActionsTableItem(selected_item.key(), "")

			# set editing options of items
			item0.setFlags(~Qt.ItemIsEditable)
			item0.setToolTip(action_module.action_help_str[selected_item.key()])
			if type_text == type_strings.None_type_str:
				item1.setFlags(Qt.ItemFlag.NoItemFlags)
				item1.setToolTip("This option does not need a value.")
				item2.setFlags(Qt.ItemFlag.NoItemFlags)
				item2.setToolTip("This cell is empty because this action does not need a value.")
			
			elif type_text == type_strings.Integer_type_str:
				item1.setToolTip(f"This option needs a value of type '{type_text}'.")
				#item2.setFlags(...) # no need to set flags
				item2.setFlags(~Qt.ItemFlag.ItemIsEditable)
				item2.setText(type_text)
				item2.setToolTip(f"This cell indicates the type of the value that has to be entered in the cell immediately to its left.")
			
			chosenActionTable.setItem(current_row, 0, item0)
			chosenActionTable.setItem(current_row, 1, item1)
			chosenActionTable.setItem(current_row, 2, item2)
		
		elif type_text == type_strings.Choice_type_str:
			item0 = ActionsTableItem(selected_item.key(), selected_item.text())
			
			item1 = ActionsTableComboBox(selected_item.key(), selected_item.text(), current_row, 1)
			item1.addItems( [""] + action_module.action_choices_list[selected_item.key()] )
			item1.setToolTip(f"This option needs a value of type '{type_text}'.")
			
			item2 = ActionsTableItem(selected_item.key(), type_text)
			item2.setFlags(~Qt.ItemFlag.ItemIsEditable)
			item2.setToolTip(f"This cell indicates the type of the value that has to be entered in the cell immediately to its left.")
			
			chosenActionTable.setItem(current_row, 0, item0)
			chosenActionTable.setCellWidget(current_row, 1, item1)
			chosenActionTable.setItem(current_row, 2, item2)

		chosenActionTable.resizeColumnToContents(0)

		# ----------------------------
		# remove the selected option from the available action list
		removedItem = availableActionList.takeItem(selected_index)
		assert(removedItem is not None)

	def remove_action(self):
		print("Removing selected action from chosen actions list...")
		parent = self.parentWidget()

		# retrieve current selection in the chosen actions list
		chosenActionTable = parent.findChild(QTableWidget, "chosenActionTable")
		assert(chosenActionTable is not None)

		selected_row = chosenActionTable.currentRow()
		print(f"    Current row: {selected_row}")

		if selected_row == -1:
			# nothing to do if nothing is selected
			return

		selected_item = chosenActionTable.item(selected_row, 0)
		selected_item = cast(ActionsTableItem, selected_item)

		print( "    Selected item from chosen actions list")
		print(f"        item key:  {selected_item.key()}")
		print(f"        item text: {selected_item.text()}")

		# insert item to available actions list
		print( "    Move selected item back to available action list")
		availableActionList = parent.findChild(QListWidget, "availableActionList")
		assert(availableActionList is not None)

		action_module = action_type_module.get_action_type_module(self.m_treebankFormatSelector.currentText())

		item_for_key = ActionListItem(selected_item.key(), selected_item.text(), availableActionList)
		item_for_key.setToolTip(action_module.action_help_str[selected_item.key()])
		availableActionList.addItem(item_for_key)

		# remove from chosen actions list
		print( "    Remove from chosen actions list")
		chosenActionTable.removeRow(selected_row)
