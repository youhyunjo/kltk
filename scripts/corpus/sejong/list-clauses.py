# -*- coding: utf-8; tab-width: 4 -*-
#!/usr/bin/python
# $Id$

import re
import codecs
import sys
import sejong.Sense

class Encode:
   def __init__(self, stdout, enc):
      self.stdout = stdout
      self.encoding = enc
   def write(self, s):
      self.stdout.write(s.encode(self.encoding))


TAG_SF = re.compile('.+SF')
TAG_EC = re.compile('.+(EC|EF|ETM|ETN).*')
TAG_SEP = re.compile('.*[^ ][+][^ ].*')



file = codecs.open(sys.argv[1], 'r', 'utf-8')
corpus = sejong.Sense.Corpus(file)
sys.stdout = Encode(sys.stdout, 'utf-8')


# print V + VX construction
def print_vx_construction():
   for sentence in corpus:
       for word in sentence.wordlist:
           if word.morphlist[0].pos == "VX":
               if word.ord > 2:
                   print sentence.wordlist[word.ord-2].form, \
							word.morphlist[0].form


# print clause
#
# V VX
# ETM NNB 
#

for sentence in corpus:
	print sentence.gid, sentence.form
	for w in sentence:
		print w.form,

        if w.has('ETM'):
			if w.ord < len(sentence.wordlist):
	        	if sentence.wordlist[w.ord].has('NNB'):
    	        	print "<nnb>",
				else:
					print "<ETM>"
            else:
               	print "<ETM>"
        elif w.has('(ETN)'):
            print "<ETN>"
        elif w.has('VA[+]게/EC'):
            print "<EC>" 
        elif w.has('V.+[+]게/EC'):
            print w.ma_str, "<EC>",
        elif w.has('EC'):
			if w.ord < len(sentence.wordlist):
	            if sentence.wordlist[w.ord].has('VX'):
    	        	print "<vx>",
                else:
					print "<EC>"
            else:
                print "<EC>"
        elif w.has('EF'):
            print "<EF>"
	print
    print "========"


