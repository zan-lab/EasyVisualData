import xlrd
import os
xls=xlrd.open_workbook(os.path.join('.\data','测试数据.xlsx'))
sheet=xls.sheet_by_name('柱状图')
print(sheet.ncols)
print(sheet.col_types(0))