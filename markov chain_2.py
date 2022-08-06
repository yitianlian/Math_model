
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (11, 5)  #set default figure size
import quantecon as qe
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from quantecon import MarkovChain

# 一个转移概率矩阵P
# 一个初始的状态init
# 一个正整数sample_size，表示时间序列的长度。
# 手动实现
def mc_sample_path(P, ini=None, sample_size=1_000):

    # set up
    P = np.asarray(P)
    X = np.empty(sample_size, dtype=int)

    # Convert each row of P into a cdf
    n = len(P)
    P_dist = [np.cumsum(P[i, :]) for i in range(n)]  # 求固定维度上的累计和
    print(P_dist)
    # draw initial state, defaulting to 0
    if ini is not None:
        X_0 = qe.random.draw(np.cumsum(ini)) # 根据 cdf 给出的累积分布概率值生成随机样本的，可以指定生成样本的总数，默认是根据概率值生成一个值
    else:
        X_0 = 0

    # simulate
    X[0] = X_0
    for t in range(sample_size - 1):
        X[t+1] = qe.random.draw(P_dist[X[t]])

    return X

P = [[0.4, 0.6],
     [0.2, 0.8]]

X = mc_sample_path(P, ini=[0.9, 0.1], sample_size=100_000)
print(X)
print(np.mean(X == 0))

# 调用库实现，速度很快

mc = qe.MarkovChain(P)
X = mc.simulate(ts_length=1_000_000)
print(np.mean(X == 0))

# 添加状态名
mc = qe.MarkovChain(P, state_values=('unemployed', 'employed'))

print(mc.simulate(ts_length=4, init='unemployed'))
print(mc.simulate(ts_length=4, init='employed'))
print(mc.simulate(ts_length=4))  # 随机选取初始化条件值

print(mc.simulate_indices(ts_length=4))  # 打印状态值索引

P = [[0.9, 0.1, 0.0],
     [0.4, 0.4, 0.2],
     [0.1, 0.1, 0.8]]

mc = qe.MarkovChain(P, ('poor', 'middle', 'rich'))
print(mc.is_irreducible)  # 判断马尔可夫链是不是不可约的


# 验证马尔可夫链周期性
P = [[0, 1, 0],
     [0, 0, 1],
     [1, 0, 0]]

mc = qe.MarkovChain(P)
print(mc.period)
P = [[0.0, 1.0, 0.0, 0.0],
     [0.5, 0.0, 0.5, 0.0],
     [0.0, 0.5, 0.0, 0.5],
     [0.0, 0.0, 1.0, 0.0]]

mc = qe.MarkovChain(P)
print(mc.period)

print(mc.is_aperiodic)  # 判断是否为非周期性

# 求马尔可夫链的平稳分布x，使得x = xP

P = np.array([[0.4, 0.6],
              [0.2, 0.8]])
ψ = (0.25, 0.75)
print(ψ @ P) # [0.25,0.75]

# 求平稳分布
mc = qe.MarkovChain(P)
print(mc.stationary_distributions)  # 显示所有的平稳分布，（平稳分布不止一个）

# 求解平稳分布

P = ((0.971, 0.029, 0.000),
     (0.145, 0.778, 0.077),
     (0.000, 0.508, 0.492))
P = np.array(P)

ψ = (0.0, 0.2, 0.8)        # Initial condition

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.set(xlim=(0, 1), ylim=(0, 1), zlim=(0, 1),
       xticks=(0.25, 0.5, 0.75),
       yticks=(0.25, 0.5, 0.75),
       zticks=(0.25, 0.5, 0.75))

x_vals, y_vals, z_vals = [], [], []
for t in range(20):
    x_vals.append(ψ[0])
    y_vals.append(ψ[1])
    z_vals.append(ψ[2])
    ψ = ψ @ P

ax.scatter(x_vals, y_vals, z_vals, c='r', s=60)
ax.view_init(30, 210)

mc = qe.MarkovChain(P)
ψ_star = mc.stationary_distributions[0]
ax.scatter(ψ_star[0], ψ_star[1], ψ_star[2], c='k', s=60)

plt.show()

