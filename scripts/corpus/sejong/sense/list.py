#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4 -*-
# list.py

"""
list units of Sejong Morphology Sense Tagged Corpus

USAGE : list unit filename

$ list words sejong-sense.txt > words.list
$ list morphs sejong-sense.txt > morphs.list
$ list senses sejong-sense.txt > senses.list
$ list sentences sejong-sense.txt > sentences.list

$Id$
"""

import codecs
import sys
from kltk.corpus.sejong.sense import Corpus

class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))


class Lister:
    """ """
    def __init__(self, file):
        self.corpus = Corpus(file)

    def printWordList(self):
        for sentence in self.corpus:
            for word in sentence.wordlist:
                print word.form

    def printMorphList(self):
        for sentence in self.corpus:
            for word in sentence.wordlist:
                for morph in word.morphlist:
                    print morph.form + "/" + morph.pos

    def printSenseList(self):
        for sentence in self.corpus:
            for word in sentence.wordlist:
                for morph in word.morphlist:
                    print morph.str


    def printSentenceList(self):
        for sentence in self.corpus:
            print sentence.form


    def printSentenceWithMorph(self):
        for sentence in self.corpus:
            morphstring = ""
            for word in sentence.wordlist:
                for morph in word.morphlist:
                    morphstring = morphstring + " " + morph.str
            print sentence.gid + "#####!#####" + sentence.form + "#####!#####" + morphstring

#
# main
#
if __name__ == '__main__':
    try:
        command = sys.argv[1]
        filename = sys.argv[2]
    except:
        print >> sys.stderr, __doc__
        exit(1)

    try :
        file = codecs.open(filename, encoding='utf-8')
    except IOError, e:
        print >> sys.stderr, e
        exit(1)

        
    lister = Lister(file)
    sys.stdout = Encode(sys.stdout, 'utf8')

    if command == "words" :
        lister.printWordList()
    elif command == "morphs" :
        lister.printMorphList()
    elif command == "senses":
        lister.printSenseList()
    elif command == "sentences":
        lister.printSentenceList()
    elif command == "h":
        lister.printSentenceWithMorph()
    else:
        print >> sys.stderr, __doc__
        exit(1)

    file.close()
