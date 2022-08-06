
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn import metrics
from sklearn import datasets
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

def draw(data):
    new_cases= np.array(data['new_cases'].tolist())

def linear_re(x,y):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=1)
    print(X_train.shape)
    print(X_test.shape)
    # print(y_train)

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    print(lr.coef_)
    print(lr.intercept_)

    y_pred = lr.predict(X_test)

    MSE = metrics.mean_squared_error(y_test, y_pred)
    RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    print('MSE:', MSE)
    print('RMSE:', RMSE)
    plt.figure(figsize=(30, 5))
    plt.plot(range(len(y_test)), y_test, 'r', label='ground truth')
    plt.plot(range(len(y_test)), y_pred, 'b', label='predict')
    plt.legend()
    plt.show()

def normlization(data):
    data = (data - data.min(axis=0))/(data.max(axis=0)-data.min(axis=0))
    return data

# 主程序
def main():
    # 读取数据文件 # Youcans, XUPT
    readPath = "./data.csv"  # 数据文件的地址和文件名
    dfFile = readDataFile(readPath)  # 调用读取文件子程序

    print(type(dfFile))  # 查看 dfFile 数据类型
    print(dfFile.shape)  # 查看 dfFile 形状（行数，列数）
    print(dfFile.head())  # 显示 dfFile 前 5 行数据

    new_cases = np.array(dfFile['new_cases'].tolist())
    new_death = np.array(dfFile['new_death'].tolist())
    val = dfFile.values
    dfFile.drop(columns='total_tests')
    # teat = np.array([[1000,  10, 9]])
    # val = val[..., -1[:-1]]
    # print(type(val[1][-1]))
    data = val[..., 3:]
    data = normlization(data)
    one_hot = pd.get_dummies(dfFile)
    one_hot = one_hot.values
    one_hot = normlization(one_hot)

    print(one_hot[:5])
    new_cases = (new_cases-min(new_cases))/(max(new_cases)-min(new_cases))
    # linear_re(data, new_cases)


    return
if __name__ == '__main__':  # Youcans, XUPT
        main()