#!/usr/bin/python

import codecs
import sys

class DepWalker:
	def __init__(self, file):
		self.file = file
	
	def __iter__(self):
		return self
	
	def readtree(self):

		line = self.readline()
		tree = Tree(line.split(' ')[0])

		line = self.readline()
		while (line):
			(ord, dep, tag1, tag2, form) = line.split("\t")	
			tree.nodes.append(Node(ord, dep, tag1, tag2, form.strip()))
			line = self.readline()

		return tree

	def readline(self):
		line = self.file.readline()

		# EOF
		if (line == '') : sys.exit(0)

		return line.strip()

		fields = line.strip().split("\t")
		if len(fields) == 5 :
			return fields
		else :
			return line.strip()	

	def next(self):
		return self.readtree()


class Tree:
	def __init__(self, id):
		self.id = id
		self.nodes = []

class Node:
	def __init__(self, ord, dep, tag1, tag2, form):
		self.ord = ord
		self.dep = dep
		self.tag1 = tag1
		self.tag2 = tag2
		self.form = form


#================
class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))



class Dep2FS:
	def __init__(self, file, output_encoding):
		self.dw = DepWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		self.dep2fs()
		
	def dep2fs(self) :
		self.print_header()
		for tree in self.dw:
			self.print_nd_open(tree.id, "", "", 0, 0)
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
		self.print_nd_open(node.form, node.tag1, node.tag2, node.ord, depth)
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



	def print_nd_open(self, form, tag1, tag2, ord, depth):
		sys.stdout.write("[%s,%s,%s,%s]" % (form.replace(",","\\,").replace("]","\\]").replace("[","\\["), tag1.replace("]","\\]").replace("[","\\["), tag2.replace("]","\\]").replace("[","\\["), str(ord)))
		
	#	"[" + form.replace(",","\\,")  \
# 				+ "," + tag1 \
# 				+ "," + tag2 \
# 				+ "," + str(ord)  \
# 		     	+ "]"
# 
	def print_header(self):
		print """@E utf-8
@P form
@P afun
@P tag
@N ord
"""



class Dep2TrXML:
	def __init__(self, file, output_encoding):
		self.dw = DepWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		self.dep2trxml()
		
	def dep2trxml(self) :
		self.print_header()
		for tree in self.dw:
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
		self.print_nd_open(node.form, node.tag1, node.tag2, node.ord, depth)
		has_child = False
		for n in list:
			if n.dep == node.ord:
				self.print_node(list, n, depth+1)
				has_child = True
		print depth*"\t" + "</nd>"



	def print_nd_open(self, form, tag1, tag2, ord, depth):
		print depth*"\t" + "<nd form='" + form  \
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
