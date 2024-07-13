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
#           LARCA (Laboratory for Relational Algorithmics, Complexity and Learning)
#           CQL (Complexity and Quantitative Linguistics Lab)
#           Jordi Girona St 1-3, Campus Nord UPC, 08034 Barcelona.   CATALONIA, SPAIN
#           Webpage: https://cqllab.upc.edu/people/lalemany/
#
################################################################################

import os

from PySide6.QtWidgets import QPushButton, QFileDialog, QLineEdit


class FileChooserButton(QPushButton):
	def __init__(self, parent=None):
		super(FileChooserButton, self).__init__(parent)

	def set_type(self, type):
		self.m_type = type
		if self.m_type == "choose_treebank_input":
			self.clicked.connect(self.choose_treebank_input_file)
		elif self.m_type == "choose_treebank_output":
			self.clicked.connect(self.choose_treebank_output_head_vector)
		elif self.m_type == "choose_treebank_collection_input":
			self.clicked.connect(self.choose_treebank_collection_input)
		elif self.m_type == "choose_treebank_collection_output":
			self.clicked.connect(self.choose_treebank_collection_output_directory)
		else:
			print(f"Wrong type '{type}' for FileChooserButton")

	def find_line(self, name):
		return self.parentWidget().findChild(QLineEdit, name)

	def choose_treebank_input_file(self):
		# choose an input file
		dialog = QFileDialog()
		selected_file = dialog.getOpenFileName(self, "Choose input treebank file")

		inputTreebankFile = self.find_line("inputTreebankFile")
		assert(inputTreebankFile is not None)

		# show selected file in the interface
		inputTreebankFile.setText(selected_file[0])

		print(f"Input file chosen '{selected_file[0]}'")

	def choose_treebank_output_head_vector(self):
		dialog = QFileDialog()
		selected_file = dialog.getSaveFileName(self, "Choose output heads file")

		outputTreebankFile = self.find_line("outputTreebankFile")
		assert(outputTreebankFile is not None)

		# show selected file in the interface
		outputTreebankFile.setText(selected_file[0])

		print(f"Output file chosen '{selected_file[0]}'")

	def choose_treebank_collection_input(self):
		# choose an input file
		dialog = QFileDialog()
		selected_file = dialog.getOpenFileName(self, "Choose input treebank collection main file")

		inputTreebankCollectionFile = self.find_line("inputTreebankCollectionFile")
		assert(inputTreebankCollectionFile is not None)

		# show selected file in the interface
		inputTreebankCollectionFile.setText(selected_file[0])

		print(f"Input treebank collection file chosen '{selected_file[0]}'")

	def choose_treebank_collection_output_directory(self):
		dialog = QFileDialog()
		dialog.setFileMode(QFileDialog.Directory)
		dialog.setOption(QFileDialog.ShowDirsOnly)
		selected_directory = dialog.getExistingDirectory(self, "Choose output directory", os.path.curdir)

		outputTreebankCollectionDirectory = self.find_line("outputTreebankCollectionDirectory")
		assert(outputTreebankCollectionDirectory is not None)

		# show selected file in the interface
		outputTreebankCollectionDirectory.setText(selected_directory)
		print(f"Output directory chosen '{selected_directory}'")
