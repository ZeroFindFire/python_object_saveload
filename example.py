#coding=utf-8
#

import objsave
import frw 
sl=objsave.SaveLoad()
def save_example(obj,filepath):
	global sl
	wt=frw.FileDataWriter()
	wt.open(filepath)
	sl.init()
	#sl.show=True
	sl.save(obj,wt)
	wt.close()

def load_example(filepath):
	global sl
	rd=frw.FileDataReader()
	rd.open(filepath)
	sl.init()
	#sl.show=True
	obj=sl.load(rd)
	rd.close()
	return obj 

class Link(object):
	def __init__(self,key,desc):
		self.key=key 
		self.desc=desc 
	def show(self):
		print "Hello World"

class NoObject:
	def __init__(self,id,name):
		self.id=id 
		self.name=name 

# class that no inherit from object or has specify situation (like numpy.ndarray and ...), should write save&load method itself
# 对于没有继承object或有特殊情况（像numpy.ndarray，没有__dict__，也不能numpy.ndarray__new__(numpy.ndarray)），需要编写自己的save和load方法
def save_no(obj,wt,save):
	wt.puti(obj.id)
	wt.putstring(obj.name)
	pass 
def load_no(rd,load):
	i=rd.geti()
	name=rd.getstring()
	return NoObject(i,name)
sl.regist(NoObject.__module__+"."+NoObject.__name__,save_no,load_no)

a=Link(666,"demo")
a.nxt=Link("z","x")
a.nxt.nxt=a 
a.no=NoObject(123,"name")
a.list=["string",123,123.456,bytearray("bytearray"),a,Link]
a.tuple=tuple(a.list)
a.map={a:a,"a":a,"list":a.list,"tuple":a.tuple,123:123}
a.empty={}
a.el=[]
a.et=()
save_example(a,"save.data")
b=load_example("save.data")
# check by yourself
# like:
"""
import example as exp
a,b=exp.a,exp.b
print a.map[a]
print b.map[b]
...
save_example([1,2,3,"test"],"save.data")
save_example({},"save.data")
...
"""