#!/usr/bin/env python3# -*- coding: utf-8 -*-
import pandas as pd
import os
path=r'C:\Users\49216\Desktop\新建文件夹\st_resident'
files=[]# 遍历所有文件路径，并将结果储存于files
for root, _, names in os.walk(path):
    for name in names:
        files.append(os.path.join(root,name))
        for file in files:
            df=pd.read_csv(file)    # 获取文件名，并生成csv格式的文件名用于导出
            (filepath, tempfilename) = os.path.split(file)
            (filename, extension) = os.path.splitext(tempfilename)
            output=path + "\%s.xlsx" % filename # 生成导出的文件名称csv格式
            df.to_excel(output)
