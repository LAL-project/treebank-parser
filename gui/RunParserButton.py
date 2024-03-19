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

from PySide6.QtWidgets import QPushButton, QLineEdit, QSpinBox

from typing import cast

from treebank_parser import treebank_formats, type_strings, output_log
from cli import argument_parser, run_parser

from gui.utils.MyOut import MyOut
from gui.utils import action_type_module

from gui.actions.ActionsTable import ActionsTable
from gui.actions.ActionsTableItem import ActionsTableItem
from gui.actions.ActionsTableComboBox import ActionsTableComboBox
from gui.actions.TreebankFormatComboBox import TreebankFormatComboBox


class RunParserButton(QPushButton):
	def __init__(self, parent=None):
		super(RunParserButton, self).__init__(parent)
		self.clicked.connect(self.run_treebank)

	def run_treebank(self):
		print("Run button was clicked")
		parent = self.parentWidget()

		argument_list = []

		# input treebank file
		inputTreebankFile = parent.findChild(QLineEdit, "inputTreebankFile")
		assert(inputTreebankFile is not None)
		MyOut.info("Retrieving the input treebank file...")
		input_file = inputTreebankFile.text()
		if input_file == "":
			MyOut.error("No input file selected.")
			MyOut.log_separator()
			return
		argument_list += ["-i"]
		argument_list += [input_file]

		# output heads file
		outputHeadsFile = parent.findChild(QLineEdit, "outputHeadsFile")
		assert(outputHeadsFile is not None)
		MyOut.info("Retrieving the output heads file...")
		output_file = outputHeadsFile.text()
		if output_file == "":
			MyOut.error("No output file selected.")
			MyOut.log_separator()
			return
		argument_list += ["-o"]
		argument_list += [output_file]

		# retrieve format selector
		treebankFormatSelector = parent.findChild(TreebankFormatComboBox, "treebankFormatSelector")
		assert(treebankFormatSelector is not None)

		MyOut.info("Retrieving treebank format selected...")
		treebank_format = treebankFormatSelector.currentText()
		print(f"Selected format: '{treebank_format}'")
		# nothing to do if there is no selection
		if treebank_format == "":
			MyOut.error("No treebank format selected.")
			MyOut.log_separator()
			return

		format_key = treebankFormatSelector.currentData().key()
		print(f"    Key of format:   '{format_key}'")
		print(f"    Argument string: '{treebank_formats.treebankformat_key_str[format_key]}'")

		action_module = action_type_module.get_action_type_module(treebank_format)
		assert(action_module is not None)
		
		argument_list += [treebank_formats.treebankformat_key_str[format_key]]
		
		# retrieve chosen actions table
		chosenActionTable = parent.findChild(ActionsTable, "chosenActionTable")
		assert(chosenActionTable is not None)

		MyOut.info("Checking correctness in the values of the chosen actions table...")
		MyOut.add_tab()
		correct_check = chosenActionTable.check_all_items_value()
		MyOut.remove_tab()
		if not correct_check:
			MyOut.log_separator()
			return

		num_rows = chosenActionTable.rowCount()
		for r in range(0, num_rows):
			item0 = cast(ActionsTableItem, chosenActionTable.item(r, 0))
			action_key = item0.key()
			
			item2 = cast(ActionsTableItem, chosenActionTable.item(r, 2))
			action_value_type = item2.text()
			
			action_value = None
			if action_value_type == type_strings.Integer_type_str:
				item1 = chosenActionTable.item(r, 1)
				action_value = cast(ActionsTableItem, item1).text()
				
			elif action_value_type == type_strings.Choice_type_str:
				item1 = chosenActionTable.cellWidget(r, 1)
				action_value = cast(ActionsTableComboBox, item1).text()

			print(f"Found action '{item0.text()}'")
			print(f"    Of key '{action_key}'")
			print(f"    Of value type '{action_value_type}'")
			print(f"    Of value '{action_value}'")

			argument_list += ["--" + action_module.action_key_str[action_key]]
			if action_value_type == type_strings.Integer_type_str:
				argument_list += [str(action_value)]
			
			elif action_value_type == type_strings.Choice_type_str:
				argument_list += [action_value]
		
		print(f"Complete list of arguments: '{argument_list}'")

		MyOut.info("Running treebank parser...")

		# verbose flags
		verbose_level = parent.findChild(QSpinBox, "loggingLevelSpinBox").value()

		output_log.info = MyOut.nothing
		output_log.debug = MyOut.nothing
		output_log.warning = MyOut.nothing
		output_log.error = MyOut.nothing
		output_log.critical = MyOut.nothing
		if verbose_level >= 0:
			output_log.error = MyOut.error
			output_log.critical = MyOut.critical
		if verbose_level >= 1:
			output_log.warning = MyOut.warning
		if verbose_level >= 2:
			output_log.info = MyOut.info
		if verbose_level >= 3:
			output_log.debug = MyOut.debug
		
		parser = argument_parser.create_parser()
		args = parser.parse_args(argument_list)
		run_parser.run(args, parent.parentWidget().LAL_module)

		MyOut.info("    Done")
		MyOut.log_separator()
