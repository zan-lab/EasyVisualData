from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Grid
def getBar(TableData) -> Bar:

    c =Bar()
    c.add_xaxis(TableData.xlist)

    for k,v in TableData.ylist.items():
        c.add_yaxis(k,v)
    c.set_global_opts(title_opts=opts.TitleOpts(title=TableData.name))
    #c.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10,interval=0)))
    return c
