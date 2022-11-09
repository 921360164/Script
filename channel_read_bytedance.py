#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile, sys

'''
读取zip评论内容
'''
def readComment(file):
    originStr = str(zipfile.ZipFile(file, 'r').comment)
    print('原始数据：' + originStr)
    print('解析的数据：' + originStr[originStr.index('{'):(originStr.index('}') + 1)])

'''
写入zip评论内容
'''
def writeComment(file, json):
    archive = zipfile.ZipFile(file, 'a')
    archive.comment = bytes(json, encoding='utf8') + archive.comment
    archive.close()

if __name__ == '__main__':
    try:
        print("usage: channel_read_bytedance -r xxxx.apk \n channel_read_bytedance -w xxxx.apk -d {\"test\":\"test\"}")
        if sys.argv[1] == '-r' and sys.argv[2] != '':
            readComment(sys.argv[2])
        elif sys.argv[1] == '-w' and sys.argv[2] != '' and sys.argv[3] == '-d' and sys.argv[4] != '':
            writeComment(sys.argv[2], sys.argv[4])
        else:
            print('argv analysis error')
    except Exception as e:
        print(e)
