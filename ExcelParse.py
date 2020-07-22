import xlrd
import os
import sys
#每一个表的数据
class TableData:
    name="默认名称"
    xlist=[]
    ylist=dict()
#数据的加载和组装
class DataProvider:
    #默认全存在data文件夹里
    path=os.path.abspath(".\data")

    #最终的table全在这里
    TableList=list()
    def __init__(self,filename):
        self.path=os.path.join(self.path,filename)
        self.load()
    def load(self):
        xls=xlrd.open_workbook(self.path)
        for sheet in xls.sheets():
            if sheet.cell(1,0).value=="" :break
            table=TableData()
            table.name=sheet.name
            table.xlist=self.__getxlist(sheet)
            table.ylist=self.__getylist(sheet)
            self.TableList.append(table)
    #获取x轴的名称list
    def __getxlist(self,table)->list:
        a=table.col_values(0,1)
        return a

    #获取y轴的名称和值
    def __getylist(self, table)->dict:
        a=dict()

        for col in range(1,table.ncols):
            if(table.cell(1,col).ctype==0):break

            b=table.col_values(col,1)
            colname=table.cell(0,col).value
            #解决数字作为y标题的问题
            if(table.cell(0,col).ctype==2):
                colname=int(colname)
                colname=str(colname)
            a[colname]=b
        return a

