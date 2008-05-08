#!/usr/bin/python 
#-*- coding: utf-8 -*-
import codecs
import sys

list = codecs.open(sys.argv[1], encoding='utf-8')
freqfile = codecs.open('ec-freq.list', encoding='utf-8')


class Encode:
    def __init__(self, stdout, enc):
        self.stdout = stdout
        self.encoding = enc
    def write(self, s):
        self.stdout.write(s.encode(self.encoding))

sys.stdout = Encode(sys.stdout, 'utf-8')




class Relation:
	def __init__(self, dep, gov, freq):
		self.dep = dep
		self.gov = gov
		self.freq = freq
		if self.gov == self.dep :
			self.reflexive = True
		else :
			self.reflexive = False

		self.number_of_connections = 0


class Emi :
	def __init__(self, form):
		self.form = form
		self.deps = []
		self.govs = []

class Lexicon:
	def __init__(self):
		self.emis = []
	
	def append(self, emi):
		self.emis.append(emi)
	
	def has_emi(self, emi_form):
		for e in self.emis:
			if e.form == emi_form:
				return True
		return False
	
	def get_emi(self, emi_form):
		for e in self.emis:
			if e.form == emi_form:
				return e
		return None
			

freq = []
for line in freqfile:
	(f, ec) = line.strip().split()
	if int(f) > 1000: # and int(f) < 10000 :
		form, pos = ec.split("/")
		freq.append(form.strip())


#freq = [u"고", u"아", u"어", u"지", u"게", u"아서", u"어서", u"니까", u"으니까"]
# freq = [u"아서", u"어서", u"니까", u"으니까", u"면서", u"으면서", u"지만", 
# u"는데", u"ㄴ데", u"은데", u"아도", u"어도", u"며", u"으며", u"면서", u"으면서", 
# u"면", u"으면"]
# 
rel = {} 
emiset = set() 
for pair in list:
	fields = pair.strip().split("\t")
	if len(fields) == 5:
		(freq1, pair1, sharp, freq2, pair2) = fields
		(temp1, temp2) = pair1.split("<")
		if len(temp1.split()) + len(temp2.split()) > 2: continue
		e1 = temp1.strip()[1:]
		e2 = temp2.strip()[1:]
		if e1 in freq and e2 in freq:
			emiset.add(e1)
			emiset.add(e2)
			rel[e1,e2] = True
	elif len(fields) == 2  :
		(freq, pair)  = fields
		(temp1, temp2) = pair.split("<")
		if len(temp1.split()) + len(temp2.split()) > 2: continue
		e1 = temp1.strip()[1:]
		e2 = temp2.strip()[1:]
		if True or (e1 in freq and e2 in freq) :
			emiset.add(e1)
			emiset.add(e2)
			rel[e1,e2] = True

emis = [ x for x in emiset]



def method1():
	print "digraph EMI {"

	for e1 in emis:
		for e2 in emis:
			if not rel.has_key((e1,e2)) : continue
			for k in emis:
				if k != e1 and k != e2  \
				 and rel.has_key((e1,k)) and rel[e1,k]\
				 and rel.has_key((k,e2)) and rel[k,e2] :
					rel[e1,e2] = False
					break
			if rel.has_key((e1,e2)) and rel[e1,e2] and e1 != e2:
				print "\t", e1, "->", e2, ";"
		

	print "}"


def method2():
	print "digraph EMI {"

	for e1 in emis:
		for e2 in emis:
			if not rel.has_key((e1,e2)) : continue
			flag = False
			for k in emis:
				if k != e1 and k != e2 and rel.has_key((e1,k)) and rel.has_key((k,e2)) :
					flag = True
					break
			if rel.has_key((e1,e2)) and (not flag) and e1 != e2:
				print "\t", e1, "->", e2, ";"
		

	print "}"







method2()






# emipairs = []
# emidic = Lexicon()
# for pair in list:
# 	fields = pair.strip().split()
# 	if len(fields) == 4 :
# 		emipairs.append(Relation(fields[1][1:], fields[3][1:], int(fields[0]))) 
# 
# 		e1 = emidic.get_emi(fields[1][1:])
# 		if not e1 :
# 			e1 = Emi(fields[1][1:])
# 			emidic.append(e1)
# 			
# 		e2 = emidic.get_emi(fields[3][1:])
# 		if not e2:
# 			e2 = Emi(fields[3][1:])
# 			emidic.append(e2)
# 		
# 		e1.govs.append(e2)
# 		e2.deps.append(e1)
# 	
# freq = []
# for line in freqfile:
# 	(f, ec) = line.strip().split()
# 	if int(f) > 200 and int(f) < 10000 :
# 		form, pos = ec.split("/")
# 		freq.append(form)
# 
# 
# 
# 
# emipair = emipairs.pop()
# while(emipairs) :
# 	emipair = emipairs.pop()
# 
# 	group = [emipair]
# 	for ep in emipairs:
# 		if ep.dep == emipair.dep:
# 			group.append(ep)
# 			emipairs.remove(ep)
# 
# 	link_govs = []
# 	for second_pair in emipairs:
# 		if emipair.gov == second_pair.dep:
# 			link_govs.append(second_pair.gov)
# 	
# 	for second_pair in emipairs:
# 		if second_pair.dep in link_govs:
# 			link_govs.append(second_pair.gov)
# 
# 	for second_pair in emipairs:
# 		if second_pair.dep in link_govs:
# 			link_govs.append(second_pair.gov)
# 
# 	for friend in group:
# 		if friend.gov in link_govs:
# 			#print "HAS LINK: ", friend.dep, friend.gov
# 			pass
# 		else :
# 			if friend.dep in freq and friend.gov in freq:
# 				print friend.dep, "->", friend.gov, ";"
# 
# 
# 
# 
# 
# 
# 
# 









#no_dep = [x.form for x in emidic.emis if not x.deps and x.govs]
#no_gov = [x.form for x in emidic.emis if not x.govs and x.deps]
#
#




# for emipair in emipairs:
# 	if emipair.dep in no_dep :
# 		print "no_dep:", emipair.dep, emipair.gov, emipair.freq
# 	elif emipair.gov in no_gov:
# 		print "no_gov:", emipair.dep, emipair.gov, emipair.freq
# 	else:
# 		print emipair.freq, "-" + emipair.dep, "<" ,"-" + emipair.gov
# 
# 




# for e in middle:
# 	for dep in e.deps:
# 		try :
# 			no_dep.index(dep)
# 		except :
# 			print dep.form, e.form
# 	for gov in e.govs:
# 		try :
# 			no_gov.index(gov)
# 		except :
# 			print e.form, gov.form
# 
# 
#  
