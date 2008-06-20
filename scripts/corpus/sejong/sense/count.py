#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4 -*-
# count.py

"""
count for Sejong Morphology Sense Tagged Corpus

$ count wordlist sejong-sense.txt > words.list
$ count morphlist sejong-sense.txt > morphs.list
$ count senselist sejong-sense.txt > senses.list

$ count sentencelist sejong-sense.txt > sentences.list
$ count clauselist sejong-sense.txt > clauses.list

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
        self.word_token_count = 0
        self.word_type_count = 0
        self.morph_token_count = 0
        self.morph_type_count = 0
        self.sense_token_count = 0
        self.sense_type_count = 0
        self.word_freq_table = {}
        #self._count()

    def printWordFrequencyTable(self):
        for sentence in self.corpus:
            for word in sentence.wordlist:
                self.word_freq_table[word.form] = self.word_freq_table.get(word.form,0) + 1
        
        wf_list = self.word_freq_table.items()
        wf_list.sort(lambda x,y: y[1] - x[1])
        for w in wf_list:
            print w[0], w[1]


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

    def _count(self):
        wordfreq_map = {}
        morphfreq = {}
        for sentence in self.corpus:
            for word in sentence.wordlist:
                self.word_token_count = self.word_token_count + 1
                wordfreq_map[word.form] = wordfreq_map.get(word.form,0)+1
                for morph in word.morphlist:
                    self.morph_token_count = self.morph_token_count + 1
                    morphfreq[morph.form+morph.sem] = morphfreq.get(morph.form+morph.sem,0)+1

        self.word_type_count = len(wordfreq_map)
        self.morph_type_count = len(morphfreq)

    def print_word_count(self):
        print "word count"
        print "token", "type"
        print self.word_token_count, self.word_type_count

    def print_morph_count(self):
        print "morph count"
        print "token", "type"
        print self.morph_token_count, self.morph_type_count

        

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

    try:
        command = sys.argv[1]
        file = codecs.open(sys.argv[2], encoding='utf-8')
        sys.stdout = Encode(sys.stdout, 'utf8')
        counter = SejongSenseCounter(file)
    except:
        print __doc__
        exit(1)

    if command == "wordlist" :
        counter.printWordList()
    elif command == "morphlist" :
        counter.printMorphList()
    elif command == "senselist":
        counter.printSenseList()
    elif command == "sentencelist":
        counter.printSentenceList()
    else:
        print __doc__

    file.close()

