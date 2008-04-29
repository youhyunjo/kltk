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
		tree = Tree(line)

		line = self.readline()
		while (line):
			(ord, dep, tag1, tag2, form) = line.split("\t")	
			tree.nodes.append(Node(ord, dep, tag1, tag2, form))
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



class Test:
	def __init__(self, file, output_encoding):
		self.dw = DepWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		self.dep2trxml()
		
	def dep2trxml(self) :
		for tree in self.dw:
			self.print_nd_open(tree.id, "", "", 0)
			root = self.find_root(tree.nodes) 
			list = tree.nodes
			list.remove(root)
			self.print_node(list, root)
			print "</nd>"


	def find_root(self, list):
		for n in list:
			if n.ord == n.dep:
				return n

	def print_node(self, list, node):
		self.print_nd_open(node.form, node.tag1, node.tag2, node.ord)
		#list.remove(node)
		for n in list:
			if n.dep == node.ord:
				self.print_node(list, n)
				pass
		print "</nd>"



	def print_nd_open(self, form, tag1, tag2, ord):
		print "<nd form=\"" + form  \
				+ "\" tag1=\"" + tag1 \
				+ "\" tag2=\"" + tag2 \
				+ "\" ord=" + str(ord)  \
		     	+ ">"

if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	Test(file, 'utf-8')
	file.close()
