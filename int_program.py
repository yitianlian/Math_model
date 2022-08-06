import pulp

pro1 = pulp.LpProblem('first_p', sense=pulp.LpMaximize)

x1 = pulp.LpVariable('x1', lowBound=0, upBound=15, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, upBound=7.5, cat='Continuous')

pro1+=(10*x1+9*x2)

pro1 += (6*x1 + 5 * x2 <=60)
pro1 += (10 * x1+20* x2 <=150)
pro1.solve()

for v in pro1.variables():
    print(v.name,' ', v.value())

print('res0', pulp.value(pro1.objective))
