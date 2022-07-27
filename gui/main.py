################################################################################
#
#   Treebank parser -- A small application that parses a treebank and converts
#   it into a collection of head vectors.
#
#   Copyright (C) 2021-2022
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

import sys
import os

# set up paths before actual gui's start up
if __name__ == "__main__":
	import pathlib
	sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()) + "/..")
	del pathlib

from PySide2.QtWidgets import QAbstractItemView, QApplication, QMainWindow
from PySide2.QtWidgets import QWidget, QTableWidget, QTextEdit, QAction
from PySide2.QtWidgets import QMenu, QMenuBar, QLabel, QVBoxLayout
from PySide2 import QtCore
from PySide2.QtCore import QRect, QFile

from treebank_parser import treebank_formats

from gui import UiLoader
from gui.utils import help_menu_strings
from gui.TreebankFormatSelector import TreebankFormatSelector
from gui.TreebankFormatSelectorData import TreebankFormatSelectorData
from gui.FileChooserButton import FileChooserButton
from gui.ActionListModifier import ActionListModifier
from gui.ChosenActionsTable import ChosenActionsTable
from gui.HelpMenu import HelpMenu
from gui.RunnerButton import RunnerButton
from gui.utils.MyOut import MyOut

class gui_treebank_parser(QMainWindow):
	def __init__(self):
		super(gui_treebank_parser, self).__init__()

		SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
		UiLoader.loadUi(
		    os.path.join(SCRIPT_DIRECTORY, 'form.ui'),
			self,
			{
			    "TreebankFormatSelector": TreebankFormatSelector,
				"TreebankFormatSelectorData": TreebankFormatSelectorData,
				"FileChooserButton": FileChooserButton,
				"ActionListModifier": ActionListModifier,
				"ChosenActionsTable": ChosenActionsTable,
				"RunnerButton": RunnerButton,
				"HelpMenu": HelpMenu
			}
		)

	def make_new_info_popup(self, widget, window_title, label_contents, align=None):
		# set the widget's window title
		widget.setWindowTitle(window_title)
		# create a vertical layout
		vbl = QVBoxLayout(widget);
		# make the label nice
		info_label = QLabel(label_contents, widget)
		if align != None:
			info_label.setAlignment(align)
		# add the info label to the layout
		vbl.addWidget(info_label)
		# adjust size of the popup to the label
		widget.adjustSize()

	def setup_how_to(self):
		self.popup__how_to = QWidget()
		self.make_new_info_popup(
		    self.popup__how_to,
			"How to",
			help_menu_strings.HOW_TO_STR)

	def setup_about(self):
		self.popup__about = QWidget()
		self.make_new_info_popup(
		    self.popup__about,
			"About",
			help_menu_strings.ABOUT_STR,
			QtCore.Qt.AlignHCenter)

	def do_basic_setup(self):
		self.setWindowTitle("Treebank parser")

		print("Set up popups...")
		self.setup_how_to()
		self.setup_about()

		msgLogger = self.findChild(QTextEdit, "msgLogger")
		assert(msgLogger is not None)

		MyOut.set_msg_log(msgLogger)
		print("Setting up interface...")

		# add all available treebank formats
		treebankFormatSelector = self.findChild(TreebankFormatSelector, "treebankFormatSelector")
		assert(treebankFormatSelector is not None)
		for key, format_str in treebank_formats.format_text_str.items():
			print(f"    Add treebank format '{format_str}'")
			treebankFormatSelector.addItem(
			    format_str, TreebankFormatSelectorData(format_str, key)
			)

		# set type of input/output file buttons
		print("Setup 'inputTreebankButton'")
		inputTreebankButton = self.findChild(FileChooserButton, "inputTreebankButton")
		assert(inputTreebankButton is not None)
		inputTreebankButton.set_type("choose_input")

		print("Setup 'outputHeadsButton'")
		outputHeadsButton = self.findChild(FileChooserButton, "outputHeadsButton")
		assert(outputHeadsButton is not None)
		outputHeadsButton.set_type("choose_output")

		# set type of add/remove action buttons
		print("Setup 'actionAddButton'")
		actionAddButton = self.findChild(ActionListModifier, "actionAddButton")
		assert(actionAddButton is not None)
		actionAddButton.set_type("add_action")
		actionAddButton.set_treebankFormatSelector(treebankFormatSelector)

		print("Setup 'actionRemoveButton'")
		actionRemoveButton = self.findChild(ActionListModifier, "actionRemoveButton")
		assert(actionRemoveButton is not None)
		actionRemoveButton.set_type("remove_action")

		# chosen actions table should have single selection only
		print("Setup 'chosenActionTable'")
		chosenActionTable = self.findChild(QTableWidget, "chosenActionTable")
		assert(chosenActionTable is not None)
		chosenActionTable.setSelectionMode(QAbstractItemView.SingleSelection)


if __name__ == "__main__":
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
	app = QApplication([])
	widget = gui_treebank_parser()
	widget.do_basic_setup()
	widget.show()
	sys.exit(app.exec_())