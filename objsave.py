#coding=utf-8

# for Python2.7

# support format:
# 	base: int, float, bool, string, bytearray, list, tuple, type
# 	object: 1)must inherit from object, 
# 				2)must has parameter __dict__, __class__, 
# 				3)must support ClassName.__new__(ClassName)
# 			1),2),3) all shoult be satisfy
# 		PS: if you write class satisfy 1), then 2),3) will be automatic support
# 	others: numpy.ndarray(just used numpy.save&load)
# unsupport:
# 	module: it's too much data to save as a total module (module.__dict__)
# 	file and so on
# 	to unsupport type, program will save SaveLoadError() instead of that type
# the type of object is store and recognize by type name string, specific codes are in save and load method of class SaveLoad, maybe can consider using integer instead of type name string to save store space
# example are in example.py

# 支持的类型：
# 	基本类型：int, float, bool, string, bytearray, list, tuple, type
# 	对象：需要满足以下3点：
# 			1）继承object
# 			2）有参数__dict__和__class__
# 			3）能够进行 类名.__new__(类名) 来创建空对象
# 		注：如果从object继承，事实上2和3都会满足
# 	其它：numpy.ndarray（实现上直接调用了numpy的save和load方法）
# 不支持：
# 	模块对象和文件对象等等。。。
# 	在实现上模块对象只保存模块名，读取时也只进行__import__(模块名)
# 	对不支持的类型，程序会将其替换成SaveLoadError对象
# 在实现中，类型是以类型名字符串来存储和辨认的，其实现在SaveLoad的save和laod方法中，可以考虑存储数字来代替字符串，节省空间
# 实际使用参考emample.py

import rw
# rw just is a descript, 
# if want write more save&load method for new type, should use io interface that rw have
# normally use can import frw
# rw模块只是io接口的描述
# 想添加对类型的存取支持时，需要使用rw模块描述的io接口
# 实际的应用，可以调用frw模块

class SaveLoadError(object):
	pass 
def combine_cst(dct,ins):
	for key in ins:
		if type(ins[key])!=SaveLoadError:
			execstr= "dct."+str(key)+"=ins[key]"
			#print "cmd:",execstr
			try:
				exec execstr 
			except:
				pass
class SaveLoad:
	Link="knil"
	error="rorre"
	check="kcehc"
	callbacks={}

	# 注册新的类型的读写方法，
	# 读取方法有两个load_cst和load_value，load_cst创建结构，load_value读取实际数据
	# 如果读取的过程中不需要调用SaveLoad().load，可以在load_cst里直接读取实际数据，否则应该在load_value读取实际数据
	# 调用形式为：func_save: func_save(data,wt,save)，参数wt为io接口(写接口)，save为SaveLoad实例的save，该方法返回为空
	# 			load_cst: load_cst(rd,load)，参数rd为io接口(读接口)，load为SaveLoad实例的load，该方法返回读取的对象
	# 			load_value: load_value(obj,rd,load)，obj为load_cst返回的对象，该方法返回为空
	# 后面有实际代码可以参考
	
	# regist save&load method for new type
	# there are tow load method: load_cst and lost_value, load_cst create object,load_value load data for that object
	# if don't need to call SaveLoad().load in the load method of that type, then you can do load data in load_cst, and ignore load_value
	# the input & return format of those method:
	# 	func_save: func_save(data,wt,save)，wt is the io interface object, save is the save method of SaveLoad instance
	# 				return: None
	# 	load_cst: load_cst(rd,load), rd is the io interface object, load is the load method of SaveLoad instance
	# 				return: Object that loaded
	# 	load_value: load_value(obj,rd,load), obj is the object return by load_cst
	# 				return: None
	@staticmethod
	def regist(type,func_save,load_cst,load_value=None):
		if load_value==None:
			load_value=SaveLoad.load_val_empty
		SaveLoad.callbacks[type]=[func_save,load_cst,load_value]

	def init(self):
		self.cnt=0
		self.map={}
		self.objs=[]

	def __init__(self,show=False):
		self.show = show  
		self.init()
		self.regist('type',SaveLoad.save_construct,SaveLoad.load_construct)
		self.regist('function',SaveLoad.save_func,SaveLoad.load_func)
		self.regist('instancemethod',SaveLoad.save_func,SaveLoad.load_func)
		self.regist('dict',SaveLoad.save_dict,SaveLoad.load_dict)
		self.regist('list',SaveLoad.save_list,SaveLoad.load_list)
		self.regist('tuple',SaveLoad.save_list,SaveLoad.load_tuple)
		self.regist('set',SaveLoad.save_list,SaveLoad.load_set)
		self.regist('int',SaveLoad.save_int,SaveLoad.load_int)
		self.regist('NoneType',SaveLoad.save_NoneType,SaveLoad.load_NoneType)
		self.regist('float',SaveLoad.save_float,SaveLoad.load_float)
		self.regist('bool',SaveLoad.save_bool,SaveLoad.load_bool)
		self.regist('str',SaveLoad.save_str,SaveLoad.load_str)
		self.regist('bytearray',SaveLoad.save_btarr,SaveLoad.load_btarr)
		self.regist('module',SaveLoad.save_module,SaveLoad.load_module)
		self.regist('numpy.ndarray',save_np,load_np)

		self.regist('numpy.int8',save_np,load_np)
		self.regist('numpy.int16',save_np,load_np)
		self.regist('numpy.int32',save_np,load_np)
		self.regist('numpy.int64',save_np,load_np)

		self.regist('numpy.uint8',save_np,load_np)
		self.regist('numpy.uint16',save_np,load_np)
		self.regist('numpy.uint32',save_np,load_np)
		self.regist('numpy.uint64',save_np,load_np)

		self.regist('numpy.float16',save_np,load_np)
		self.regist('numpy.float32',save_np,load_np)
		self.regist('numpy.float64',save_np,load_np)

	def save(self,val,wt):
		if self.show:
			print "TRY SAVE:",val 
		tp=type(val).__name__
		md=type(val).__module__
		try:
			if tp=="instance":
				ttp=val.__class__.__name__ 
				tmd=val.__class__.__module__
				if tmd!="__builtin__":
					tktp=tmd+"."+ttp
				else:
					tktp=ttp 
				if self.callbacks.has_key(tktp):
					tp=ttp 
					md=tmd
		except:
			pass 
		if md!="__builtin__":
			tp=md+"."+tp
		i=id(val)
		if self.map.has_key(i):
			if self.show:
				print "save type:"+self.Link,
				print "index:",self.map[i],
				print "type:",tp 
			wt.putstring(self.Link)
			wt.puti(self.map[i])
			return 
		self.map[i]=self.cnt 
		self.cnt+=1
		if self.callbacks.has_key(tp):
			fc_save=self.callbacks[tp][0]
		else:
			fc_save=SaveLoad.save_obj
		wt.putstring(tp)
		if self.show:
			print "save type:"+tp,
			print "index:",self.map[i]
		fc_save(val,wt,self.save)

	def load(self,rd):
		tp=rd.getstring()
		if self.show:
			print "load type:"+tp 
		if tp==self.Link:
			i=rd.geti()
			if self.show:
				print "index:",i 
			return self.objs[i]
		if self.callbacks.has_key(tp):
			fc_load=self.callbacks[tp][1]
			load_value=self.callbacks[tp][2]
		else:
			fc_load=SaveLoad.load_obj
			load_value=SaveLoad.load_obj_value
		index=len(self.objs)
		self.objs.append(None)
		val=fc_load(rd,self.load)
		self.objs[index]=val
		load_value(val,rd,self.load)
		if self.show:
			print "objs length:",len(self.objs)
		return val

	@staticmethod 
	def isobject(obj):
		try:
			obj=obj.__class__
		except:
			pass 
		try:
			while obj!=object:
				obj=obj.__base__ 
		except:
			return False 
		return True 

	@staticmethod
	def load_val_empty(obj,rd,load):
		pass 

	@staticmethod
	def save_obj(obj,wt,save):
		try:
			md=obj.__class__.__module__
			dct=obj.__dict__
			name=obj.__class__.__name__
			__import__(md)
			import sys 
			cmd=sys.modules[md]
			cst=getattr(cmd,name)
			test=cst.__new__(cst)
			if SaveLoad.isobject(obj)==False:
				raise Exception()
		except:
			wt.putstring(SaveLoad.error)
			return  
		try:
			cst_dct=cst.__dict__
		except:
			cst_dct={}
		wt.putstring(SaveLoad.check)
		wt.putstring(md)
		wt.putstring(name)
		#print "save cstdct:",cst_dct
		SaveLoad.save_dict(cst_dct,wt,save)
		SaveLoad.save_dict(dct,wt,save)
		return 

	@staticmethod
	def load_obj(rd,load):
		chk=rd.getstring()
		if chk==SaveLoad.error:
			return SaveLoadError()
		md=rd.getstring()
		name=rd.getstring()
		__import__(md)
		import sys 
		md=sys.modules[md]
		cst=getattr(md,name)
		obj=cst.__new__(cst)
		return obj 
		# obj.__dict__=SaveLoad.load_dict(rd,load)
		# return obj 
	
	@staticmethod
	def load_obj_value(obj,rd,load):
		if type(obj)!=SaveLoadError:
			cst_dict=SaveLoad.load_dict(rd,load)
			#print "load cstdct:",cst_dict
			try:
				#print "BFR load cstdct:",type(obj).__dict__
				combine_cst(type(obj),cst_dict)
				#print "AFT load cstdct:",type(obj).__dict__
			except Exception,e:
				print "ERROR:",e
				pass
			obj.__dict__=SaveLoad.load_dict(rd,load)

	@staticmethod
	def save_construct(cst,wt,save):
		try:
			md=cst.__module__
			name=cst.__name__
			if SaveLoad.isobject(cst)==False:
				raise Exception()
		except:
			wt.putstring(SaveLoad.error)
			return 
		wt.putstring(SaveLoad.check)
		wt.putstring(md)
		wt.putstring(name)
		#print "SAVE:"+md+"."+name
		try:
			cst_dct=cst.__dict__
		except:
			cst_dct={}
		SaveLoad.save_dict(cst_dct,wt,save)
		return  

	@staticmethod
	def load_func(rd,load):
		chk=rd.getstring()
		if chk==SaveLoad.error:
			return SaveLoadError()
		md=rd.getstring()
		class_name = load(rd)
		#class_name=rd.getstring()
		f_object = load(rd)
		name=rd.getstring()
		if f_object is not None:
			cst = getattr(f_object,name)
		else:
			__import__(md)
			import sys 
			md=sys.modules[md]
			try:
				dct = md.__dict__ 
				if class_name == ' ':
					cst=getattr(md,name)
				else:
					cst = getattr(dct[class_name],name)
			except:
				return SaveLoadError()
		cst_dict=SaveLoad.load_dict(rd,load)
		try:
			combine_cst(cst,cst_dict)
		except:
			pass
		return cst 
	@staticmethod
	def save_func(cst,wt,save):
		try:
			md=cst.__module__
			name=cst.__name__
			__import__(md)
			import sys 
			tmd=sys.modules[md]
			dct = tmd.__dict__ 
			class_name = None
			try:
				#print "function:",cst
				f_object = cst.im_self
				#print "f_object:",f_object
			except Exception,e:
				#print "Inner Exception:",e.message
				f_object = None
				if name in dct and getattr(tmd,name) == cst:
					class_name = ' '
				else:
					for k in dct:
						cs = dct[k]
						if type(cs) == type:
							try:
								cdct = cs.__dict__ 
								if name in cdct and getattr(cs,name)==cst:
									class_name = cs.__name__ 
									break
							except:
								pass 
			if SaveLoad.isobject(cst)==False or (class_name is None and f_object is None):
				raise Exception(str(cst)+" is not object")
		except Exception,e:
			#print "Exception:",e.message
			wt.putstring(SaveLoad.error)
			return 
		wt.putstring(SaveLoad.check)
		wt.putstring(md)
		save(class_name, wt)
		save(f_object, wt)
		wt.putstring(name)
		try:
			cst_dct=cst.__dict__
		except:
			cst_dct={}
		SaveLoad.save_dict(cst_dct,wt,save)
		return  

	@staticmethod
	def load_construct(rd,load):
		chk=rd.getstring()
		if chk==SaveLoad.error:
			return SaveLoadError()
		md=rd.getstring()
		name=rd.getstring()
		__import__(md)
		import sys 
		#print "LOAD:"+md+"."+name
		md=sys.modules[md]
		cst=getattr(md,name)
		cst_dict=SaveLoad.load_dict(rd,load)
		try:
			combine_cst(cst,cst_dict)
		except:
			pass
		return cst 
	
	@staticmethod
	def save_dict(dct,wt,save):
		l=len(dct)
		wt.puti(l)
		for key in dct:
			val=dct[key]
			save(val,wt)
			save(key,wt)

	@staticmethod
	def load_dict(rd,load):
		rst={}
		l=rd.geti()
		for i in xrange(l):
			val=load(rd)
			key=load(rd)
			rst[key]=val 
		return rst

	@staticmethod
	def save_list(lst,wt,save):
		l=len(lst)
		wt.puti(l)
		for it in lst:
			save(it,wt)

	@staticmethod
	def load_list(rd,load):
		l=rd.geti()
		rst=[]
		for i in xrange(l):
			rst.append(load(rd))
		return rst 

	@staticmethod
	def load_tuple(rd,load):
		return tuple(SaveLoad.load_list(rd,load))

	@staticmethod
	def load_set(rd,load):
		return set(SaveLoad.load_list(rd,load))

	@staticmethod
	def save_int(val,wt,save):
		wt.puti(val)

	@staticmethod
	def load_int(rd,load):
		return rd.geti()

	@staticmethod
	def save_float(val,wt,save):
		wt.putf(val)

	@staticmethod
	def load_float(rd,load):
		return rd.getf()

	@staticmethod
	def save_bool(val,wt,save):
		wt.putb(val)

	@staticmethod
	def load_bool(rd,load):
		return rd.getb()

	@staticmethod
	def save_NoneType(val,wt,save):
		pass

	@staticmethod
	def load_NoneType(rd,load):
		return None

	@staticmethod
	def save_str(val,wt,save):
		wt.putstring(val)

	@staticmethod
	def load_str(rd,load):
		return rd.getstring()

	@staticmethod
	def save_btarr(val,wt,save):
		wt.putbytearray(val)

	@staticmethod
	def load_btarr(rd,load):
		return rd.getbytearray()

	@staticmethod
	def save_module(val,wt,save):
		name=val.__name__
		wt.putstring(name)
		return  
		# Error: 
		# RuntimeError: dictionary changed size during iteration
		# maybe save something changing while running
		# 实现时发现，如果保存module的__dict__，会报错说dict在变化
		dct=val.__dict__ 
		SaveLoad.save_dict(dct,wt,save)

	@staticmethod
	def load_module(rd,load):
		name=rd.getstring()
		__import__(name)
		import sys 
		md=sys.modules[name]
		return md 
		dct=SaveLoad.load_dict(rd,load)
		rst=md.__dict__
		for k in dct:
			rst[k]=dct[k]
		return md 


# numpy.ndarray的实现估计还需要修改，tmpfile的使用感觉不太好
def save_np(val,wt,save):
	import numpy 
	tmpfile="testsave.tmp.npy"
	numpy.save(tmpfile,val)
	f=open(tmpfile,"rb")
	s=f.read()
	f.close()
	wt.putstring(s)

def load_np(rd,load):
	import numpy 
	s=rd.getstring()
	tmpfile="testload.tmp.npy"
	f=open(tmpfile,"wb")
	f.write(s)
	f.close()
	val=numpy.load(tmpfile)
	return val 