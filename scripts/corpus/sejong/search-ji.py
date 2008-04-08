# -*- coding: utf-8; tab-width: 4 -*-
#!/usr/bin/python
# search.py
# Search emi matrix
# $Id$

import re
import codecs
import sys
import kltk.corpus.sejong.Sense

def cat (str1, str2):
	return str1 + " " + str2

def combine_list(a, b):
	temp = []
	for i in xrange(0, len(a)):
		temp.append(a[i] + "/" + b[i])
	return temp


class Encode:
   def __init__(self, stdout, enc):
      self.stdout = stdout
      self.encoding = enc
   def write(self, s):
      self.stdout.write(s.encode(self.encoding))

file = codecs.open(sys.argv[1], 'r', 'utf-8')
corpus = kltk.corpus.sejong.Sense.Corpus(file)
sys.stdout = Encode(sys.stdout, 'utf-8')

TAG_E = re.compile('(EC|EF|ETM|ETN)')
FORM_JI = re.compile(u'.+지$')
form = []
pos = []
flag_ji = 0

for sentence in corpus:
	form = []
	pos = []
	flag_ji = 0
	for word in sentence.wordlist:
		#print word.gid, word.ord, word.form
		for morph in word.morphlist:
			#print morph.form, morph.pos, morph.sem
			if TAG_E.match(morph.pos) and FORM_JI.match(morph.form):
				flag_ji = 1
	#if len(form) == 3 and pos == ['EC', 'EC', 'EF']:
	if flag_ji == 1:
		print sentence.gid, sentence.form


 
