# Head-Vector parameter documentation

All the parameters accepted by the Head-Vector format parser can be queried using the `Head-Vector --help` parameter. The output is the following:

	usage: main.py Head-Vector [-h] [--DiscardSentencesShorter length_in_words]
	                           [--DiscardSentencesLonger length_in_words]
	                           [--ChunkSyntacticDependencyTree {Anderson,Macutek}]
	
	The parser of a head vector-formatted file. This command has special mandatory and optional parameters.
	These are listed below.
	
	optional arguments:
	  -h, --help            show this help message and exit
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
