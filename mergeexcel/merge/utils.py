import os
import xlrd
from django.conf import settings
from xlwt import Workbook
import pandas as pd
import shutil
def writeexcel(sheet1,list,n):
    '''
    :param sheet1: 写入的表格
    :param list: 传入的列表值
    :param n: 列值
    :return:
    '''

    for j in range(0, len(list)):
        sheet1.write(j, n, list[j])
#单文件处理
def mergerexcel(file):
    '''

    :param file: 读取文件的路径
    :return:
    '''
    try:
        #拼接路径，
        temp = os.path.join(settings.UPLOADFILES, "temp.xlsx")
        #拼接路径，
        old = os.path.join(settings.DOWNLOADFILES, "temp.xls")
        #以下是利用xlrd与pandas合并文件
        wb = xlrd.open_workbook(file)
        sh = [pd.read_excel(io=file, sheet_name=i, ) for i  in range(wb.nsheets)]
        b = pd.concat(sh, axis=0, join="outer", ignore_index=True, sort=True)
        b.to_excel(temp)
        #移动文件到下载目录。
        shutil.copyfile(temp, old)
        #以下是读取表头,返回表头
        tempsht = xlrd.open_workbook(temp)
        sh = tempsht.sheet_by_index(0)
        nc = sh.ncols  # 列
        headlist = []
        for i in range(nc):
            headlist.append(sh.cell_value(0,i))
        #处理完之后删除文件
        os.remove(file)
        return headlist

    except Exception as e :
        return e
#多文件处理
#与单文件处理类似，只不过多了一层循环，遍历读取文件
def mergerexcels(filelist):
    '''

    :param filelist: 读取文件的路径列表
    :return:
    '''
    try:
        temp = os.path.join(settings.UPLOADFILES, "temps.xlsx")
        old = os.path.join(settings.DOWNLOADFILES,"temp.xls")
        wblist = [xlrd.open_workbook(file) for file in filelist]
        sh = []
        for wb in range(len(wblist)):
            for j in range(wblist[wb].nsheets):
                sh.append(pd.read_excel(io=filelist[wb], sheet_name=j, ))
        b = pd.concat(sh, axis=0, join="outer", ignore_index=True, sort=True)
        b.to_excel(temp)
        shutil.copyfile(temp,old)
        tempsht = xlrd.open_workbook(temp)
        sh = tempsht.sheet_by_index(0)
        nc = sh.ncols  # 列
        headlist = []

        for i in range(nc):
            headlist.append(sh.cell_value(0,i))
        for file in filelist:
            os.remove(file)
        return headlist

    except Exception as e :
        return e
#excel文件跟去表头排序
def sortexcel(namelist):
    '''

    :param namelist: 表头列表
    :return: 排序成功返回True
    '''
    temp = os.path.join(settings.UPLOADFILES, "temp.xlsx")
    merge = os.path.join(settings.DOWNLOADFILES, "temp.xls")
    tempsht = xlrd.open_workbook(temp)
    onlykey = namelist[0]
    sh = tempsht.sheet_by_index(0)
    nc = sh.ncols  # 列
    nr = sh.nrows  # 行
    list2 = []

    for j in range(nc):
        list1 = []
        for k in range(nr):
            s = sh.cell_value(k, j)
            list1.append(s)
        list2.append(list1)

    wb = Workbook()
    sheet1 = wb.add_sheet("sheet1")
    for i in range(len(namelist)):
        for j in list2:
            if namelist[i] in j:
                writeexcel(sheet1, j, i)
    wb.save(merge)
    repeat = xlrd.open_workbook(merge)
    repsh = repeat.sheet_by_index(0)
    nc = repsh.ncols #列
    nr = repsh.nrows #行
    for i in range(1,nr):
        for j in range(1,nc):
            repsh.cell_value(i,j)

    return True
#excel文件去重函数，根据字典的键唯一原则去重。如果负载比较大，这里可以引用redis数据库
def quchong(merge):
    oldrepeat = xlrd.open_workbook(merge)
    repsh = oldrepeat.sheet_by_index(0)
    nc = repsh.ncols  # 列
    nr = repsh.nrows  # 行
    print(nc, nr)
    tabledata = {}
    tableheader = []
    for i in range(0,nc):
        tableheader.append(repsh.cell_value(0,i))

    for i in range(1, nr):
        listvalue = []
        listkey = repsh.cell_value(i, 0)
        for j in range(1, nc):
            cell = repsh.cell_value(i, j)
            listvalue.append(cell)
        tabledata.setdefault(listkey, listvalue)
    newrept = Workbook()
    sheet1 = newrept.add_sheet("sheet1")

    for i in range(len(tableheader)):
        sheet1.write(0, i, tableheader[i])
    i = 1
    for k, v in tabledata.items():
        sheet1.write(i, 0, k)
        for j in range(0, len(v)):
            sheet1.write(i, j+1, v[j])
        i += 1
    newrept.save(merge)
#使用缓冲流下载文件
def readFile(filename, chunk_size=512):
    """
    缓冲流下载文件方法
    :param filename:
    :param chunk_size:
    :return:
    """
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break