import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import tushare as ts
from statsmodels.tsa.arima.model import ARIMA

def acquire_acf(data, m):
    m = 10  # 检验10个自相关系数

    acf, q, p = sm.tsa.acf(data, nlags=m, qstat=True)  ## 计算自相关系数 及p-value
    out = np.c_[range(1, 11), acf[1:], q, p]
    output = pd.DataFrame(out, columns=['lag', "AC", "Q", "P-value"])
    output = output.set_index('lag')
    print(output)

def AR_model(change_data):
    change_data = np.array(change_data, dtype=np.float)
    model = ARIMA(change_data, order=(1,1,1))
    results_AR = model.fit()
    plt.figure(figsize=(12, 6))
    plt.plot(change_data, 'b', label='changepct')
    plt.plot(results_AR.fittedvalues, 'r', label='AR model')
    plt.legend()
    plt.show()
    print(len(results_AR.roots))  # 模型阶数

ts.set_token('586bece88bd30938365edb42ca08df69e0ef26f668259de1405f5d6c')
pro = ts.pro_api()
df = pro.daily(ts_code='600519.SH',start_date='20180101') #茅台股价

df = df[['trade_date','close']]
df['trade_date'] = pd.to_datetime(df['trade_date'])
data = df.set_index('trade_date')

data['change_pct'] =''
for i in range(0,len(data['close'])-1):
    data.iloc[i, 1] = 100*(data['close'][i+1] - data['close'][i])/data['close'][i] # 计算每日收益率（涨跌幅）
data['change_pct'] = data['change_pct'][0:-1]
data['close_diff_1'] = data['close'].diff(1)
data = data[0:-1] # 由于changepct值最后一行缺失，因此去除最后一行
data['change_pct'] = data['change_pct'].astype('float64') #使changepct数据类型和其他三列保持一致
print(data.head())
data.plot(subplots=True,figsize=(12,12))
plt.show()

# 收盘价的自相关系数

close_data = data['close'] # 上证指数每日收盘价
m = 10 # 检验10个自相关系数
acquire_acf(close_data, m)


# 收益率的自相关系数
change_data = data['change_pct']
m = 10 # 检验10个自相关系数
acquire_acf(change_data, m)

AR_model(change_data)

