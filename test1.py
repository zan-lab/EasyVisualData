import pyecharts.options as opts
from pyecharts.charts import Line,Page,Bar

themes = [
 ('chalk', '粉笔风'),
 ('dark', '暗黑风'),
 ('essos', '厄索斯大陆'),
 ('infographic', '信息图'),
 ('light', '明亮风格'),
 ('macarons', '马卡龙'),
 ('purple-passion', '紫色激情'),
 ('roma', '石榴'),
 ('romantic', '浪漫风'),
 ('shine', '闪耀风'),
 ('vintage', '复古风'),
 ('walden', '瓦尔登湖'),
 ('westeros', '维斯特洛大陆'),
 ('white', '洁白风'),
 ('wonderland', '仙境')
]

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
snms = ['蒸发量', '降水量']
data = {
         snms[0]: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
         snms[1]: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
        }

a, b = snms

page = Page(layout=Page.SimplePageLayout)

for i, (e, c) in enumerate(themes):
    tags = [f'{i + 1}_柱状图基本示例：\n\t\t{e}：（{c}）',
            '一年的降水量和蒸发量']
    mt, st = tags

    # 利用动态变量和共同指向一个对象的赋值特性向 page 添加图像
    x = '变量别名'
    locals()[f'bar_{i}'] = x  # 动态变量
    x = (
        Bar(init_opts=opts.InitOpts(theme = e))
        .add_xaxis(xaxis_data=months)
        .add_yaxis(series_name=a, yaxis_data=data.get(a))
        .add_yaxis(series_name=b, yaxis_data=data.get(b))
        .set_global_opts(
            title_opts = opts.TitleOpts(title = mt,
                                    subtitle = st))
           )

    page.add(x)

page.render('bar_theme.html')