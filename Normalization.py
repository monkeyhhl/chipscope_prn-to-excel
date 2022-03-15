import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import codecs
import xlwt
import xlrd
import xlutils.copy

fig = plt.figure()
#ax1 = fig.add_subplot(1, 1, 1)


def prn2excel(file_name, column):
    "输入一个chipscope的文件，输出ecxel文件，其中转换出的十进制输出到sheet1中，归一化的数据输出到sheet2中,column为写入excle的第几列"
    f = codecs.open(file_name, mode='r', encoding='utf-8')  # 读取文件
    # lines = graph_data.split('\n')

    line = f.readline()  ##以行的形式读取文件
    pulse_data_hex = []  ##原始数据hex形式
    while line:  # 按行读取数据
        a = line.split('\t')  # 每行按照tab分离数据
        b = a[2]  # 读取第2列的数据adc1_data的数据
        pulse_data_hex.append(b)  # 将数据缓存到pulse_data_hex
        line = f.readline()
    f.close()

    pulse_data_hex.pop(0)  # 去掉文件中标题“adc1_data”
    hex2int = []  # 存储十六进制转为十进制的数据
    for i in pulse_data_hex:
        hex2int.append(int(i, 16))  # 将十六进制数据转为十进制的数据

    # 将转换后的数据保存到excel中
    # excel= xlwt.Workbook()  # 创建工作簿
    # sheet1 = excel.add_sheet(u'hex2int', cell_overwrite_ok=True)  # 创建sheet
    # sheet1 = excel.add_sheet(u'归一化', cell_overwrite_ok=True)  # 创建sheet
    # for i in range(len(hex2int)):
    #     sheet1.write(i, column, hex2int[i]) # 指定存入第column列
    # # sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))
    # excel.save('prn2excel.xls')  # 保存文件

    #################
    excel_path = "./prn2excel.xls"
    excel = xlrd.open_workbook(excel_path, formatting_info=True)
    new_book = xlutils.copy.copy(excel)  # 要使用这种xlutils方法不会对已有数据造成破坏
    new_sheet = new_book.get_sheet(0)
    for i in range(len(hex2int)):
        new_sheet.write(i, column, hex2int[i])  # 指定存入第column列
    new_book.save(excel_path)

    #################

    return hex2int
def normalization(data):
    " 将数据归一化，输入的是一串核脉冲数据，输出经过归一化后的数据"
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

excel = xlwt.Workbook()  # 创建空白工作簿
sheet0 = excel.add_sheet(u'hex2int', cell_overwrite_ok=True)  # 创建sheet0：hex2int
sheet1 = excel.add_sheet(u'归一化数据', cell_overwrite_ok=True)  # 创建sheet1：归一化数据
excel.save('prn2excel.xls')  # 保存文件

file_name = ['n1', 'y0']  # 在此输入要转换的文件名列表

hex2int_plot = {}  # 用于画图的数据
xs2 = np.arange(0, 1024, 1)  # 生成X坐标
# 将文件名列表中的文件全部写入excel
count = 0
print(len(file_name))
#ax1.clear()
while count < len(file_name):  # 将十六进制数转换为十进制数并写入到excel表中的sheet0中
    hex2int_plot[count] = prn2excel(file_name[count], count)  # 调用 prn2excel函数，将chipscope文件转为十进制保存到excel中
    # hex2int_plot[0]里的内容是一串核信号数据
    normalization_tmp = []
    normalization_tmp = normalization(hex2int_plot[count])  #hex2int_plot为已经转为十进制的数据
    excel_path = "./prn2excel.xls"
    excel = xlrd.open_workbook(excel_path, formatting_info=True)
    new_book = xlutils.copy.copy(excel)  # 要使用这种xlutils方法不会对已有数据造成破坏
    new_sheet = new_book.get_sheet(1) #将归一化的数据存入——sheet1：归一化数据 中
    for i in range(len(normalization_tmp)):
        new_sheet.write(i, count, normalization_tmp[i])  # 指定存入第column列
    new_book.save(excel_path)


##——————————————————————————————以下为画图用的代码
    plt.figure(1)
    plt.plot(xs2, hex2int_plot[count], label=file_name[count], linewidth=1)# 画转换为十进制的数据
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlabel("time/20ns")
    plt.ylabel("ADC")
    plt.plot()

    plt.figure(2)
    plt.plot(xs2, normalization_tmp, label=file_name[count], linewidth=1)  # 画归一化后的数据
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlabel("time/20ns")
    plt.ylabel("A.U.")
    plt.plot()


    count = count + 1  #有多少个文件就循环多少次
plt.show()

##——————————————————————————————给excel文件的每一列列头添加源文件的文件名，会敲除第0个有效数据，但几乎不影响数据
count = 0
while count < len(file_name):
    excel_path = "./prn2excel.xls"
    excel = xlrd.open_workbook(excel_path, formatting_info=True)
    new_book = xlutils.copy.copy(excel)
    new_sheet = new_book.get_sheet(0)
    new_sheet.write(0, count, file_name[count])
    new_sheet = new_book.get_sheet(1)
    new_sheet.write(0, count, file_name[count])
    new_book.save(excel_path)
    count = count+1

# print(hex2int_plot[0])

