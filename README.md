# python_object_saveload

# for Python2.7

# main codes are in objsave.py
# example are in example.py

# ����ʵ����objsave.py
# ʵ��ʹ�òο�emample.py

# character font in readme is too large, don't want to write too much
# the program is to save python object to file and load python object from file. generally, base type and Objects inherit from type object can directly use the program to save and load. the main work of the project is: 1, a framework and implement of save&load of base type(int, float, list, map...) 2, an io interface and implementation in file. 3, avoid unlimit save when objects has ring

# ��readmeд������ʾ�ܴ󣬲����д
# ʵ�ֽ�python���󱣴浽�ļ��ʹ��ļ���ȡ�ķ������������ͺͼ̳���object�Ķ���һ�㶼����save��load����Ҫ�Ĺ����ǣ�1��һ����ܺͻ����������ͣ�int��float��list��map��������save��load��ʵ�֣�2��һ��io�ӿں������ļ��ϵ�ʵ�֣�3���ڶ�����л���ʱ�򣬱�������ѭ����save


# ������demo.py�ĺ��������ʹ��
# can easily used by demo.py