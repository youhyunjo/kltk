# -*- coding: utf-8 -*-
# Sejong Morphology Tagged Corpus
# $Id$

""" 
Sejong Morphology Tagged Corpus Reader.

@status: Not yet fully implemented
"""


class Word:
	""" 
	Word class for Sejong Parsed Corpus.

	Word class has 4 attributes:
	 - ord is the order in the sentence
	 - form is the orthographical form
	 - morphs is an array of Morph instances
	 - morph_string is the morphology string in the corpus
	   for example, "보/VX + 는데/EC"
	"""
	def __init__(self, ord, form, morphs, morph_string):
		"""
		@param ord: order in the sentence
		@type ord: int
		@param form: word form
		@type form: string
		@param morphs: list of morphs
		@type morphs: list of L{Morph}s
		@param morph_string: raw morphology string
		@type morph_string: string
		"""
		self.ord = ord
		self.form = form
		self.morphs = morphs
		self.morph_string = morph_string
	
	def add_morph(self, morph):
		"""
		@param morph: a morpheme
		@type morph: L{Morph}
		"""
		self.morphs.append(morph)

	def has_pos(self, pos):
		"""
		@param pos: part of speech tag 
		@type pos: string
		@rtype: boolean
		"""
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
	"""
	Morph
	"""
	def __init__(self, form, pos):
		"""
		@param form: morphology form
		@type form: string
		@param pos: part of speech tag
		@type pos: string
		"""
		self.form = form
		self.pos = pos



