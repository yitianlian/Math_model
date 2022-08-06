from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox  #导入白噪声检验函数
from random import gauss
# 时间序列的数据分解为趋势(trend),季节性(seasonality)和残差(residual)三部分
from statsmodels.tsa.seasonal import seasonal_decompose
def test_stationarity(timeseries, window=12):
    rolmean = timeseries.rolling(window=window, center=False).mean()
    rolstd = timeseries.rolling(window=window, center=False).std()
    orig = plt.plot(timeseries, color='blue', label='Original')# 设置原始图，移动平均图和标准差图的式样
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')  # 使用自动最佳的图例显示位置
    plt.title('Rolling Mean & Standard Deviation')
    plt.show() #供肉眼观察是否平稳
    print('ADF检验结果：')
    dftest = adfuller(timeseries, autolag='AIC')  # 使用减小AIC的办法估算ADF测试所需的滞后数
    # 将ADF测试结果、显著性概率、所用的滞后数和所用的观测数打印出来
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', 'Num Lags Used', 'Num Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)
# test_stationarity(ts_week)

def noise_detection():
    whitenoise = pd.Series([gauss(0.0, 1.0) for i in range(1000)]) #创建一个高斯分布的白噪声
    print(u'白噪声检验结果为：', acorr_ljungbox(whitenoise,lags=1)) #检验结果：平稳度，p-value。p-value>0.05为白噪声




def clean_tend(for_data=False):

    # 转化为平稳序列
    '''
    Deflation by CPI
    Logarithmic（取对数）
    First Difference（一阶差分）
    Seasonal Difference（季节差分）
    Seasonal Adjustment
    '''
    # 影响因素：
    # 趋势 Trend
    # 季节性 Seasonality


    data = pd.read_csv('AirPassengers.csv', parse_dates=['Month'], index_col='Month')
    print(data.head())
    ts = data['AirPassengers']
    ts_log = np.log(ts)
    if for_data:
        return ts_log
    plt.plot(ts)
    # plt.show()
    test_stationarity(ts)

    # 消除趋势的第一个方法是转换。在本例中我们可以清楚地看到有一个显著的趋势。
    # 我们可以通过变换，惩罚较高值而不是较小值。这可以采用取对数log,平方根,立方跟等。

    plt.title('add log')
    plt.plot(ts_log)
    plt.show()


    # 聚合-取一段时间的平均值（月/周平均值）
    # 平滑-取滚动平均数
    # 多项式回归分析-适合的回归模型

    moving_avg = ts_log.rolling(12).mean()
    plt.plot(ts_log)
    plt.plot(moving_avg, color='red')
    plt.show()

    ts_log_moving_avg_diff = ts_log - moving_avg
    print(ts_log_moving_avg_diff.head(12))

    ts_log_moving_avg_diff.dropna(inplace=True)
    test_stationarity(ts_log_moving_avg_diff)

    # 加权移动平均
    # 指数加权移动平均法是很受欢迎的方法，所有的权重被指定给先前的值连同衰减系数。这可以通过Pandas实现：

    expwighted_avg = ts_log.ewm(halflife=12).mean()  # 参数“halflife”来定义指数衰减量
    plt.plot(ts_log)
    plt.plot(expwighted_avg, color='red')
    plt.title('exp wighted avg')
    plt.show()

    ts_log_ewma_diff = ts_log - expwighted_avg
    test_stationarity(ts_log_ewma_diff)

    # 两种消除趋势和季节性的方法：
    # 差分：采用一个特定时间差的差值
    # 分解：建立有关趋势和季节性的模型和从模型中删除它们

    ts_log_diff = ts_log.diff() # ts_log_diff = ts_log - ts_log.shift() 差分
    plt.plot(ts_log_diff)

    ts_log_diff.dropna(inplace=True)  # 差分需要去除nan
    test_stationarity(ts_log_diff)
    return ts_log

def clean_season_affect(ts_log):
    decomposition = seasonal_decompose(ts_log)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    plt.subplot(411)
    plt.plot(ts_log, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()
    ts_log_decompose = residual
    ts_log_decompose.dropna(inplace=True)
    test_stationarity(ts_log_decompose)



def main():
    ts_log = clean_tend(True)
    clean_season_affect(ts_log)


if __name__=='__main__':
    main()