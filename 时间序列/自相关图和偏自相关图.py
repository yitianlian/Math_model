import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm

data = pd.read_csv("daily-minimum-temperatures-in-me.csv", parse_dates=['Date'], index_col='Date')
data.head()
data.plot(figsize=(12,6))
# plt.show()

# 画自相关图
sm.graphics.tsa.plot_acf(data)
plt.figure(figsize=(12, 6))
plt.show()

# 偏自相关图
sm.graphics.tsa.plot_pacf(data, lags=50)
plt.figure(figsize=(12, 6))
plt.show()