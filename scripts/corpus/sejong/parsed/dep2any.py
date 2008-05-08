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
from kltk.corpus.sejong.DepTreeBank import ForestWalker

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
		self.print_nd_open(node.word.form, node.word.morph_string, node.tag1, node.tag2, node.ord, depth)

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



if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	Dep2FS(file, 'utf-8')
	file.close()
