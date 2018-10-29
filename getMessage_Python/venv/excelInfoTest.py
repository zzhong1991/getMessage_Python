#-*- coding:utf-8 -*-

import xlwt
from wxpy import *
import os

bot = Bot(cache_path=True)

# 新建一个excel文件
file = xlwt.Workbook()
borders = xlwt.Borders()
borders.left = xlwt.Borders.DASHED
#边框格式
borders.right = xlwt.Borders.DASHED
borders.top = xlwt.Borders.DASHED
borders.bottom = xlwt.Borders.DASHED
borders.left_colour = 0x40
borders.right_colour = 0x40
borders.top_colour = 0x40
borders.bottom_colour = 0x40
style = xlwt.XFStyle() # Create Style 1
style_1 = xlwt.XFStyle() #Create Style 2
style_2 = xlwt.XFStyle() #Create Style 3
style.borders = borders # Add Borders to Style1
style_1.borders = borders # Add Borders to Style2
style_2.borders = borders # Add Borders to Style2
#背景色
pattern = xlwt.Pattern()
pattern_1 = xlwt.Pattern()
pattern_2 = xlwt.Pattern()

pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern.pattern_fore_colour = 5

pattern_1.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern_1.pattern_fore_colour = 2
pattern_2.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern_2.pattern_fore_colour = 3

style.pattern = pattern
style_1.pattern = pattern_1
style_2.pattern = pattern_2
# 新建一个sheet
table = file.add_sheet('info', cell_overwrite_ok=True)
# 写入数据table.write(行,列,value)

table.write(0, 0, '姓名',style_2)
table.write(0, 1, '性别',style_2)
table.write(0, 2, '城市',style_2)
table.write(0, 3, '签名',style_2)
table.write(0, 4, '备注',style_2)

#测试、定义单元格宽度
col_width = [0,12,0,0,0]
for h in bot.friends():
    if len(h.name) > col_width[0]:
        col_width[0] = len(h.name)
    if len(h.city) > col_width[2]:
        col_width[2] = len(h.city)
    if len(h.signature) > col_width[3]:
        col_width[3] = len(h.signature)
    if len(h.remark_name) > col_width[4]:
        col_width[4] = len(h.remark_name)

m = 0
for c in col_width:
    table.col(m).width = 256 * c
    m += 1
list_1 = [style,style_1]
i=0
sex=''
for f in bot.friends():
    i=i+1
    if i == 1:
        continue
    if i % 2 == 1:
        list_2 = list_1[0]
    else:
        list_2 = list_1[1]
    table.write(i-1, 0, f.name,list_2)
    if f.sex==1:
        sex='男'
    elif f.sex==2:
        sex='女'
    table.write(i-1, 1, sex,list_2)
    table.write(i-1, 2, f.city,list_2)
    table.write(i-1, 3, f.signature,list_2)
    table.write(i-1, 4, f.remark_name,list_2)

# 保存文件
file.save('filex.xls')
print('save success!')
os.system('filex.xls')