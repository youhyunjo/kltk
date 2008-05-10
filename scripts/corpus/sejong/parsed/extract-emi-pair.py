#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4 -*-
# Extracts emi dependency pairs 
# $Id$ 
""" extract-emi-pair : extracts emi dependency pairs 

USAGE:
$ extract-emi-pair sejong-parsed.dep > emi-pair.list
"""

import codecs
import sys
import re
from kltk.corpus.sejong.dep import ForestWalker

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
		self.print_emi_pair()
		#self.print_morph()
	

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
