#程序文件Pex3_9.py
from pylab import rc
from sympy import *
rc('font',size=16); rc('text',usetex=False)
x=symbols('x'); y=sin(x)
for k in range(3,8,2): print(y.series(x,0,k))  #等价于print(series(y,x,0,k))，泰勒展开到k-1项
plot(y,series(y,x,0,3).removeO(),series(y,x,0,5).removeO(),
     series(y,x,0,7).removeO(),(x,0,2),xlabel='$x$',ylabel='$y$')
