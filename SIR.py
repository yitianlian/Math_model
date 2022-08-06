
# 1. SIR 模型，常微分方程组
from scipy.integrate import odeint  # 导入 scipy.integrate 模块
import numpy as np  # 导入 numpy包
import matplotlib.pyplot as plt  # 导入 matplotlib包

def dySIS(y, t, lamda, mu):  # SI/SIS 模型，导数函数
    dy_dt = lamda*y*(1-y) - mu*y  # di/dt = lamda*i*(1-i)-mu*i
    return dy_dt

def dySIR(y, t, lamda, mu):  # SIR 模型，导数函数
    i, s = y
    di_dt = lamda*s*i - mu*i  # di/dt = lamda*s*i-mu*i
    ds_dt = -lamda*s*i  # ds/dt = -lamda*s*i
    return np.array([di_dt,ds_dt])

# 设置模型参数
number = 1e5  # 总人数
lamda = 0.02  # 日接触率, 患病者每天有效接触的易感者的平均人数
sigma = 3.28  # 传染期接触数
mu = 0.93  # 日治愈率, 每天被治愈的患病者人数占患病者总数的比例
fsig = 1-1/sigma
tEnd = 200  # 预测日期长度
t = np.arange(0.0,tEnd,1)  # (start,stop,step)
i0 = 1e-4  # 患病者比例的初值
s0 = 1-i0  # 易感者比例的初值
Y0 = (i0, s0)  # 微分方程组的初值

print("lamda={}\tmu={}\tsigma={}\t(1-1/sig)={}".format(lamda,mu,sigma,fsig))

# odeint 数值解，求解微分方程初值问题
ySI = odeint(dySIS, i0, t, args=(lamda,0))  # SI 模型
ySIS = odeint(dySIS, i0, t, args=(lamda,mu))  # SIS 模型
ySIR = odeint(dySIR, Y0, t, args=(lamda,mu))  # SIR 模型

# 绘图
plt.title("Comparison among SI, SIS and SIR models")
plt.xlabel('t-youcans')
plt.axis([0, tEnd, -0.1, 1.1])
plt.axhline(y=0,ls="--",c='c')  # 添加水平直线
plt.plot(t, ySI, ':g', label='i(t)-SI')
plt.plot(t, ySIS, '--g', label='i(t)-SIS')
plt.plot(t, ySIR[:,0], '-r', label='i(t)-SIR')
plt.plot(t, ySIR[:,1], '-b', label='s(t)-SIR')
plt.plot(t, 1-ySIR[:,0]-ySIR[:,1], '-m', label='r(t)-SIR')
plt.legend(loc='best')  # youcans
plt.show()
