# -*- coding:utf-8; tab-width: 4 -*-
#!/usr/bin/python
# Sejong Parsed Corpus
# $Id$

""" Sejong Parsed Corpus (distributed 2007-12-11)

The class ForestWalker is specific to the Sejong Parsed Corpus
and all the other classes are general, i.e. reusable!

USAGE:

You have a Sejong parsed corpus file named 'BGJO0150.bnk'. 
At first, remove XML tags and check file encoding.

	file = codecs.open('BGJO0150-noxml.bnk' encoding='utf-8')
	fw = ForestWalker(file)

ForestWalker is an iterator of forest (treebank). It isn't the
treebank itself. It does NOT load trees to the memory. It's
light and fast!

	for tree in fw:
		do (tree)

If you want to get a fully-loaded treebank object, try getTreeBank().
It takes some time according to the file size. 

	treebank = fw.getTreeBank()


CLASSES:

ForestWalker

TreeBank
	Tree[]
		Sentence
			Word[]
				Morph[]
		Node

TerminalNode

"""

import codecs
import sys
import re

# intra-package references
from morph import Morph
from word import Word

class TreeParseError(Exception):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return repr(self.message)



# parsed corpus sample tree
# ----------------
# 	; 그 신세계에 냉동 태아(冷凍 胎兒)가 등장한다.
# 	(S      (NP_AJT         (DP 그/MM)
# 			 (NP_AJT 신/XPN + 세계/NNG + 에/JKB))
# 	 (S      (NP_SBJ         (NP     (NP     (NP 냉동/NNG)
# 									  (NP 태아/NNG))
# 							  (NP_PRN         (L (/SS)
# 											   (NP_PRN         (NP     (NP 冷凍/SH)
# 																(NP 胎兒/SH))
# 												(R_PRN )/SS))))
# 			  (X_SBJ 가/JKS))
# 	  (VP 등장/NNG + 하/XSV + ㄴ다/EF + ./SF)))
# ----------------
class ForestWalker:  
	def __init__(self, file):
		self.file = file
		self.number_of_trees = 0
	
	def __iter__(self):
		return self

	def next(self):
		return self.readtree()

	def readtree(self): 
		# INITIALIZE
		self.number_of_trees += 1
		id = str(self.number_of_trees)

		# SENTENCE FORM
		# read sentence form line and initialize a tree
		line = self.readline()

		if (line[0:2] == '; '):
			i = 0
			sentence_form = line[2:]
			tree = Tree(id, Sentence(id, sentence_form, None))
		else:
			print "ERROR: no sentence form line"
			sys.exit(1) # ERROR: no sentence form line 


		# PARSE TREE 
		ord = 0
		line = self.readline()
		while (line and line !="") :
			ord += 1

			try :
				(path, number_of_parentheses) = self.parseline(line)
			except TreeParseError, e:
				print "TreeParseError: ", e.message

			if tree.root is not None:
				tree.move_up()

			# NON-TERMINAL NODES
			while (len(path) > 1) :
				tree.add_child_to_current_node( Node(None, path.pop(0)) )	

			# TERMINAL (LEXICAL) NODE
			morph_string = path.pop(0)
			morphs = self.parse_morph_string(morph_string)
			w = Word(ord, morph_string, morphs, morph_string)

			#print tree.current_node.name, morph_string, w.form
				

			tnode = TerminalNode(ord, None, morph_string, w)
			tree.add_child_to_current_node( tnode )
			tree.lexical_nodes.append(tnode)
			
			for i in xrange(0, number_of_parentheses ):
				tree.move_up()
			line = self.readline()
			
		return tree

	def parse_morph_string(self, morph_string):	
		morphs = []

		m = morph_string
		for m in morph_string.split('+'):
			m = m.strip()
			if m == "" :
				pass
			else :
				if m == "/SW":
					form, pos = "+", "SW"
				elif m[0:2] == "//":
					form, pos = "/", m[2:]
				else :
					try :
						form, pos = m.split("/")
						if pos == "" : pos = "_ERR_"
					except :
						form, pos = m, "_ERR_"	
				morphs.append(Morph(form,pos))
		
		return morphs

	def parseline(self, line):
		""" get a tree source line and return path_to_terminal.
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
			raise TreeParseError("Illegal terminal node")
			#sys.exit(1) # ERROR: illegal terminal node

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

		


class TreeBank:
	def __init__(self):
		pass

		
class Tree:
	def __init__(self, id, sentence):
		self.id = id
		self.sentence = sentence
		self.root = None
		self.current_node = None
		self.lexical_nodes = []

	def __str__(self):
		return self.id	

	def get_path_to_current_node(self):
		return self.get_path_to_node(self.current_node)
	
	def get_path_to_node(self, node):
		p = []
		n = node
		p.insert(0,n.name)
		while ( n is not self.root):
			n = n.parent	
			p.insert(0,n.name)

		return p		

	def set_root(self, node):
		self.root = node
		self.root.set_head(True)

	def add_child_to_current_node(self, node):
		if self.root is None:
			self.set_root(node)
		else :
			self.add_child_to_node(self.current_node, node)

		self.set_current_node(node)

	def add_child_to_node(self, node, child):
		node.add_child(child)
	
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
		self.head_flag = False
	
	def is_head(self):
		return self.head_flag
	
	def set_head(self, bool):
		self.head_flag = bool	
	
	def set_parent(self, node):
		self.parent = node

	def add_child(self, node):
		if self.first_child is None:
			node.set_parent(self)
			self.first_child = node
			self.first_child.set_head(True)
		elif self.second_child is None :
			node.set_parent(self)
			self.second_child = node
			self.first_child.set_head(False)
			self.second_child.set_head(True)
		else :
			print node.name
			print "ERROR: more than 2 children"
			sys.exit(0) # TreeError	: more than 2 children

class TerminalNode (Node):
	def __init__(self, ord, parent, morph_string, word):
		self.ord = ord
		self.name = word.form
		self.morph_string = morph_string
		self.word = word
		self.parent = parent
		self.set_head(True)

	def __str__(self):
		return self.name
		
class Sentence:
	def __init__(self, id, form, words):
		self.id = id
		self.form = form
		self.words = words 
		self.idx = 0
		
			
	def __iter__(self):
		return self

	def next(self):
		if self.idx >= len(self.words):
			raise StopIteration
		w = self.words[self.idx]
		self.idx += 1
		return w

#===============================================================
# CODE FOR TEST

class Encode:
	def __init__(self, stdout, enc):
		self.stdout = stdout
		self.encoding = enc

	def write(self, s):
		self.stdout.write(s.encode(self.encoding))


class Test:
	def __init__(self, file):
		fw = ForestWalker(file)
		self.bnk2dep(fw, 'utf8')

	def bnk2dep(self, fw, enc):
		sys.stdout = Encode(sys.stdout, enc)
		for tree in fw:
			#print "================ beg"
			#print "TREE_ID: ", tree.id
			print tree.id, ";", tree.sentence.form
			#print "ROOT_NODE: ", tree.root.name
			for t in  tree.lexical_nodes:
				#print reduce( lambda x, y :  x+" "+y, tree.get_path_to_node(t))
				dep_parent_ord, dep_name = self.get_dep_parent_of_node(t)
				print "%s\t%s\t%s\t%s\t%s\t%s" % (t.ord, dep_parent_ord, dep_name, t.parent.name, t.word, t.name)
			print
			#print "================ end"

	def get_dep_parent_of_node(self, node):
		while(node.is_head() and node.parent is not None):
			node = node.parent


		dep_name = node.name
		if node.parent is not None: 
			node = node.parent

		while(node.__class__ is not TerminalNode):
			if node.second_child is None:
				node = node.first_child
			else :
				node = node.second_child

		return node.ord, dep_name
		
if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	Test(file)
	file.close()


