# -*- coding: utf-8; tab-width: 4 -*-
# Sejong Dependency Treebank 
# $Id$ 

"""
Sejong Dependency Treebank Reader. 

The treebank converted 
from Sejong Parsed Corpus (distributed at 2007-11-12)
by bnk2dep.py script. 

USAGE:

Suppose you have a Sejong Dependency Treebank file named "sejong.dep".

::

	from kltk.corpus.sejong.dep import ForestWalker

	file = codecs.open('sejong.dep', encoding='utf-8')
	fw = ForestWalker(file)

L{ForestWalker} is an iterator of forest (treebank). It isn't
the treebank itself. It does NOT load trees into the memory.

::

	for tree in fw:
		do (tree)

If you want to get a fully-loaded L{TreeBank} object, try getTreeBank().
It takes some time according to the file size.

::

	treebank = fw.getTreeBank()



"""

import codecs
import sys
import re

# intra-package references
from morph import Morph
from morph import Word

class ForestWalker:
	"""ForestWlaker
	"""
	def __init__(self, file):
		"""
		@param file: Sejong Dependency Treebank file
		@type file: file object
		"""
		self.file = file
	
	def __iter__(self):
		return self
	
	def readtree(self):
		"""
		@rtype: L{Tree}
		"""
		# read sentence form line
		line = self._readline()
		i = line.find(';')
		tree = Tree(line[0:i].strip(), line[i+1:-1].strip())

		# make list of nodes
		list_of_nodes = []
		line = self._readline()
		while (line):
			(ord, dep, tag1, tag2, wordform, morph_string) = line.split("\t")	
			morphs = self._parse_morph_string(morph_string)
			word = Word(ord, wordform, morphs, morph_string)
			list_of_nodes.append(Node(ord, dep, tag1, tag2, word))
			line = self._readline()

		# make tree with list of nodes
		# set parent-child relations
		for n in list_of_nodes:
			if n.dep == n.ord:
				tree.set_root(n)
			else:
				p = list_of_nodes[int(n.dep)-1]
				n.parent = p
				p.add_a_child(n)

		tree.nodes = list_of_nodes
		return tree
	
	def _parse_morph_string(self, morph_string):
		"""
		@rtype: list of L{Morph}
		"""
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



	def _readline(self):
		"""
		@rtype: string or list
		@return: a line of the treebank source or a list of fields
		"""
		line = self.file.readline()

		# EOF
		if (line == '') : sys.exit(0)

		return line.strip()

		fields = line.strip().split("\t")
		if len(fields) == 6 :
			return fields
		else :
			return line.strip()	

	def next(self):
		return self.readtree()



class TreeBank:
	"""
	@status: Not yet implemented
	"""
	pass
	
class Tree:
	"""
	Dependency Tree
	"""
	def __init__(self, id, sentence_form):
		self.id = id
		"""
		@type: string
		"""
		self.sentence_form = sentence_form
		"""
		@type: string
		"""
		self.nodes = []
		"""
		@type: list of L{Node}
		"""
		self.root = None
		"""
		@type: L{Node}
		"""
		self.terminals = []
		"""
		@type: list of L{Node}
		"""
	
	def set_root(self, node):
		"""
		@param node: node 
		@type node: L{Node}
		"""
		self.root = node
	
	def get_terminals(self):
		"""
		@rtype: list of L{Node}
		@return: list of terminal nodes
		@warning: Remember this is a dependency tree!
		"""
		if self.terminals :
			pass
		else:
			for n in self.nodes:
				if not n.children :
					self.terminals.append(n)
		return self.terminals



class Node:
	"""
	Node of Dependency L{Tree}
	"""
	def __init__(self, ord, dep, tag1, tag2, word):
		"""
		@param ord: order in the sentence
		@type ord: int
		@param dep: order of the parent
		@type dep: int
		@param tag1: label
		@type tag1: string
		@param tag2: label
		@type tag2: string
		@param word: word
		@type word: L{Word}

		"""
		self.parent = None
		"""parent node
		@type: L{Node}
		"""
		self.children = []
		"""list of child nodes
		@type: list of L{Node}s
		"""
		self.ord = ord
		"""
		@type: int
		"""
		self.dep = dep
		"""ord of parent node
		@type: int
		"""
		self.tag1 = tag1
		"""
		@type: string
		"""
		self.tag2 = tag2
		"""
		@type: string
		"""
		self.form = word.form
		"""
		@type: string
		"""
		self.word = word
		"""
		@type: L{Word}
		"""
	
	def add_a_child(self, node):
		self.children.append(node)

#================
# TEST CODE

class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))



class Test:
	def __init__(self, file, output_encoding):
		self.fw = ForestWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		#self.print_emi_pair()
		self.print_morph()
	

	def print_morph(self):
		for tree in self.fw:
			for n in tree.nodes:
				for m in n.word.morphs:
					print m.form + "/" + m.pos

	def print_emi_pair(self):
		for tree in self.fw:
			for n in tree.nodes:
				if n.word.has_pos("EC") \
				   and n.parent is not None \
				   and n.parent.word.has_pos("EC"):
					sys.stdout.write(tree.id + " ; ")
					for m in n.word.morphs:
						if m.pos == "EC" :
							sys.stdout.write(" -" + m.form)
					sys.stdout.write(" < ")
					for m in n.parent.word.morphs:
						if m.pos == "EC" :
							sys.stdout.write(" -" + m.form)
					sys.stdout.write("\n")

	def print_path_with_more_than_two_ECs(self):
		for tree in self.fw:
			#print tree.id
			for n in tree.get_terminals() :
				path = []
				path.append(n)
				while(n.parent) :
					n = n.parent
					path.append(n)
				
				# print path with more than two ECs
				count = 0
				for n in path:
					if n.word.has_pos("EC") : count += 1 

				if count > 1: 
					sys.stdout.write(tree.id)
					flag = False
					for n in path:
						if n.word.has_pos("EC") : flag = True
						if flag : 
							sys.stdout.write(" < ")
							for m in n.word.morphs :
								if m.pos == "EC":
									sys.stdout.write("-" + m.form)
					print ""



			#self.print_node(tree.root, 0)

	def print_node(self, node, depth):
		print "\t"*depth + node.word
		for n in node.children:
			self.print_node(n, depth+1)
	

if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	Test(file, 'utf-8')
	file.close()
