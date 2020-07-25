from pyecharts import options as opts
from pyecharts import charts
from pyecharts.charts import Bar, Page,Grid,Pie,Line
from common import Res
import os
import xlrd
import time
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
            if sheet.cell(1,1).ctype==0 or sheet.cell(1,0).ctype==0:
                return False
            #空格问题太要命，先不检测数据是否完整了

        elif typename=="折线图":
            if sheet.cell(1, 1).ctype == 0 or sheet.cell(1, 0).ctype == 0:
                return False
        elif typename=="饼图":
            if sheet.cell(0, 1).ctype == 0 or sheet.cell(0, 0).ctype == 0:
                return False
        return True
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
            return xls.sheet_by_name(sheetname)
        else:
            return filename+"中的"+sheetname+"不存在"

    #查看文件是否存在
    def checkFile(self,filename)->bool:
        datafile=os.path.join("./uploads",filename)
        return os.path.exists(datafile)
    #获取折线图
    def getLine(self,sheet:xlrd.sheet)->Line:
        #记录第一列的第二个单元格开始的数据，表示横轴
        xlist=sheet.col_values(0,1)
        #记录所有的列数据，表示y
        ylist=dict()
        for i in range(1,sheet.ncols):
            ylist[sheet.cell(0,i).value]=sheet.col_values(i,1)
        c=(
            Line(init_opts=opts.InitOpts(theme="chalk"))
            .add_xaxis(xaxis_data=xlist)
        )
        for name,list in ylist.items():
            c. add_yaxis(
            series_name=name,
            y_axis=list
             )
        c.set_global_opts(

            title_opts=opts.TitleOpts(title=sheet.name),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),#hover时的状态
            #toolbox_opts=opts.ToolboxOpts(is_show=True),#是否显示工具栏
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
             )

        return c

    #获取饼图
    def getPie(self,sheet:xlrd.sheet) -> Pie:
        names=sheet.col_values(0)
        values=sheet.col_values(1)
        c = (
            Pie(init_opts=opts.InitOpts(theme = "chalk"))
                .add(
                "tooltip 名",
                list(zip(names, values)),
                radius=["40%", "75%"],
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=sheet.name),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c

    #生成柱状图
    def getBar(self,sheet:xlrd.sheet) -> Bar:
        # 记录第一列的第二个单元格开始的数据，表示横轴
        xlist = sheet.col_values(0, 1)
        # 记录所有的列数据，表示y
        ylist = dict()
        for i in range(1, sheet.ncols):
            ylist[sheet.cell(0, i).value] = sheet.col_values(i, 1)
        c = Bar(init_opts=opts.InitOpts(theme = "wonderland"))
        c.add_xaxis(xlist)

        for k, v in ylist.items():
            c.add_yaxis(k, v)
        c.set_global_opts(
            title_opts=opts.TitleOpts(title=sheet.name)
           # legend_opts=opts.LegendOpts( pos_top="15%", pos_left="2%")
        )

        #设置x轴大小
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

    #生成所有图表，放到一个page里
    def render(self):
        page=Page(page_title= "数据可视化",layout=Page.SimplePageLayout)

        for tabledic in self.tablelist:
            #获取每次的文件名和表名
            filename=tabledic.get('filename')
            tablename=tabledic.get('tablename')
            type=tabledic.get('type')
            #判断是否文件存在
            if not self.checkFile(filename):
                return Res(code='-2',msg=filename+"文件不存在")
            #返回sheet对象，如果没有则返回出错message
            sheet=self.getSheet(filename,tablename)
            #根据类型来判断是否获取到了
            if isinstance(sheet,str):
                return Res(code='-2',msg=sheet)
            if not self.checkData(sheet,type):
                return Res(code='-2',msg=sheet.name+"sheet的数据不合理")
            page.add(self.getCharts(sheet,type))
        renderfilename=str(int(time.time()))+'.html'
        page.add_js_funcs('document.body.style.backgroundColor="rgba(41, 52, 65, 1)"')
        page.render(os.path.join('./downloads',renderfilename))
        return Res(data={'renderfilename':renderfilename},msg="已生成")

