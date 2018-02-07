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

# 实际使用参考emample.py
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


# objsave is the main module
# rw just is a descript, 
# if want write more save&load method for new type, should use io interface that rw have
# normally use can import frw

# 主模块为objsave
# rw模块只是io接口的描述
# 想添加对类型的存取支持时，需要使用rw模块描述的io接口
# 实际的应用，可以调用frw模块

# you can add save&load method for new type by yourself, call SaveLoad.regist:
# 	@staticmethod
# 	def regist(type,func_save,load_cst,load_value=None)
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

# 可以再添加其它类型对象的save和load方法，需要调用SaveLoad.regist:
# 	@staticmethod
# 	def regist(type,func_save,load_cst,load_value=None)
# 注册新的类型的读写方法，
# 读取方法有两个load_cst和load_value，load_cst创建结构，load_value读取实际数据
# 如果读取的过程中不需要调用SaveLoad().load，可以在load_cst里直接读取实际数据，否则应该在load_value读取实际数据
# 调用形式为：func_save: func_save(data,wt,save)，参数wt为io接口(写接口)，save为SaveLoad实例的save，该方法返回为空
# 			load_cst: load_cst(rd,load)，参数rd为io接口(读接口)，load为SaveLoad实例的load，该方法返回读取的对象
# 			load_value: load_value(obj,rd,load)，obj为load_cst返回的对象，该方法返回为空
# objsave.py后面有实际代码可以参考