from sklearn import linear_model
import numpy as np

import matplotlib.pyplot as plt

X = np.array([8.19, 2.72, 6.39, 8.71, 4.7, 2.66, 3.78])
Y = np.array([7.01, 2.78, 6.47, 6.71, 4.1, 4.23, 4.05])

X = X.reshape(-1,1)
model = linear_model.LinearRegression()
model.fit(X=X, y=Y)
k = model.coef_
b = model.intercept_
fig = plt.figure()
x = np.linspace(0,10,1000)
y=x*k+b
plt.scatter(x=X.reshape(1,-1), y=Y)
plt.plot(x,y)
plt.show()