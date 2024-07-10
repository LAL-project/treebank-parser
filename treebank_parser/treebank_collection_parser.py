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


import treebank_parser.output_log as tbp_logging


def parse_treebank_collection(
	parser,
	treebank_collection_main_file,
	output_directory,
	args,
	lal_module
):
	
	r"""
	Parse a treebank collection
	===========================

	This function passes a treebank collection summarized in the main file
	`treebank_collection_main_file`. The output directory where to store the
	result is indicated at `output_directory`.

	Parameters
	----------

	- parser: the parser object that will parse each individual treebank
	- treebank_collection_main_file: the file that lists all the treebanks in the
	collection. The format is the same as that required by the Linear Arrangement
	Library.
	- output_directory: where to store the output files
	- args: the arguments as parsed by the cli parser.
	- lal_module: the LAL module to use (either debug or release compilations)
	"""

	all_parsers = []
	all_ids = []
	total_num_sentences = []

	tbcolreader = lal_module.io.treebank_collection_reader()
	error = tbcolreader.init(treebank_collection_main_file)
	
	if error.get_error_type() != lal_module.io.treebank_error_type.no_error:
		tbp_logging.critical(error.get_error_message())
		return

	while not tbcolreader.end():
		tbreader = tbcolreader.get_treebank_reader()

		treebank_file = tbreader.get_treebank_filename()
		treebank_id = tbreader.get_treebank_identifier()

		p = parser(
			treebank_file,
			output_directory + "/" + treebank_id + ".hv",
			args,
			lal_module
		)
		p.parse()
		
		all_parsers.append(p)
		all_ids.append(treebank_id)
		total_num_sentences.append(p.get_num_sentences())

		tbcolreader.next_treebank()

	if not args.consistency_in_sentences:
		for p in all_parsers:
			p.dump()
	else:
		if len(set(total_num_sentences)) != 1:
			tbp_logging.warning("Number of sentences parsed is different among the parsers")
			for (id, num_sents) in zip(all_ids, total_num_sentences):
				print(f"Treebank {id} contains {num_sents} sentences")

		num_sents = total_num_sentences[0]
		output_sentence = [
			all(map(lambda p: p.is_sentence_ok(i), all_parsers))
			for i in range(0, num_sents)
		]

		for p in all_parsers:
			p.dump_contents_conditionally(output_sentence)

		pass