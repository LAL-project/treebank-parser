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

from PySide2.QtWidgets import QPushButton, QFileDialog, QLineEdit


class FileChooserButton(QPushButton):
	def __init__(self, parent=None):
		super(FileChooserButton, self).__init__(parent)

	def set_type(self, type):
		self.m_type = type
		if self.m_type == "choose_input":
			self.clicked.connect(self.choose_input_file)
		elif self.m_type == "choose_output":
			self.clicked.connect(self.choose_output_file)
		else:
			print(f"Wrong type '{type}'")

	def choose_input_file(self):
		# choose an input file
		dialog = QFileDialog(None, "Choose input treebank file")
		selected_file = dialog.getOpenFileName()

		inputTreebankFile = self.parentWidget().findChild(QLineEdit, "inputTreebankFile")
		assert(inputTreebankFile is not None)

		# show selected file in the interface
		inputTreebankFile.setText(selected_file[0])

		print(f"Input file chosen '{selected_file[0]}'")

	def choose_output_file(self):
		dialog = QFileDialog(None, "Choose output heads file")
		selected_file = dialog.getSaveFileName()

		outputHeadsFile = self.parentWidget().findChild(QLineEdit, "outputHeadsFile")
		assert(outputHeadsFile is not None)

		# show selected file in the interface
		outputHeadsFile.setText(selected_file[0])

		print(f"Output file chosen '{selected_file[0]}'")
