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
			word = Word(ord, wordform, morphs)
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
	def __init__(self, ord, form, morphs):
		self.ord = ord
		self.form = form
		self.morphs = morphs
	
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
class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))



class Dep2FS:
	def __init__(self, file, output_encoding):
		self.fw = ForestWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		self.dep2fs()
		
	def dep2fs(self) :
		self.print_header()
		for tree in self.fw:
			self.print_nd_open(tree.id, "", "", "", 0, 0)
			sys.stdout.write("(")
			root = self.find_root(tree.nodes) 
			list = tree.nodes
			list.remove(root)
			self.print_node(list, root, 1)
			print ")"
		
	def find_root(self, list):
		for n in list:
			if n.ord == n.dep:
				return n

	def print_node(self, list, node, depth):
		self.print_nd_open(node.word, node.morphs, node.tag1, node.tag2, node.ord, depth)
		children = []
		for n in list:
			if n.dep == node.ord:
				children.append(n)

		if len(children) > 0:
			sys.stdout.write("(")
			while(children) :
				n = children.pop(0)
				self.print_node(list, n, depth+1)
				if(len(children) > 0) : sys.stdout.write(",")
			sys.stdout.write(")")



	def print_nd_open(self, word, morphs, tag1, tag2, ord, depth):
		sys.stdout.write("[%s,%s,%s,%s,%s]" % 
			(word.replace(",","\\,").replace("]","\\]").replace("[","\\[").replace("=", "\\="), 
			morphs.replace(",","\\,").replace("]","\\]").replace("[","\\[").replace("=", "\\="), 
			tag1.replace("]","\\]").replace("[","\\[").replace("=", "\\="), 
			tag2.replace("]","\\]").replace("[","\\[").replace("=", "\\="), 
			str(ord)))
		
	def print_header(self):
		print """@E utf-8
@P form 
@P lemma
@P afun
@P tag
@N ord
"""



class Dep2TrXML:
	def __init__(self, file, output_encoding):
		self.fw = ForestWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		self.dep2trxml()
		
	def dep2trxml(self) :
		self.print_header()
		for tree in self.fw:
			self.print_nd_open(tree.id, "", "", 0, 0)
			root = self.find_root(tree.nodes) 
			list = tree.nodes
			list.remove(root)
			self.print_node(list, root, 1)
			print "</nd>"
		print "</trees>"


		
	def find_root(self, list):
		for n in list:
			if n.ord == n.dep:
				return n

	def print_node(self, list, node, depth):
		self.print_nd_open(node.word, node.tag1, node.tag2, node.ord, depth)
		has_child = False
		for n in list:
			if n.dep == node.ord:
				self.print_node(list, n, depth+1)
				has_child = True
		print depth*"\t" + "</nd>"



	def print_nd_open(self, word, tag1, tag2, ord, depth):
		print depth*"\t" + "<nd form='" + word  \
				+ "' afun='" + tag1 \
				+ "' tag='" + tag2 \
				+ "' ord='" + str(ord)  \
		     	+ "'>"

	def print_header(self):
		print """		
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE trees PUBLIC "-//CKL.MFF.UK//DTD TrXML V1.0//EN" "http://ufal.mff.cuni.cz/~pajas/tred.dtd" [
<!ENTITY % trxml.attributes "  
  token CDATA #IMPLIED
  label CDATA #IMPLIED
  tag_1 CDATA #IMPLIED
  tag_2 CDATA #IMPLIED
  tag_3 CDATA #IMPLIED
  other CDATA #IMPLIED
  form CDATA #IMPLIED
  ref CDATA #IMPLIED">
]>
<!-- Time-stamp: <Wed Apr 30 03:43:02 2008 TrXMLBackend> -->
<trees>
<info>
  <meta name="schema" content="Fslib::Schema=HASH(0xb4038a0)"/>
</info>
<types full="1">
  <t n="token"/>
  <t n="label"/>
  <t n="tag_1"/>
  <t n="tag_2"/>
  <t n="tag_3"/>
  <t n="other"/>
  <t n="form"/>
  <t n="ref"/>
  <t n="ord"/>
  <t n="dep"/>
  <t n="afun"/>
  <t n="tag"/>
</types>
"""

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
