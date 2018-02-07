# python_object_saveload

# for Python2.7

# example are in example.py
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

# ʵ��ʹ�òο�emample.py
# ֧�ֵ����ͣ�
# 	�������ͣ�int, float, bool, string, bytearray, list, tuple, type
# 	������Ҫ��������3�㣺
# 			1���̳�object
# 			2���в���__dict__��__class__
# 			3���ܹ����� ����.__new__(����) �������ն���
# 		ע�������object�̳У���ʵ��2��3��������
# 	������numpy.ndarray��ʵ����ֱ�ӵ�����numpy��save��load������
# ��֧�֣�
# 	ģ�������ļ�����ȵȡ�����
# 	��ʵ����ģ�����ֻ����ģ��������ȡʱҲֻ����__import__(ģ����)
# 	�Բ�֧�ֵ����ͣ�����Ὣ���滻��SaveLoadError����
# ��ʵ���У����������������ַ������洢�ͱ��ϵģ���ʵ����SaveLoad��save��laod�����У����Կ��Ǵ洢�����������ַ�������ʡ�ռ�


# objsave is the main module
# rw just is a descript, 
# if want write more save&load method for new type, should use io interface that rw have
# normally use can import frw

# ��ģ��Ϊobjsave
# rwģ��ֻ��io�ӿڵ�����
# ����Ӷ����͵Ĵ�ȡ֧��ʱ����Ҫʹ��rwģ��������io�ӿ�
# ʵ�ʵ�Ӧ�ã����Ե���frwģ��

# you can add save&load method for new type by yourself, call SaveLoad.regist:
# 	@staticmethod
# 	def regist(type,func_save,load_cst,load_value=None)
# regist save&load method for new type
# there are tow load method: load_cst and lost_value, load_cst create object,load_value load data for that object
# if don't need to call SaveLoad().load in the load method of that type, then you can do load data in load_cst, and ignore load_value
# the input & return format of those method:
# 	func_save: func_save(data,wt,save)��wt is the io interface object, save is the save method of SaveLoad instance
# 				return: None
# 	load_cst: load_cst(rd,load), rd is the io interface object, load is the load method of SaveLoad instance
# 				return: Object that loaded
# 	load_value: load_value(obj,rd,load), obj is the object return by load_cst
# 				return: None

# ����������������Ͷ����save��load��������Ҫ����SaveLoad.regist:
# 	@staticmethod
# 	def regist(type,func_save,load_cst,load_value=None)
# ע���µ����͵Ķ�д������
# ��ȡ����������load_cst��load_value��load_cst�����ṹ��load_value��ȡʵ������
# �����ȡ�Ĺ����в���Ҫ����SaveLoad().load��������load_cst��ֱ�Ӷ�ȡʵ�����ݣ�����Ӧ����load_value��ȡʵ������
# ������ʽΪ��func_save: func_save(data,wt,save)������wtΪio�ӿ�(д�ӿ�)��saveΪSaveLoadʵ����save���÷�������Ϊ��
# 			load_cst: load_cst(rd,load)������rdΪio�ӿ�(���ӿ�)��loadΪSaveLoadʵ����load���÷������ض�ȡ�Ķ���
# 			load_value: load_value(obj,rd,load)��objΪload_cst���صĶ��󣬸÷�������Ϊ��
# objsave.py������ʵ�ʴ�����Բο�