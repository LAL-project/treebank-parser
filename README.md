# Treebank parser

This repository contains a small python application that parses treebanks and converts them into the _head vector_ format so that LAL (the [Linear Arrangement library](https://github.com/LAL-project/linear-arrangement-library)) can process them.

## Head vectors

The _head vector_ format is very easy to understand: a single head vector can represent the underlying tree structure of a single syntactic dependency structure. It does so in the form of a vector of whole, non-negative numbers. In these vectors, every number occupies a position from `1` to `n` (where `n` is the number of vertices of the tree) and indicates the parent vertex for the vertex at the corresponding position. The number `0` represents the root of the tree (that is, the corresponding vertex has no parent); the other numbers represent the _head_ (or _parent_) of the vertex at the corresponding position in the vector.

For example, the head vector

    0 1 1 1 1 1 1
    
represents the simple structure of a _star tree_:



This other head vector has a slightly more complicated structure,



Those familiar with the Universal Dependencies format are already accostumed to dealing with _heads_. Consider the following phrase (taken from [UD English](https://github.com/UniversalDependencies/UD_English-PUD/blob/master/en_pud-ud-test.conllu)).

    # sent_id = n01002042
    # te  xt = The new spending is fueled by Clinton’s large bank account.
    1	The	the	DET	DT	Definite=Def|PronType=Art	3	det	3:det	_
    2	new	new	ADJ	JJ	Degree=Pos	3	amod	3:amod	_
    3	spending	spending	NOUN	NN	Number=Sing	5	nsubj:pass	5:nsubj:pass	_
    4	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	5	aux:pass	5:aux:pass	_
    5	fueled	fuel	VERB	VBN	Tense=Past|VerbForm=Part	0	root	0:root	_
    6	by	by	ADP	IN	_	11	case	11:case	_
    7	Clinton	Clinton	PROPN	NNP	Number=Sing	11	nmod:poss	11:nmod:poss	SpaceAfter=No
    8	’s	’s	PART	POS	_	7	case	7:case	_
    9	large	large	ADJ	JJ	Degree=Pos	11	amod	11:amod	_
    10	bank	bank	NOUN	NN	Number=Sing	11	compound	11:compound	_
    11	account	account	NOUN	NN	Number=Sing	5	obl	5:obl:by	SpaceAfter=No
    12	.	.	PUNCT	.	_	5	punct	5:punct	_

The head vector of this sentence can be found at the 7th column:

    3 3 5 5 0 11 11 7 11 11 5 5

## Dependencies

The application is built on (and thus, depends on) the [Linear Arrangement library](https://github.com/LAL-project/linear-arrangement-library). 

## Usage of the application

This application has no GUI (Graphical User Interface). Usage of the command line is required.

