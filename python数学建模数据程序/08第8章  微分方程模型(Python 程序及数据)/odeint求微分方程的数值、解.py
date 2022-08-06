#程序文件Pex8_4.py
from scipy.integrate import odeint
from numpy import arange
dy=lambda y, x: -2*y+x**2+2*x  # 代表y对于x的导数，这里是隐函数求导
x=arange(1, 10.5, 0.5)
sol=odeint(dy, 2, x)  # 第一个是方程，第二个是初始值，第三个是自变量
print("x={}\n对应的数值解y={}".format(x, sol.T))
