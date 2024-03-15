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
	  --SplitMultiwordTokens
	                        Multiword tokens are ignored and in their place their individual words are used
	                        as nodes of the tree.
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

Consider the following example where we find multiword tokens (3-4, 8-9) and empty nodes (7.1).

	1   nosotros nosotros
	2   vamos    ir
	3-4 al       _
	3   a        a
	4   el       el
	5   mar      mar
	6   y        y
	7   vosotros vosotros
	7.1 vais     ir
	8-9 al       _
	8   a        a
	9   el       el
	10  parque   parque

Multiword tokens, and empty nodes are dealt with as follows:

- Empty nodes (such as 7.1) are always ignored and are never used as part of the tree.
- Users can choose to ignore multiword tokens (such as 3-4) or split them. By default, multiword tokens are used and their words (such as 3 and 4) are ignored instead.
	- If `--RemoveFunctionWords` is used then the tree will not contain a multiword token if *all* of its tokens is a function word.
	- If both `--RemoveFunctionWords` and `--SplitMultiwordTokens` are used then only the tokens (of a multiword token) that are function words will be removed.
