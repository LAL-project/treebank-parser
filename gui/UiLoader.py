# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@gmail.com>
# Modifications by Charl Botha <cpbotha@vxlabs.com>
# * customWidgets support (registerCustomWidget() causes segfault in
#   pyside 1.1.2 on Ubuntu 12.04 x86_64)
# * workingDirectory support in loadUi
# Modifications by Lluís Alemany <lluis.alemany.puig@upc.edu>
# * removed documentation and comments

# found this here:
# https://github.com/lunaryorn/snippets/blob/master/qt4/designer/pyside_dynamic.py

# following the answer in Stack Overflow:
# https://stackoverflow.com/a/14894550/12075306

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import (print_function, division, unicode_literals, absolute_import)

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QMetaObject


class UiLoader(QUiLoader):
	def __init__(self, baseinstance, customWidgets=None):
		QUiLoader.__init__(self, baseinstance)
		self.baseinstance = baseinstance
		self.customWidgets = customWidgets

	def createWidget(self, class_name, parent=None, name=''):
		if parent is None and self.baseinstance:
			return self.baseinstance

		if class_name in self.availableWidgets():
			widget = QUiLoader.createWidget(self, class_name, parent, name)
		else:
			try:
				widget = self.customWidgets[class_name](parent)
			except (TypeError, KeyError) as e:
				raise Exception('No custom widget ' + class_name + ' found in customWidgets param of UiLoader __init__.')

		if self.baseinstance:
			setattr(self.baseinstance, name, widget)

		return widget


def loadUi(uifile, baseinstance=None, customWidgets=None, workingDirectory=None):
	loader = UiLoader(baseinstance, customWidgets)

	if workingDirectory is not None:
		loader.setWorkingDirectory(workingDirectory)

	widget = loader.load(uifile)
	QMetaObject.connectSlotsByName(widget)
	return widget
