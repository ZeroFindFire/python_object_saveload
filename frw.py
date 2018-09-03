#coding=utf-8
#
from rw import DataReader,DataWriter

import struct
class FileDataReader(DataReader):
	def __init__(self,fp=None):
		self.fp=fp
	def getbts(self,size=-1):
		if size<0:
			return self.fp.read()
		else:
			return self.fp.read(size)
	def getbytearray(self):
		s=self.getstring()
		return bytearray(s)
	def getstring(self):
		sz=self.geti()
		out=self.fp.read(sz);
		return out
	def open(self,filename):
		self.fp=open(filename,'rb');
	def close(self):
		self.fp.close()
	def getf(self):
		return self.getd()
		num,=struct.unpack('>f',self.fp.read(4))
		return num;
	def getd(self):
		num,=struct.unpack('>d',self.fp.read(8))
		return num;
	def geti(self):
		num,=struct.unpack('>i',self.fp.read(4))
		return num;
	def getb(self):
		num,=struct.unpack('>?',self.fp.read(1))
		return num;
class FileDataWriter(DataWriter):
	def __init__(self,fp=None):
		self.fp=fp
	def putbts(self,bts):
		self.fp.write(bts)
	def putbytearray(self,bts):
		self.putstring(str(bts))
	def putstring(self,str):
		sz=len(str)
		self.puti(sz)
		self.fp.write(str)
	def open(self,filename):
		self.fp=open(filename,'wb');
	def close(self):
		self.fp.close()
	def putf(self,dt):
		return self.putd(dt)
		self.fp.write(struct.pack('>f',dt))
	def putd(self,dt):
		self.fp.write(struct.pack('>d',dt))
	def puti(self,dt):
		self.fp.write(struct.pack('>i',dt))
	def putb(self,dt):
		self.fp.write(struct.pack('>?',dt))

