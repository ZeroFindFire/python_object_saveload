# python_object_saveload

# for Python2.7

# main codes are in objsave.py
# example are in example.py

# 具体实现在objsave.py
# 实际使用参考emample.py

# character font in readme is too large, don't want to write too much
# the program is to save python object to file and load python object from file. generally, base type and Objects inherit from type object can directly use the program to save and load. the main work of the project is: 1, a framework and implement of save&load of base type(int, float, list, map...) 2, an io interface and implementation in file. 3, avoid unlimit save when objects has ring

# 在readme写的字显示很大，不想多写
# 实现将python对象保存到文件和从文件读取的方法，基本类型和继承自object的对象，一般都可以save和load。主要的工作是，1）一个框架和基本数据类型（int，float，list，map。。。）save和load的实现，2）一个io接口和其在文件上的实现，3）在对象间有环的时候，避免无限循环的save


# 可以用demo.py的函数方便的使用
# can easily used by demo.py