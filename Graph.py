from pyecharts import options as opts
from pyecharts import charts
from pyecharts.charts import Bar, Page,Grid,Pie,Line
from common import Res
import os
import xlrd
class Graph:

    def __init__(self,tablelist):
        #除去空数据
        for i in tablelist:
            if i==[]:
               tablelist.remove(i)
        self.tablelist=tablelist
    #查看数据是否合法
    def checkData(self,sheet:xlrd.sheet,typename)->bool:
        if typename=="柱状图":
            return True
            pass
        elif typename=="折线图":
            pass
        elif typename=="饼图":
            pass

    #返回sheet对象
    def getSheet(self,filename,sheetname):
        dirpath = os.path.abspath("./uploads")
        filepath=os.path.join(dirpath,filename)
        try:
            xls=xlrd.open_workbook(filepath)
        except:
            return filename + "文件打开失败"
        sheetlist=xls.sheet_names()
        if sheetname in sheetlist:
            return xls.sheets['sheetname']
        else:
            return filename+"中的"+sheetname+"不存在"

    #查看文件是否存在
    def checkFile(self,filename)->bool:
        datafile=os.path.join("./uploads",filename)
        return os.path.exists(datafile)
    #获取折线图
    def getLine(self,sheet:xlrd.sheet)->Line:
        pass
    #获取饼图
    def getPie(self,sheet:xlrd.sheet) -> Pie:
        pass
    #生成柱状图
    def getBar(TableData) -> Bar:
        c = Bar()
        c.add_xaxis(TableData.xlist)
        for k, v in TableData.ylist.items():
            c.add_yaxis(k, v)
        c.set_global_opts(title_opts=opts.TitleOpts(title=TableData.name))
        # c.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10,interval=0)))
        return c
    #生成charts
    def getCharts(self,sheet,typename)->charts:
        if typename == "柱状图":
            return self.getBar(sheet)
        elif typename == "折线图":
            return self.getLine(sheet)
        elif typename == "饼图":
            return self.getPie(sheet)
    def render(self):
        page=Page(layout=Page.SimplePageLayout)
        for tabledic in self.tablelist:
            #获取每次的文件名和表名
            filename=tabledic.get('filename')
            tablename=tabledic.get('tablename')
            type=tabledic.get('type')
            #判断是否文件存在
            if not self.checkFile(filename):
                pass
            #返回sheet对象，如果没有则返回出错message
            sheet=self.getSheet(filename,tablename)
            #根据类型来判断是否获取到了
            if type(sheet)==str:
                pass
            if not self.checkData(sheet,type):
                pass
            page.add(self.getCharts(sheet,type))
        page.render()
        return Res(msg="已生成")

        #
        #还差，找到两个表的数据渲染方法，由sheet生成图表