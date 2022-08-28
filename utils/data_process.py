import pandas as pd
import numpy as np
import statsmodels
import matplotlib.pyplot as plt
import plotly.express as ex

def fill_nan(data: pd.DataFrame, style='forward_fill'):
    """填补空缺值

    Args:
        data (pd.DataFrame): 含有空缺值的dataframe列
        style (str, optional): 填补的方式. Defaults to 'forward_fill'.
    """    ''''''
    if style=='forward_fill':
        data.ffill(inplace=True)
    elif style=='moving_average':
        data=np.where(data.isnull(),
                             data.shift(1).rolling(3,min_periods=1).mean(),
                             data)
    elif style=='inter_lin':
        data = data.interpolate(method='linear')
    elif style=='inter_poly':
        data=data.interpolate(method='polynomial', order=3)

def data_smoothing(data:pd.DataFrame, alpha=0.8):
    """data smoothing

    Args:
        data (pd.DataFrame): the data need to smoothing
        alpha (float, optional): the smoothing alpha. Defaults to 0.8.
    """    ''''''
    data= data.ewm(alpha =alpha).mean()
    
def ADF_test(data: pd.Series, autolag='AIC'):
    """ADF检测平稳性

    Args:
        data (pd.Series): _description_
        autolag (str, optional): _description_. Defaults to 'AIC'.
    return: ADF Statistic, p-value
    """
    result = statsmodels.tsa.stattools.adfuller(data, autolag='AIC')
    return result[0], result[1]

def draw_acf_pacf(data: pd.Series):
    statsmodels.graphics.tsaplots.plot_acf(data)
    plt.show()
    statsmodels.graphics.tsaplots.plot_pacf(data)
    plt.show()
    
    