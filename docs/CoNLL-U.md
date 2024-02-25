# CoNLL-U parameter documentation

All the parameters accepted by the CoNLL-U format parser can be queried using the `CoNLL-U --help` parameter. The output is the following:

	usage: main.py CoNLL-U [-h] [--RemoveFunctionWords] [--RemovePunctuationMarks]
                           [--DiscardSentencesShorter length_in_words]
                           [--DiscardSentencesLonger length_in_words]
                           [--ChunkSyntacticDependencyTree {Anderson,Macutek}]

	The parser of a CoNLL-U-formatted file. This command has special mandatory and optional parameters.
	These are listed below.

	optional arguments:
	  -h, --help            show this help message and exit
	  --RemoveFunctionWords
	                        Remove function words from each sentence. A function word is identified by the
	                        values 'ADP', 'AUX', 'CCONJ', 'DET', 'NUM', 'PART', 'PRON', 'SCONJ' in the
	                        corresponding UPOS field. The origins of this description are found in a 2022
	                        paper available at arXiv (https://arxiv.org/abs/2007.15342).
	  --RemovePunctuationMarks
	                        Remove punctuation marks from each sentence. A punctuation mark is identified
	                        by the value 'PUNCT' in the UPOS field.
	  --DiscardSentencesShorter length_in_words
	                        Discard sentences whose length (in words) is less than or equal to (<=) a
	                        given length. This is applied *after* removing punctuation marks and/or
	                        function words.
	  --DiscardSentencesLonger length_in_words
	                        Discard sentences whose length (in words) is greater than or equal to (>=) a
	                        given length. This is applied *after* removing punctuation marks and/or
	                        function words.
	  --ChunkSyntacticDependencyTree {Anderson,Macutek}
	                        Chunks a syntactic dependency tree using the specified algorithm. This is
	                        applied only to those sentences that have not been discarded.

## Notes

Multitoken words are, by default, ignored and are split into its different tokens. In the following example,

    1      nosotros   nosotros
    2      vamos      ir
    3-4    al         _
    3      a          a
    4      el         el
    5      mar        mar
    6      y          y
    7      vosotros   vosotros
    7.1    vais       ir
    8-9    al         _
    8      a          a
    9      el         el
    10     parque     parque

the tree built will contain the tokens with IDS: 1 2 3 4 5 6 7 8 9 10.