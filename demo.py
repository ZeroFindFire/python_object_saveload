#coding=utf-8
#

import objsave
import frw 
sl=objsave.SaveLoad()
def save(obj,filepath,show = False):
	global sl
	wt=frw.FileDataWriter()
	wt.open(filepath)
	sl.init()
	sl.show=show
	sl.save(obj,wt)
	wt.close()

def load(filepath,show = False):
	global sl
	rd=frw.FileDataReader()
	rd.open(filepath)
	sl.init()
	sl.show=show
	obj=sl.load(rd)
	rd.close()
	return obj 


def combine(dct,ins):
	if type(dct)==type("str"):
		import sys
		dct=sys.modules[dct].__dict__
	for key in ins:
		dct[key]=ins[key]
