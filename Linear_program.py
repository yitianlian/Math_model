import pulp


# LpProblem 代表是一个问题， 然后problem1是我给这个问题定的名字，sense代表我要求解的是最大值还是最小值，这里代表极大值
myproblem = pulp.LpProblem('problem1', sense=pulp.LpMaximize)

# 这里代表三个问题变量，最小值取0，最大值取7， ‘continuous’代表是连续变量， ' Integer ' 表示离散变量（用于整数规划问题）、' Binary ' 表示0/1变量（用于0/1规划问题）。
x1 = pulp.LpVariable('x1', lowBound=0, upBound=7, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, upBound=7, cat='Continuous')
x3 = pulp.LpVariable('x3', lowBound=0, upBound=7, cat='Continuous')

myproblem += 2*x1 + 3*x2 - 5*x3      # 设置目标函数
myproblem += (2*x1 - 5*x2 + x3 >= 10)
myproblem += (x1 + 3*x2 + x3 <= 12)
myproblem += (x1 + x2 + x3 == 7)
myproblem.solve()  # 解决问题

print(pulp.LpStatus[myproblem.status])

for v in myproblem.variables():  # 这里储存着问题的变量
    print(v.name, "=", v.varValue)  # 输出每个变量的最优值
print("Max F(x) = ", pulp.value(myproblem.objective))  #输出最优解的目标函数值


# 多变量问题求解

import numpy as np

a = np.arange(0,20)
for i in range(len(a)):
    print(min(len(a)-1-6, max(i-3, 0)), min(len(a)-1, max(i+3, 6)))