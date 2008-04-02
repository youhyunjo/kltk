# -*- coding: utf8 -*-
# Normalize allomophs
# $Id$
"""
Normalize variants form of a morpheme 
  eg) 아/EC, 어/EC -> 어/EC
"""

class Allomorph :
	def __init__(self):
		self.normalized = { "아/EC" : "어/EC",
				"아서/EC" : "어서/EC",
				"아도/EC" : "어도/EC",
				"으면/EC" : "면/EC",
				"으며/EC" : "며/EC",
				"으니까/EC" : "니까/EC",
				"아야/EC" : "어야/EC",
				"으니/EC" : "니/EC",
				"은지/EC" : "ㄴ지/EC",
				"는지/EC" : "ㄴ지/EC",
				"으러/EC" : "러/EC",
				"으려고/EC" : "려고/EC",
				"은데/EC" : "ㄴ데/EC",
				"는데/EC" : "ㄴ데/EC",
			}

	def normalize(self, variant):
		if self.normalized.has_key(variant):
			return self.normalized[variant]
		else :
			return variant
	
	def print_list(self):
		for allo in self.normalized:
			print allo, self.normalize(allo)
	


# test
if __name__ == '__main__':
	allomorph = Allomorph()
	allomorph.print_list()

