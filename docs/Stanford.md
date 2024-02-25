# Stanford parameter documentation

All the parameters accepted by the Stanford format parser can be queried using the `Stanford --help` parameter. The output is the following:

	usage: main.py Stanford [-h] [--RemovePunctuationMarks] [--DiscardSentencesShorter length_in_words]
							[--DiscardSentencesLonger length_in_words]
							[--ChunkSyntacticDependencyTree {Anderson,Macutek}]

	The parser of a Stanford-formatted file. This command has special mandatory and optional parameters.
	These are listed below.

	optional arguments:
	  -h, --help            show this help message and exit
	  --RemovePunctuationMarks
							Remove punctuation marks from each sentence. A punctuation mark is identified
							by the dependency type 'punct'.
	  --DiscardSentencesShorter length_in_words
							Discard sentences whose length (in words) is less than or equal to (<=) a given
							length. This is applied *after* removing punctuation marks and/or function
							words.
	  --DiscardSentencesLonger length_in_words
							Discard sentences whose length (in words) is greater than or equal to (>=) a
							given length. This is applied *after* removing punctuation marks and/or
							function words.
	  --ChunkSyntacticDependencyTree {Anderson,Macutek}
							Chunks a syntactic dependency tree using the specified algorithm. This is
							applied only to those sentences that have not been discarded.
