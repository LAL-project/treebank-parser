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

from PySide2.QtWidgets import QPushButton, QLineEdit, QSpinBox

from typing import cast

from treebank_parser import treebank_formats, type_strings, output_log
from cli import argument_parser, run_parser

from gui.ChosenActionsTable import ChosenActionsTable
from gui.ChosenActionsTableItem import ChosenActionsTableItem
from gui.TreebankFormatSelector import TreebankFormatSelector
from gui.utils.MyOut import MyOut
from gui.utils import action_type_module


class RunnerButton(QPushButton):
	def __init__(self, parent=None):
		super(RunnerButton, self).__init__(parent)
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

		# verbose flags
		loggingLevelSpinBox = parent.findChild(QSpinBox, "loggingLevelSpinBox")
		argument_list += ["--verbose", str(loggingLevelSpinBox.value())]

		# retrieve format selector
		treebankFormatSelector = parent.findChild(TreebankFormatSelector, "treebankFormatSelector")
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
		print(f"    Argument string: '{treebank_formats.format_key_str[format_key]}'")

		action_module = action_type_module.get_action_type_module(treebank_format)
		assert(action_module is not None)
		
		argument_list += [treebank_formats.format_key_str[format_key]]
		
		# retrieve chosen actions table
		chosenActionTable = parent.findChild(ChosenActionsTable, "chosenActionTable")
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
			col0 = cast(ChosenActionsTableItem, chosenActionTable.item(r, 0))
			action_key = col0.key()

			col1 = cast(ChosenActionsTableItem, chosenActionTable.item(r, 1))
			action_value = col1.text()

			col2 = cast(ChosenActionsTableItem, chosenActionTable.item(r, 2))
			action_value_type = col2.text()

			print(f"Found action '{col0.text()}'")
			print(f"    Of key '{action_key}'")
			print(f"    Of value type '{action_value_type}'")

			argument_list += ["--" + action_module.action_key_str[action_key]]
			if action_value_type == type_strings.Integer_type_str:
				argument_list += [str(action_value)]
		
		print(f"Complete list of arguments: '{argument_list}'")

		MyOut.info("Running treebank parser...")
		
		output_log.tbp_info = MyOut.info
		output_log.tbp_debug = MyOut.debug
		output_log.tbp_warning = MyOut.warning
		output_log.tbp_error = MyOut.error
		output_log.tbp_critical = MyOut.critical
		
		parser = argument_parser.create_parser()
		args = parser.parse_args(argument_list)
		run_parser.run(args, parent.parentWidget().LAL_module)

		MyOut.info("    Done")
		MyOut.log_separator()
