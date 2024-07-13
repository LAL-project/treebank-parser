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

from datetime import datetime


class MyOut:
	def set_tab(str):
		MyOut.tab = str

	def set_msg_log(widget):
		MyOut.message_logger = widget

	def add_tab():
		MyOut.tab += "    "

	def remove_tab():
		MyOut.tab = MyOut.tab[:-4]

	def log_separator():
		MyOut.message_logger.append("---------------------------")

	def get_current_time():
		now = datetime.now()
		return now.strftime("%Y-%m-%d %H:%M:%S")

	def info(str):
		# use current time for the message
		current_time = MyOut.get_current_time()
		# log message
		MyOut.message_logger.append(f"[INFO] {current_time}{MyOut.tab} : {str}")

	def error(str):
		# use current time for the message
		current_time = MyOut.get_current_time()
		# log message
		MyOut.message_logger.append(f"[ERROR] {current_time}{MyOut.tab} : {str}")

	def critical(str):
		# use current time for the message
		current_time = MyOut.get_current_time()
		# log message
		MyOut.message_logger.append(f"[CRITICAL] {current_time}{MyOut.tab} : {str}")
	
	def warning(str):
		# use current time for the message
		current_time = MyOut.get_current_time()
		# log message
		MyOut.message_logger.append(f"[WARNING] {current_time}{MyOut.tab} : {str}")
	
	def debug(str):
		# use current time for the message
		current_time = MyOut.get_current_time()
		# log message
		MyOut.message_logger.append(f"[DEBUG] {current_time}{MyOut.tab} : {str}")

	def nothing(str):
		pass

MyOut.tab = ""
