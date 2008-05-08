#-*- coding: utf-8; tab-width: 4 -*-
# Sejong Sense Tagged Corpus
# $Id$
"""Sejong Sense Tagged Corpus

The Sejong sense tagged corpus consists of records:
    word + sense tag + pos tag

for example:

2BT_0010000010  1.          1/SN + ./SF
2BT_0010000020  아름다운      아름답/VA + ㄴ/ETM
2BT_0010000030  그          그/MM
2BT_0010000040  시작        시작_01/NNG

A record has 3 columns:

    1st column : corpus-wide global index
    2nd column : orthographical form
    3rd column : list of morphemes

A list of morphemes:

    morpheme_semtag/postag + ... 


Structure:

    Corpus
        Sentence[]
            gid = the gid of the first word
            form
            Word[]
                gid = global index
                ord = order in the sentence
                form
                Morph[]
                    form
                    sem
                    pos


Ussage:

    file = codecs.open(filename, encodeing='utf-8')
    corpus = Corpus(file)

    corpus.readsentence()

    for sentence in corpus:
        print sentence
"""
import re

class Word:
    """A word in a sentence
        gid : global index
        ord : order in the sentence
        form
        Morph[]
        ord: order in the word
            form
            pos
    """
    def __init__(self, gid, ord, form, morphlist_raw_str):
        self.gid = gid
        self.ord = ord
        self.form = form
        self.morphlist_raw_str = morphlist_raw_str

        self.morphlist =  []
        
        for morph_raw_str in morphlist_raw_str.split(' + '):
            self.morphlist.append(Morph(morph_raw_str.replace(" ", "")))
    def str__(self):
        return self.form
    def encode(self, enc):
        return self.form.encode(enc)
    def has(self, str):
        s = re.compile(".*"+str+".*")
        return s.match(self.morphlist_raw_str)


class Morph:
    """A morpheme with a pos tag

    str  : raw string
    ord  : order in the word
    form :
    pos  :
	sem  : 00 for non-specified
    """
    def __init__(self, morph_str):  
        self.str = morph_str
        if(morph_str == "//SP"):
            self.form = "/"
            self.pos = "SP"
			self.sem = "00"
        else:
            temp = morph_str.split('/')
            if len(temp) == 2:
                (form_sem, self.pos) = temp
                try:
                    (self.form, self.sem) = form_sem.split('__')
                except ValueError:
                    (self.form, self.sem) = (form_sem, '00')
            else:
                self.form = morph_str
                self.pos = 'SOURCE_ERROR'
				self.sem = '00'

class Sentence:
    def __init__(self, first_word):
        self.wordlist = [first_word]
        self.idx = 0

        self.form = first_word.form
        self.gid = first_word.gid

    def append(self, word):
        self.wordlist.append(word)
        self.form = self.form + u" " + word.form

    def str__(self):
        return self.str

    def encode(self, enc):
        return self.str.encode(enc)

    def __iter__(self):
        return self

    def next(self):
        if self.idx >= len(self.wordlist):
            raise StopIteration
        word = self.wordlist[self.idx]
        self.idx += 1
        return word
                



SF = re.compile('.*[/]SF.*')        
TEXT_LINE = re.compile("^9BS.*")

class Corpus:
    """Sejong Sense Tagged Corpus
    """
    def __init__(self, file):
        self.file = file

    def __iter__(self):
        return self

    def readline(self):
		line = self.file.readline()

		# immediately exits the program when EOF is encountered
		if (line == "") : exit(0)

		if TEXT_LINE.match(line) :
			try:
				(gid, form, morph_arr) = line.strip().split('\t')
			except UnicodeDecodeError:
				(gid, form, morph_arr) = ('NULL', 'UnicodeDecodeError', 'NULL')
			except ValueError:
				(gid, form, morph_arr) = ('NULL', line, 'NULL')
			return (gid, form, morph_arr)
		else :
			# ignores current line and processes next line
			return self.readline()	
				  
    def readsentence(self):

        # read first word
        ord = 1
        line = self.readline()
        (gid, form, morph_arr) = line
        first_word = Word(gid, ord, form, morph_arr)
        curr_sentence = Sentence(first_word)

        # read following words
        while((not SF.match(morph_arr)) and line):
            ord = ord + 1
            line = self.readline()
            (gid, form, morph_arr) = line
            curr_sentence.append(Word(gid, ord, form, morph_arr))

        return curr_sentence

    def next(self):
        return self.readsentence()
 





#
# TEST
#
import codecs
import sys

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
            print "======================"
            print sentence.gid, sentence.form
            for word in sentence.wordlist:
                print word.ord, word.form
                for morph in word.morphlist:
                    print '\t', morph.form, morph.sem, morph.pos


if __name__ == '__main__':
    file = codecs.open(sys.argv[1], encoding='utf-8')
    Test(file)
    file.close()

