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
$ list clauses sejong-sense.txt > clauses.list

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


class SejongSenseCounter:
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

if __name__ == '__main__':
    try:
        command = sys.argv[1]
        file = codecs.open(sys.argv[2], encoding='utf-8')

        counter = SejongSenseCounter(file)
    except:
        print __doc__
        exit(1)

    sys.stdout = Encode(sys.stdout, 'utf8')

    if command == "words" :
        counter.printWordList()
    elif command == "morphs" :
        counter.printMorphList()
    elif command == "senses":
        counter.printSenseList()
    elif command == "sentences":
            counter.printSentenceList()
    else:
        print __doc__
        exit(1)

    file.close()
