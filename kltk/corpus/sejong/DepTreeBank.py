# -*- coding: utf-8; tab-width: 4 -*-
#!/usr/bin/python
# Dependency Treebank 
# $Id$ 
""" Sejong Dependency Treebank, converted 
from Sejong Parsed Corpus (distributed at 2007-11-12)
by phr2dep of kltk.corpus.sejong.Parsed


"""


import codecs
import sys
import re

class ForestWalker:
	def __init__(self, file):
		self.file = file
	
	def __iter__(self):
		return self
	
	def readtree(self):

		# read sentence form line
		line = self.readline()
		tree = Tree(line.split(' ')[0])

		# make list of nodes
		list_of_nodes = []
		line = self.readline()
		while (line):
			(ord, dep, tag1, tag2, wordform, morph_string) = line.split("\t")	
			morphs = self.parse_morph_string(morph_string)
			word = Word(ord, wordform, morphs, morph_string)
			list_of_nodes.append(Node(ord, dep, tag1, tag2, word))
			line = self.readline()

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



	def readline(self):
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
	pass
	
class Tree:
	def __init__(self, id):
		self.id = id
		self.nodes = []
		self.root = None
		self.terminals = []
	
	def set_root(self, node):
		self.root = node
	
	def get_terminals(self):
		if self.terminals :
			pass
		else:
			for n in self.nodes:
				if not n.children :
					self.terminals.append(n)
		return self.terminals



class Node:
	def __init__(self, ord, dep, tag1, tag2, word):
		self.parent = None
		self.children = []
		self.ord = ord
		self.dep = dep
		self.tag1 = tag1
		self.tag2 = tag2
		self.form = word.form
		self.word = word
	
	def add_a_child(self, node):
		self.children.append(node)

class Word:
	def __init__(self, ord, form, morphs, morph_string):
		self.ord = ord
		self.form = form
		self.morphs = morphs
		self.morph_string = morph_string
	
	def add_morph(self, morph):
		self.morphs.append(morph)
	
	def has_pos(self, pos):
		for m in self.morphs:
			if m.pos == pos :
				return True
		return False

	def __str__(self):
		str = ""
		for m in self.morphs:
			if str == "":
				str = m.form
			elif m.pos[0] == "S" :
				str += m.form
			else :
				str += "-" + m.form
		return str
		#return reduce(lambda x,y: x.form+"-"+y.form, self.morphs)


class Morph:
	def __init__(self, form, pos):
		self.form = form
		self.pos = pos
 

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
