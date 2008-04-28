# -*- coding:utf-8; tab-width: 4 -*-
#!/usr/bin/python
# Sejong Parsed Corpus
# $Id$

""" Sejong Parsed Corpus distributed 2007-11-12



TreeBank:
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

import codecs
import sys


class TreeBank:  
	""" tree sample
	; 그 신세계에 냉동 태아(冷凍 胎兒)가 등장한다.
	(S      (NP_AJT         (DP 그/MM)
			 (NP_AJT 신/XPN + 세계/NNG + 에/JKB))
	 (S      (NP_SBJ         (NP     (NP     (NP 냉동/NNG)
									  (NP 태아/NNG))
							  (NP_PRN         (L (/SS)
											   (NP_PRN         (NP     (NP 冷凍/SH)
																(NP 胎兒/SH))
												(R_PRN )/SS))))
			  (X_SBJ 가/JKS))
	  (VP 등장/NNG + 하/XSV + ㄴ다/EF + ./SF)))
"""
	def __init__(self, file):
		self.file = file
		self.number_of_trees = 0
	
	def __iter__(self):
		return self

	def readtree(self): 
		# read SENTENCE FORM
		# read sentence form line and initialize a tree
		line = self.readline()
		self.number_of_trees += 1
		id = str(self.number_of_trees)
		if (line[0:2] == '; '):
			tree = Tree(id, line[2:])
		else:
			sys.exit(1) # ERROR: no sentence form line 

		# PARSE TREE 

		line = self.readline()
		while (line and line !="") :
			(path, number_of_parentheses) = self.parseline(line)
			if tree.root is not None:
				tree.move_up()
			while (path) :
				tree.append_to_current_node( path.pop(0) )	
			
			print reduce(lambda x, y: x + " " +y, tree.get_path_to_current_node())
			for i in xrange(0, number_of_parentheses ):
				tree.move_up()
			line = self.readline()
			
		return tree

	
	def parseline(self, line):
		""" get one tree source line and return path_to_terminal
		path_to_terminal corresponds to one line of TreeBank file.
		It is a tuple of nodes, a terminal node and the number of 
		parentheses at the end of the source line.
		for example,
		
		source line :			(S      (NP_AJT         (DP 그/MM)
		path_to_terminal :    ["S", "NP_AJT", "DP", "그/MM", 1]
		"""
		temparr = line.split("\t")	

		# process NON-TERMINAL NODES
		# append ["S", "NP_AJT"]
		path = []
		for x in temparr[:-1]:
			path.append(x.strip()[1:])

		# process LAST NODES
		# finally, append ["DP", "그/MM", 1]
		last = temparr[-1][1:]

		# add LAST NON-TERMINAL NODE ["DP"]
		i = last.find(" ")
		if i > 0 : 
			path.append(last[0:i])
			terminal = last[i:]
		else     : 
			sys.exit(1) # ERROR: illegal terminal node

		# add terminal ["그/MM"] and # of parentheses [1]
		number_of_parentheses = 0
		while (terminal.endswith(")")) :
			terminal = terminal[0:-1]
			number_of_parentheses += 1
		path.append(terminal)
		
		return path, number_of_parentheses

	def readline(self):
		line = self.file.readline()

		# EOF
		# immediately exits the program when EOF is encounterd
		if (line == '') : sys.exit(0)

		if (line[0:2] == '; '):
			return line.rstrip()
		elif (line.strip() == '') :
			return "" 
		else :
			return line.strip()

		
	def next(self):
		return self.readtree()

class Sentence:
	def __init__(self, id, form):
		self.id = id
		self.form = form
		self.words = []
		self.idx = 0
		
		# init words
		ord = 0
		for word in form.split(' '):
			ord += 1
			self.words.append(Word(ord, word))	
	
	def __iter__(self):
		return self

	def next(self):
		if self.idx >= len(self.words):
			raise StopIteration
		w = self.words[self.idx]
		self.idx += 1
		return w


class Word:
	def __init__(self, ord, form):
		self.ord = ord
		self.form = form
		self.morphs = []

class Tree:
	def __init__(self, id, sentence):
		self.id = id
		self.sentence = Sentence(id, sentence)
		self.root = None
		self.current_node = None

	def __str__(self):
		return self.id	

	def get_path_to_current_node(self):
		p = []
		n = self.current_node
		p.insert(0,n.name)
		while ( n is not self.root):
			n = n.parent	
			p.insert(0,n.name)

		return p

	def set_root(self, name):
		self.root = Node(None, name)	
		self.current_node = self.root

	def append_to_current_node(self, name):
		if self.root is None:
			self.set_root(name)
		else :
			node = Node(self.current_node, name)
			self.current_node.append(node)
			self.set_current_node(node)
	
	def set_current_node (self, node):
		self.current_node = node
	
	def move_up(self):
		self.set_current_node(self.current_node.parent)	

class Node:
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.first_child = None
		self.second_child = None
		self.ord = 0
	
	def append(self, node):
		if self.first_child is None:
			self.first_child = node
		elif self.second_child is None :
			self.second_child = node
		else :
			exit(0) # TreeError	

class TerminalNode:
	def __init__(self, ord, parent, word):
		self.ord = ord
		self.parent = parent
		self.word = word

class Morph:
	def __init__(self, form, pos):
		self.form = form
		self.pos = pos
 




class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))


class Test:
	def __init__(self, file):
		treebank = TreeBank(file)
		self.test(treebank, 'utf8')

	def test(self, treebank, enc):
		sys.stdout = Encode(sys.stdout, enc)
		for tree in treebank:
			print "================ beg"
			print tree	
			print tree.id
			print tree.sentence.form
			print tree.root.name
			print "================ end"
			
		
if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	Test(file)
	file.close()


