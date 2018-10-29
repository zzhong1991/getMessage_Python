#-*- coding:utf-8 -*-

import xlwt,xlrd

def infoExcel(result,title):
    try:
        # 设置字体
        font = xlwt.Font()
        font.bold = True
        # 设置边框
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        # 设置居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_TOP  # 垂直方向
        # 设置背景颜色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 3  # 背景颜色
        # 定义不同的excel style
        style1 = xlwt.XFStyle()
        style1.font = font
        style1.borders = borders
        style1.alignment = alignment
        style2 = xlwt.XFStyle()
        style2.borders = borders
        style2.alignment = alignment

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('My Worksheet')
    except Exception as  e:
        print(e)
    # 确定栏位宽度
    col_width = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            if i == 0:
                col_width.append(len_byte(result[i][j]))
            else:
                if col_width[j] < len_byte(str(result[i][j])):
                    col_width[j] = len_byte(result[i][j])

    # 设置栏位宽度，栏位宽度小于10时候采用默认宽度
    for i in range(len(col_width)):
        if col_width[i] > 10:
            worksheet.col(i).width = 256 * (col_width[i] + 1)

    excelTitle=['发布时间','标 题  ','评论(条)','有无视频','链       接       ']
    isExsit='False'
    try:
        # 打开文件
        xlrd.open_workbook(title)
        isExsit = 'True'
    except Exception as e:
        print('数据写入...')
    if isExsit=='True' :
        rexcel = open_workbook(title)  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
        row = rows
        for addResult in result :
            for j in range(len(addResult)):
                # xlwt对象的写方法，参数分别是行、列、值
                table.write(row,j, addResult[j])
            row += 1
        try:
            # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            excel.save(title)
        except Exception :
            # 失败过后5秒再次尝试
            time.sleep(5)
            excel.save(title)
    else :
        excelCheck(worksheet,workbook,excelTitle,result,style1,style2,title)

def excelCheck(worksheet,workbook,oneResult,result,style1,style2,title):
    try:
        # 生成第一行
        for i in range(0, len(oneResult)):
            worksheet.write(0, i, label=oneResult[i], style=style1)
        # excel内容写入
        for i in range(len(result)):
            for j in range(len(result[i])):
                worksheet.write(i + 1, j, label=result[i][j], style=style2)
        # 保存excel
        workbook.save(title)
    except Exception as e:
        print(e)
# 获取字符串长度，一个中文的长度为2
def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)