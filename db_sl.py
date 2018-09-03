#coding=utf-8

#for python 2.7 
class Unpack(object):
	def work_list(self, index):
		if index in self.works:
			return self.works[index]
		tmp = self.objs[index]
		rst = []
		self.works[index] = rst 
		for key in tmp:
			obj = self.work(key)
			rst.append(obj)
		rst = self.types[index](rst)
		self.works[index] = rst 
		return rst
	def work_dict(self, index):
		if index in self.works:
			return self.works[index]
		tmp = self.objs[index]
		rst = {}
		self.works[index] = rst
		for key_id in tmp:
			obj_id = tmp[key_id]
			key = self.work(key_id)
			obj = self.work(obj_id)
			rst[key] = obj 
		return rst 
	def work_unit(self, index):
		return self.objs[index]
	def work(self, index):
		if self.types[index] in [list, set, tuple]:
			return self.work_list(index)
		elif self.types[index] in [dict]:
			return self.work_dict(index)
		else:
			return self.work_unit(index)
	def __call__(self, obj_types):
		self.objs = obj_types[0] 
		self.types = obj_types[1] 
		self.works = {}
		return self.work(0)
def unpack(obj_types):
	return Unpack()(obj_types)
		
class Pack(object):
	def work_list(self, obj):
		addr = id(obj)
		if addr in self.links:
			return self.links[addr]
		rst = len(self.objs)
		tmp = []
		self.links[addr] = rst
		self.objs.append(tmp)
		self.types.append(type(obj))
		for it in obj:
			it_id = self.work(it)
			tmp.append(it_id)
		return rst 
	def work_dict(self, obj):
		addr = id(obj)
		if addr in self.links:
			return self.links[addr]
		rst = len(self.objs)
		tmp = {}
		self.objs.append(tmp)
		self.types.append(type(obj))
		self.links[addr] = rst
		for key in obj:
			key_id = self.work(key)
			obj_id = self.work(obj[key])
			tmp[key_id] = obj_id 
		return rst 
	def work_unit(self, obj):
		if obj in self.val_links:
			return self.val_links[obj]
		rst = len(self.objs)
		self.types.append(type(obj))
		self.objs.append(obj)
		self.val_links[obj] = rst 
		return rst 
	def work(self, obj):
		if type(obj) in [set, list, tuple]:
			rst = self.work_list(obj)
		elif type(obj) in [dict]:
			rst = self.work_dict(obj)
		else:
			rst = self.work_unit(obj)
		return rst 
	def __call__(self, obj):
		self.val_links = {}
		self.links = {}
		self.objs = []
		self.types = []
		self.work(obj)
		return [self.objs, self.types]
def pack(obj):
	return Pack()(obj)
unit_maps = {
float:">d"
}
def dumps_ot(obj_types):
	objs, types = obj_types 
	stypes = []
	import struct
	import json 
	for tp in types:
		stype = [tp.__module__,tp.__name__]
		stypes.append(stype)
	sobjs = []
	for obj in objs:
		if type(obj) in unit_maps:
			sobj = struct.pack(unit_maps[type(obj)],obj)
		else:
			sobj = json.dumps(obj)
		sobjs.append(sobj)
	stypes = json.dumps(stypes)
	s = struct.pack(">i", len(sobjs))
	for sobj in sobjs:
		s+=struct.pack(">i",len(sobj))
		s+= sobj 
	return s + stypes 
	return json.dumps([sobjs,stypes])

def loads_ot(s):
	import json
	import struct
	l, = struct.unpack(">i",s[:4])
	s = s[4:] 
	sobjs = []
	for i in xrange(l):
		sz, = struct.unpack(">i", s[:4])
		s = s[4:]
		sobj = s[:sz]
		s = s[sz:]
		sobjs.append(sobj)
	stypes = json.loads(s)
	types = []
	import sys 
	for stype in stypes:
		smd, sname = stype
		__import__(smd)
		cmd=sys.modules[smd]
		cst=getattr(cmd,sname)
		types.append(cst)
	objs = []
	for tp, sobj in zip(types, sobjs):
		if tp in unit_maps:
			obj, = struct.unpack(unit_maps[tp], sobj)
		else:
			obj = json.loads(sobj)
		if type(obj) in [dict]:
			tmp = {}
			for key in obj:
				int_key =int(key)
				int_obj = int(obj[key])
				tmp[int_key] = int_obj 
			obj = tmp 
		objs.append(obj)
	return [objs, types]

def dumps(obj):
	obj_type = pack(obj)
	return dumps_ot(obj_type)
def loads(s):
	obj_type = loads_ot(s)
	return unpack(obj_type)
"""

demo:

database.user.add(name=name, pwd=pwd, urls=[url0, url1, ...])
database.user.add("format", *attrs)
database.user.format("").add(*attrs).add(*attrs)...
id = database.urls.add(url)
database.user.urls.add(id)
id = database.company.find("name = zxc")
database.user.company = id 
host = database.urls.add(url)
id = database.urls.add_if_not_find(url)

host.out_urls.add(id)

...

lnks
objs



find users visited urlx 

rst = [user for user in database.user if url in user.urls]




"""


"""
maps={}
TYPE_MAP = 0
TYPE_LIST = 1 
TYPE_STRING = 2 
TYPE_INT = 3 
def obj_type(obj):
	pass 
maps.user = []
class regist(object):
	def __init__(self):
		self.ids = {}
	def regist(self, obj):
		addr = id(obj)
		self.ids[addr] = obj  
	def registed(self, obj):
		addr = id(obj)
		if addr in self.ids:
			return True 
		return False
class table(object):
	regists = regist()
	def __init__(self):
		self.__map = {}
		self.__list = []
		self.__index = 0
	def __setattr__(self, key, value):
		#addr = id(value)
		#table.regists[addr] = value
		self.__map[key] = value 
	def __getattr__(self, key):
		if key not in self.__map:
			tmp = table()
			#addr = id(tmp)
			#table.regists[addr] = tmp
			self.__map[key] = tmp
		return self.__map[key]
	def set(self, key, value):
		
		addr = id(value)
		self.__map[key] = id
	def __iter__(self):
		pass 
	def add(self, *attrs, **maps):
		for i in xrange(len(attrs)):
			maps[i] = attrs[i]
		tmp = table()
		self.__map[self.__index] = maps 
		
		self.__index += 1
		pass 
	
def set(key, value):
	if obj_type(value) == TYPE_MAP:
		if not find_obj(value):
			create_map(rand_key)
			for k in value:
				set_map(k,value[k])
		pass 
	maps[key] = value 
	pass 

def unset(key):
	del maps[key]
	pass 

def add_list(key, value):
	pass 

def create_list(key):
	pass 

def delete_list(key):
	pass 

def create_map(key):
	pass 

def delete_map(key):
	pass 

"""