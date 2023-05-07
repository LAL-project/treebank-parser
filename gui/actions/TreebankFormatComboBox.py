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

from PySide2.QtWidgets import QComboBox, QListWidget, QTableWidget

from gui.actions.ActionListItem import ActionListItem
from gui.utils import action_type_module


class TreebankFormatComboBox(QComboBox, object):
	r"""
	The combobox used to store all treebank formats (CoNLL-U, ...)
	"""
	def __init__(self, parent=None):
		super(TreebankFormatComboBox, self).__init__(parent)
		self.m_current_index = 0
		self.currentIndexChanged.connect(self.choose_treebank_format)

	def choose_treebank_format(self):
		# do nothing if there was no change in the index
		if self.currentIndex() == self.m_current_index:
			return

		self.m_current_index = self.currentIndex()

		availableActionList = self.parentWidget().findChild(QListWidget, "availableActionList")
		assert(availableActionList is not None)
		chosenActionTable = self.parentWidget().findChild(QTableWidget, "chosenActionTable")
		assert(chosenActionTable is not None)

		text = self.currentText()

		# if the selection is empty, then empty the list and table
		if availableActionList.count() > 0:
			availableActionList.clear()
		if chosenActionTable.rowCount() > 0:
			chosenActionTable.clear()

		action_module = action_type_module.get_action_type_module(text)
		if action_module is None:
			# nothing more to do
			return

		for key, action_text in action_module.action_text_str.items():
			itemForKey = ActionListItem(key, action_text, availableActionList)
			itemForKey.setToolTip(action_module.action_help_str[key])
			availableActionList.addItem(itemForKey)
