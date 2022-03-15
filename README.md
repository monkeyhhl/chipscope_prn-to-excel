# chipscope_prn-to-excel
将多个Xilinx Chipscope输出的ASCII格式文件转到一个excel文件中，因为在实验中需要使用到FPGA和ADC将采集到的波形数据保存下来，但Xilinx 的Chipscope在线逻辑分析仪的BUS Plot波形显示的export输出来的是十六进制，通常会采集很多个波形数据还要归一化观察波形宽窄，为了方便一次读取多个文件转换到一个excel中方便操作，所以写了这个脚本，一劳永逸。

## 本脚本实现的功能：
将在线逻辑分析仪Chipscope输出的16进制数据转换成10进制格式和归一化保存到一个excel文件中。
## 注意事项：
- 0.我的n1,y0 两个文本第3列才是我需要的有效数据，数据的形状类似指数衰减信号。
- 1.从chipscope中使用ASCII导出信号的数据，注意需要1024个点，否则会报错（需修改列表长度即可）。注意保存时文件不要带有后缀，需要将文件放置在.py相同的根目录下，带后缀也行，就是记得要在python脚本的第65行加上扩展名。我的
- 2.当保存了很多数据后，在python代码中第65行修改添加文件名即可：
file_name = ['n1', 'y0']  # 在此输入要转换的文件
- 3.程序运行后会生成 prn2excel.xls 文件，文件中记录了原始数据（十进制）和归一化后的数据分别记录在“hex2int”和“归一化数据”两个工作表中，同时会有两个图生成。
