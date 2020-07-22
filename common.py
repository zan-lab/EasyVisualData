import xlrd
import os
import sys
def Res(data={},code=200,msg="Success"):
        return {"code":code,"data":data,"msg":msg}
def getTableName(filename):
        datafile=os.path.join("./uploads",filename)
        if os.path.exists(datafile)==False:
                return {"msg":"文件上传出错","code":"-1"}
        else:
                try:
                        xls=xlrd.open_workbook(datafile)
                        tablename=xls.sheet_names()
                        return {"msg":"SUCCESS","code":0,"data":tablename}

                except:
                        return {"msg": "文件打开出错，请检查文件格式","code":"-1"}
def checkTableName(filename,tablename):
        res=getTableName(filename)
        if res['code']==0:
                if tablename in res['data']:
                        res['data']={"tablename":tablename}
                        return res
                else:
                        res['code']=-2
                        res['data']={"tablename":tablename}
                        res['msg']="未找到该表名"
                        return res
        else:
                return res