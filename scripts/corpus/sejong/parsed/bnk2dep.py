# -*- coding:utf-8; tab-width: 4 -*-
#!/usr/bin/python
# Converts Sejong Parsed Corpus to dependency treebank
# $Id$

""" bnk2dep : converts Sejong Parsed Corpus to dependency treebank

USAGE:

$ bnk2dep sejong-parsed.bnk > sejong-parsed.dep
"""

import codecs
import sys
import kltk.corpus.sejong.parsed

class Encode:
	def __init__(self, stdout, enc):
		self.stdout = stdout
		self.encoding = enc
	def write(self, s):
		self.stdout.write(s.encode(self.encoding))


class Convert:
	def __init__(self, file):
		fw = kltk.corpus.sejong.parsed.ForestWalker(file)
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

		while(node.__class__ is not kltk.corpus.sejong.parsed.TerminalNode):
			if node.second_child is None:
				node = node.first_child
			else :
				node = node.second_child

		return node.ord, dep_name
		
if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	Convert(file)
	file.close()


