# -*- coding:utf-8; tab-width: 4 -*-
#!/usr/bin/python
# Sejong Parsed Corpus
# $Id$

""" Sejong Parsed Corpus distributed 2007-11-12



Corpus:
	Tree[] trees

# A sentence string line begins with ";".
# It's a raw string. Morphemes have to be taken
# from the terminal nodes in the tree.

Sentence:
	string		id
	string		form
	Word[]		words

Word:
	string		form
	Morph[]		morphs

# The tree begins after the sentence line.
# It's BINARY TREE.

Tree:
	string		id
	Sentence	sentence
	Node		root

Node:
	string		name
	Node		parent
	Node		first_child
	Node		second_child
	int			ord

TerminalNode:
	Word		word
	int			ord
	Node		parent

Morph:
	string		form
	string		pos
    
"""


