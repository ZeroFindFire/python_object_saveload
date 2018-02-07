#coding=utf-8
#
# just format descript

class DataReader(object):
	def getbts(self,size=-1):return None;
	def getstring(self):return None;
	def getbytearray(self):return None;
	def getf(self):return None;
	def getd(self):return None;
	def geti(self):return None;
	def getb(self):return None;
	def get_arr(self,num,arr,get):
		if arr is None:
			arr=[]
			for i in xrange(num):
				arr.append(0)
		for i in xrange(num):
			arr[i]=get()
		return arr;
	def getfs(self,num,arr=None):
		return self.get_arr(num,arr,self.getf)
	def getds(self,num,arr=None):
		return self.get_arr(num,arr,self.getd)
	def getis(self,num,arr=None):
		return self.get_arr(num,arr,self.geti)

class DataWriter(object):
	def putbts(self,bts):return;
	def putstring(self,str):return;
	def putbytearray(self,str):return;
	def put_arr(self,arr,num,put):
		if num==-1:num=len(arr)
		for i in range(num):
			put(arr[i])
		return arr;
	def putfs(self,arr,num=-1):
		self.put_arr(arr,num,self.putf)
	def putds(self,arr,num=-1):
		self.put_arr(arr,num,self.putd)
	def putis(self,arr,num=-1):
		self.put_arr(arr,num,self.puti)
	def putf(self,dt):return None;
	def putd(self,dt):return None;
	def puti(self,dt):return None;
	def putb(self,dt):return None;
