# 将控制台内容重定向至文件
"""
使用os.system(command)等模块执行系统命令时，返回值为命令执行结果，命令执行成功返回Ture，否则返回False；
若要得命令本身返回的内容，需要将命令输出至控制台的内容写到文件中，即将标准输出由控制台重定向至文件。
"""
import sys
import os

# 自定义目标文件夹和目标文件名
filepath = "E:/code/projects/weatherPlatform/templates"
filename = "chongDX.html"
fullname = os.path.join(filepath, filename)

# 备份默认的标准输出（输出值控制台）
standard_output = sys.stdout

# 将标准输出重定向至文件
"""
此处实质为向文件写入内容。
通常，向文件写入内容的步骤为：打开文件-->写入内容-->关闭文件
此处步骤与上述步骤相同，只不过“写”的方式发生了改变。
一般的文件写入为由人通过键盘键入内容或者copy内容，此处为由解释器向文件写入内容。
标准输出是解释器将内容写到（输出到）控制台，我们可以在控制台看到内容，此处这是解释器将内容
写入（输出到）了文件，我们可以在文件中找到内容。
"""
sys.stdout = open(fullname, "w+")

# 写入内容。已经将标注输出更改为输出至文件，所以执行命令后，会将原来输出至控制台的内容输出至文件。
help(list)

# 关闭文件
sys.stdout.close()

# 恢复默认标准输出
sys.stdout = standard_output

# # 检测写入到文件的内容
# print(open(fullname, "r").read())
