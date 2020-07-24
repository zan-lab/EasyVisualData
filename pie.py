from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
x=['吃饭','睡觉','打游戏']
y=[30,100,22.2222]

c = (
    Pie()
    .add(
        "tooltip 名",
        list(zip(x,y)),
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-Radius"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("pie_radius.html")
)