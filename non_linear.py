from scipy.optimize import brent, fmin, minimize
import numpy as np
# brent()：单变量无约束优化问题，混合使用牛顿法/二分法。
# fmin()：多变量无约束优化问题，使用单纯性法，只需要利用函数值，不需要函数的导数或二阶导数。
# leatsq()：非线性最小二乘问题，用于求解非线性最小二乘拟合问题。
# minimize()：约束优化问题，使用拉格朗日乘子法将约束优化转化为无约束优化问题。



# optimize.brent() 的主要参数：
#
# func: callable f(x,*args) 　　目标函数 ，以函数形式表示，可以通过 *args 传递参数
# args: tuple　　可选项，以 f(x,*args) 的形式将可变参数 p 传递给目标函数  。
# brack: tuple　　可选项，搜索算法的开始区间（不是指 x 的上下限）
# optimize.brent() 的主要返回值：
#
# xmin: 　　返回函数达到最小值时的 x（注意是局部最优，不一定是全局最优）。
# fval: 　　返回函数的最优值（默认不返回，仅当 full_output 为 1 时返回）。

def objf(x):
    fx = x**2 - 8*np.sin(2*x+np.pi)
    return fx

xIni = -5
x_res = brent(objf, brack=(xIni,2))
print("xOpt={:.4f}\tfxOpt={:.4f}".format(x_res,objf(x_res)))


# optimize.fmin() 的主要参数：
#
# func: callable f(x,*args) 　　目标函数 ​，以函数形式表示，可以通过 *args 传递参数。
# x0: nadarray　　搜索算法的初值。
# args: tuple　　可选项，以 f(x,*args) 的形式将可变参数 p 传递给目标函数 ​ 。
# optimize.fmin() 的主要返回值：
#
# xopt: 　　返回最小值时的 x 值。
# fopt: 　　返回最小值时的目标函数值，fopt=func(xopt)。

def objf2(x):  # Rosenbrock benchmark function
    fx = sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0)
    return fx

xIni = np.array([-2, -2])
xOpt = fmin(objf2, xIni)
print("xIni={:.4f},{:.4f}\tfxIni={:.4f}".format(xIni[0],xIni[1],objf2(xIni)))
print("xOpt={:.4f},{:.4f}\tfxOpt={:.4f}".format(xOpt[0],xOpt[1],objf2(xOpt)))


# 导入 scipy、numpy 包；
# 定义目标函数 objf3(x)，输入变量 x 表示向量，返回值 fx 是目标函数的计算结果 。
# 定义边界约束，即优化变量的上下限：
# minimize() 默认无边界约束条件，即各自变量的取值范围没有限制；
# 如果设置边界约束，要对每个自变量（决策变量）定义其上下限，注意定义边界约束的格式；
# 如果某个自变量没有上限（下限），则表示为 None 。
# 4. 定义 x 的初值。
#
# 5. 求解最小化问题 resRosen，其中目标函数 objf3 和搜索的初值点 xIni 是必需的，指定优化方法和边界条件是可选项。如果优化问题是求最大值 maxFx，可以通过 minFx = - maxFx 的变换来实现。
#
# 6. 通过调用最小化问题的返回值 resRosen.x 得到最优点 xOpt。

# 注意，这里必须化为标准式子，只有大于等于和等于号

def objf3(x):
    a,b,c,d = 1,2,3,8
    fx = a*x[0]*x[0]+b*x[1]*x[1]+c*x[2]+d
    return fx

def con1(x):
    return x[0]**2-x[1]+x[2]**2
def con2(x):
    return -(x[0]+x[1]**2+x[2]**3-20)
def con3(x):
    return -x[0]-x[1]**2+2
def con4(x):
    return x[1]+2*x[2]**2-3

c1 = {'type':'ineq', 'fun':con1}
c2 = {'type':'ineq', 'fun':con2}
c3 = {'type':'eq', 'fun':con3}
c4 = {'type':'eq', 'fun':con4}
c_all = (c1,c2,c3,c4)
b = (0.0,None)
bnds = (b,b,b)

x0 = np.array([1., 2., 3.])
res = minimize(objf3, x0, bounds=bnds, constraints=c_all)

print("Optimization problem (res):\t{}".format(res.message))  # 优化是否成功
print("xOpt = {}".format(res.x))  # 自变量的优化值
print("min f(x) = {:.4f}".format(res.fun))  # 目标函数的优化值