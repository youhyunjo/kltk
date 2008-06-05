#!/usr/bin/python

from kltk.corpus.sejong.dep import *
import codecs
import sys

class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc

    def write(self, s):
        self.stdout.write(s.encode(self.encoding))

def get_output_string(morphs) :
	str = ""
	pos_arr = []
	morphform_arr = []
	for m in morphs:
		pos_arr.append(m.pos)
		morphform_arr.append(m.form)

	str = morphform_arr[0]
	return str




sys.stdout = Encode(sys.stdout, "utf8")

file = codecs.open(sys.argv[1], encoding="utf8")
fw = ForestWalker(file)

for s in fw:
	for n in s.nodes:
		if n.tag1 == "NP_OBJ" :
			#print n.tag1, n.word.morph_string, n.parent.tag1, n.parent.word.morph_string
			#print n.tag1, n.word.form, n.parent.tag1, n.parent.word.form
			#print n.tag1, n.parent.tag1
			#print n.word.form, n.parent.word.form
			print n.tag1, get_output_string(n.word.morphs), get_output_string(n.parent.word.morphs)



