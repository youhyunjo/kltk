#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4 -*-
# 
# $Id$ 
""" print list of sentences 

USAGE:
$ list-sentences sejong-parsed.dep > morphs.list
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

class DoIt:
	def __init__(self, file, output_encoding):
		self.fw = ForestWalker(file)
		sys.stdout = Encode(sys.stdout, output_encoding)
		self.print_sentences()
	

	def print_sentences(self):
		for tree in self.fw:
			s = tree.id 
			for n in tree.nodes:
				for m in n.word.morphs:
					s = s + " " +  m.form + "/" + m.pos
			print s

if __name__ == '__main__':
	file = codecs.open(sys.argv[1], encoding='utf-8')
	DoIt(file, 'utf-8')
	file.close()
