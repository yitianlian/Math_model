
import pandas as pd
import os
# 读取数据文件
def readDataFile(readPath):
    try:
        if readPath[-4:] == ".csv":
            dfFile = pd.read_csv(readPath, header=0, sep=",")
        elif readPath[-4:] == ".xls" or readPath[-5:] == ".xlsx":
            dfFile = pd.read_excel(readPath, header=0)
        elif readPath[-4:] == ".dat":
            dfFile = pd.read_table(readPath, sep=" ", header=0)
        else:
            print("不支持的文件格式。")
    except Exception as e:
        print(f"读取数据文件失败：{str(e)}")
        return
    return dfFile

def read_txt(txt_path):
    with open(path) as f:    #打开文件并绑定对象f
        s=f.read().splitlines()  #返回每一行的数据
    return s

# 主程序
def main():
    # 读取数据文件 # Youcans, XUPT
    readPath = "../data/toothpaste.csv"  # 数据文件的地址和文件名
    dfFile = readDataFile(readPath)  # 调用读取文件子程序

    print(type(dfFile))  # 查看 dfFile 数据类型
    print(dfFile.shape)  # 查看 dfFile 形状（行数，列数）
    print(dfFile.head())  # 显示 dfFile 前 5 行数据
    return
if __name__ == '__main__':  # Youcans, XUPT
        main()