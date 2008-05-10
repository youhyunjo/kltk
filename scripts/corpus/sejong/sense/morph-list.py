#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4 -*-
# $Id$

#
# TEST
#
import codecs
import sys
from kltk.corpus.sejong.sense import Corpus

class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))

class Test:
    def __init__(self, file):
        corpus = Corpus(file)
        self.test(corpus, 'utf8')


    def test_full(self, corpus, enc):
        sys.stdout = Encode(sys.stdout, enc)
        for sentence in corpus:
            print "======================"
            print sentence, sentence.form
            for word in sentence.wordlist:
                print word, word.gid, word, word.form
                for morph in word.morphlist:
                    print morph, morph.form, morph.pos


    def test(self, corpus, enc):
        sys.stdout = Encode(sys.stdout, enc)
        for sentence in corpus:
            #print "======================"
            #print sentence.gid, sentence.form
            for word in sentence.wordlist:
                #print word.ord, word.form
                for morph in word.morphlist:
                    print morph.form, morph.sem, morph.pos


if __name__ == '__main__':
    file = codecs.open(sys.argv[1], encoding='utf-8')
    Test(file)
    file.close()

