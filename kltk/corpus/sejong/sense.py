#-*- coding: utf-8; tab-width: 4 -*-
# Sejong Morphology Sense Tagged Corpus Reader
# $Id$

"""
Sejong Morphology Sense Tagged Corpus Reader.

corpus sample::

    2BT_0010000010  1.          1/SN + ./SF
    2BT_0010000020  아름다운      아름답/VA + ㄴ/ETM
    2BT_0010000030  그          그/MM
    2BT_0010000040  시작        시작_01/NNG

A record has 3 columns:

    - 1st column : corpus-wide global index
    - 2nd column : orthographical form
    - 3rd column : list of morphemes

A list of morphemes:

    - morpheme_semtag/postag + ... 


Usage
=====

example::

    file = codecs.open(filename, encodeing='utf-8')
    corpus = Corpus(file)

    corpus.readsentence()

    for sentence in corpus:
        print sentence



Structure
=========

::

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

"""
#__docformat__ = 'restructuredtext'


import re

class Word:
    """
    A word in a sentence.
    """
    def __init__(self, gid, ord, form, morph_string):
        self.gid = gid
        """
        @type: string
        """
        self.ord = ord
        """
        @type: int
        """
        self.form = form
        """
        @type: string
        """
        self.morph_string = morph_string
        """
        @type: string
        """

        self.morphlist =  []
        """
        @type: list of L{Morph}
        """
        
        for morph_raw_str in morph_string.split(' + '):
            self.morphlist.append(Morph(morph_raw_str.replace(" ", "")))

    def str__(self):
        return self.form
    def encode(self, enc):
        return self.form.encode(enc)
    def has(self, str):
        s = re.compile(".*"+str+".*")
        return s.match(self.morph_string)

    
class Morph: 
   """
   Morphology: a morpheme with a sense tag and a pos tag.

   -str  : raw string
   -ord  : order in the word
   -form :
   -pos  :
   -sem  : 00 for non-specified
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
                






class Corpus:
    """Sejong Sense Tagged Corpus.
    """

    def __init__(self, file):
        self.file = file

    def __iter__(self):
        return self

    def _readline(self):
        line = self.file.readline()

        # raise StopIteration when EOF is encountered
        if (line == "") : 
            raise StopIteration

        TEXT_LINE = re.compile("^9BS.*")
        if TEXT_LINE.match(line) :
            try:
                (gid, form, morph_string) = line.strip().split('\t')
            except UnicodeDecodeError:
                (gid, form, morph_string) = ('NULL', 'UnicodeDecodeError', 'NULL')
            except ValueError:
                (gid, form, morph_string) = ('NULL', line, 'NULL')
            return (gid, form, morph_string)
        else :
            # ignores current line and processes next line
            #return self._readline() 
            return line
                  
    def readsentence(self):

        # read first word
        ord = 1

        line = self._readline()
        while len(line) != 3 :
            line = self._readline()
        (gid, form, morph_string) = line

        first_word = Word(gid, ord, form, morph_string)
        curr_sentence = Sentence(first_word)

        # read following words
        SF = re.compile(u'.*[/]SF( \+ [\'"」]/SS)?$')        
        while((not SF.match(morph_string)) and line):
            ord = ord + 1
            line = self._readline()
            try:
                (gid, form, morph_string) = line
                curr_sentence.append(Word(gid, ord, form, morph_string))
            except:
                return curr_sentence


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

