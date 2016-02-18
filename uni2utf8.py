#-*- coding:utf-8 -*-
__author__ = 'miudodo'


import json              #导入Json模块

def processJson(inputJsonFile, outputJsonFile):
    fin = open(inputJsonFile, 'r')
    fout = open(outputJsonFile, 'w')
    for eachLine in fin:
        line = eachLine.strip().decode('utf-8')                #去除每行首位可能的空格，并且转为Unicode进行处理
        line = line.strip(',')                                 #去除Json文件每行大括号后的逗号
        js = None
        try:
            js = json.loads(line)                              #加载Json文件
        except Exception,e:
            print 'bad line'
            continue
        #js["xxx"] = xxx                                        #对您需要修改的项进行修改，xxx表示你要修改的内容
        outStr = json.dumps(js, ensure_ascii = False) + ','    #处理完之后重新转为Json格式，并在行尾加上一个逗号
        fout.write(outStr.strip().encode('utf-8') + '\n')      #写回到一个新的Json文件中去
    fin.close()                                                #关闭文件
    fout.close()

processJson('items.json', 'item.json')

