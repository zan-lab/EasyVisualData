from pyecharts import options as opts
from pyecharts import charts
from pyecharts.charts import Bar, Page,Grid,Pie,Line,Gauge,Funnel,Radar
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
        elif typename=="仪表盘":
            if sheet.cell(0,0).ctype==0 or sheet.cell(0,1).ctype==0:
                return False
        elif typename=="漏斗图":
            if sheet.cell(0,0).ctype==0 or sheet.cell(0,1).ctype==0:
                return False
        elif typename=="雷达图":
            #检查 是否maxvalue齐全
            if 0 in sheet.col_types(1,1) or 0 in sheet.col_types(2,1):
                return False
            #检查每个value是否小于等于maxvalue
            for j in range(2,sheet.ncols):
                for i in range(1,sheet.nrows):
                    if sheet.cell(i,j).value>sheet.cell(i,1).value:
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
            legend_opts=opts.LegendOpts(pos_left="20%", pos_top='5%')
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
            title_opts=opts.TitleOpts(title=sheet.name+"\n",pos_left='left',title_textstyle_opts={'color':'#FFFFFF'}),
            legend_opts=opts.LegendOpts(  pos_left="20%",pos_top='5%')
        )

        #设置x轴大小
        # c.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10,interval=0)))
        return c
    #生成仪表盘
    def getGauge(self,sheet:xlrd.sheet)->Gauge:
        key=sheet.cell(0,0).value
        value=sheet.cell(0,1).value
        g=Gauge()
        g.add(series_name=sheet.name, data_pair=[(key,value)],
              title_label_opts=opts.LabelOpts(
                font_size=40, color="blue", font_family="Microsoft YaHei"),
              )#改标题字体颜色

        g.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            #tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{a} <br/>{b} : {c}%",textstyle_opts=opts.TextStyleOpts(color="#fff")),#图例颜色和显示格式
            title_opts=opts.TitleOpts(title=sheet.name)#加上图标题
        )
        return g
    #生成漏斗图
    def getFunnel(self,sheet:xlrd.sheet)->Funnel:
        x_data = sheet.col_values(0)
        y_data = sheet.col_values(1)
        data=[(x_data[i],y_data[i]) for i in range(len(x_data))]
        f=Funnel()
        f.add(
            series_name=sheet.name,
            data_pair=data,
            gap=2,
            #tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%",textstyle_opts=opts.TextStyleOpts(color="#fff")),#图例颜色和显示格式
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
        )
        f.set_global_opts(title_opts=opts.TitleOpts(title=sheet.name,title_textstyle_opts=opts.TextStyleOpts(color="#fff")))
        return f
    #生成雷达图
    def getRadar(self,sheet:xlrd.sheet)->Radar:
        namelist = sheet.col_values(0, 1)
        maxvaluelist=sheet.col_values(1,1)
        maxlist=[opts.RadarIndicatorItem(name=namelist[i],max_=maxvaluelist[i]) for i in range(len(namelist))]
        valuelists = dict()
        for i in range(2, sheet.ncols):
            valuelists[sheet.cell(0, i).value] = sheet.col_values(i, 1)
        r=Radar()
        r.add_schema(
            schema=maxlist,
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="#fff"),
        )
        #设置颜色的列表
        colorstr=["#CD0000","#5CACEE","#7B68EE","#FFFF00"]
        colorth=0
        for name,values in valuelists.items():
            r.add(
                series_name=name,
                data=values,
                linestyle_opts=opts.LineStyleOpts(color=colorstr[colorth]),
            )
            colorth=(colorth+1)%len(colorstr)#颜色循环

        r.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        r.set_global_opts(
            title_opts=opts.TitleOpts(title=sheet.name,title_textstyle_opts=opts.TextStyleOpts(color="#fff")), legend_opts=opts.LegendOpts()
        )
        return r
    #生成charts
    def getCharts(self,sheet,typename)->charts:
        sheet.name=sheet.name+"\n"
        if typename == "柱状图":
            return self.getBar(sheet)
        elif typename == "折线图":
            return self.getLine(sheet)
        elif typename == "饼图":
            return self.getPie(sheet)
        elif typename=="仪表盘":
            return self.getGauge(sheet)
        elif typename=="漏斗图":
            return self.getFunnel(sheet)
        elif typename=="雷达图":
            return self.getRadar(sheet)

    #生成所有图表，放到一个page里
    def render(self):
        page=Page(page_title= "数据展示",layout=Page.SimplePageLayout)

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
                return Res(code='-2',msg=sheet.name+"sheet的数据不合理,请查看使用说明!")
            page.add(self.getCharts(sheet,type))
        renderfilename=str(int(time.time()))+'.html'
        page.add_js_funcs('document.body.style.backgroundColor="rgba(41, 52, 65, 1)"')
        page.render(os.path.join('./downloads',renderfilename))
        return Res(data={'renderfilename':renderfilename},msg="已生成")

