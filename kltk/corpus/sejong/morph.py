# -*- coding: utf-8 -*-
# Sejong Morphology Tagged Corpus
# $Id$

""" Sejong Morphology Tagged Corpus
"""


""" Word class for Sejong Parsed Corpus

Word class has 4 attributes:
 - ord is the order in the sentence
 - form is the orthographical form
 - morphs is an array of Morph instances
 - morph_string is the morphology string in the corpus
   for example, "보/VX + 는데/EC"
"""
class Word:
	def __init__(self, ord, form, morphs, morph_string):
		self.ord = ord
		self.form = form
		self.morphs = morphs
		self.morph_string = morph_string
	
	def add_morph(self, morph):
		self.morphs.append(morph)

	def has_pos(self, pos):
		for m in self.morphs:
			if m.pos == pos :
				return True
		return False

	def __str__(self):
		str = ""
		for m in self.morphs:
			if str == "":
				str = m.form
			elif m.pos[0] == "S" :
				str += m.form
			else :
				str += "-" + m.form
		return str
		#return reduce(lambda x,y: x.form+"-"+y.form, self.morphs)


class Morph:
	def __init__(self, form, pos):
		self.form = form
		self.pos = pos



