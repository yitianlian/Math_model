
import pandas as pd

# 读取数据文件
def readDataFile(readPath):  # readPath: 数据文件的地址和文件名
    # readPath = "../data/youcansxupt.csv"  # 文件路径也可以直接在此输入
    try:
        if (readPath[-4:] == ".csv"):
            dfFile = pd.read_csv(readPath, header=0, sep=",")  # 间隔符为逗号，首行为标题行
            # dfFile = pd.read_csv(filePath, header=None, sep=",")  # sep: 间隔符，无标题行
        elif (readPath[-4:] == ".xls") or (readPath[-5:] == ".xlsx"):  # sheet_name 默认为 0
            dfFile = pd.read_excel(readPath, header=0)  # 首行为标题行
            # dfFile = pd.read_excel(filePath, header=None)  # 无标题行
        elif (readPath[-4:] == ".dat"):  # sep: 间隔符，header：首行是否为标题行
            dfFile = pd.read_table(readPath, sep=" ", header=0)  # 间隔符为空格，首行为标题行
            # dfFile = pd.read_table(filePath,sep=",",header=None) # 间隔符为逗号，无标题行
        else:
            print("不支持的文件格式。")
    except Exception as e:
        print("读取数据文件失败：{}".format(str(e)))
        return
    return dfFile



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