#coding=utf-8
#

import objsave
import frw 
sl=objsave.SaveLoad()
def save(obj,filepath):
	global sl
	wt=frw.FileDataWriter()
	wt.open(filepath)
	sl.init()
	#sl.show=True
	sl.save(obj,wt)
	wt.close()

def load(filepath):
	global sl
	rd=frw.FileDataReader()
	rd.open(filepath)
	sl.init()
	#sl.show=True
	obj=sl.load(rd)
	rd.close()
	return obj 


def combine(dct,ins):
	if type(dct)==type("str"):
		import sys
		dct=sys.modules[dct].__dict__
	for key in ins:
		dct[key]=ins[key]
