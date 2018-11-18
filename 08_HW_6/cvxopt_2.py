from cvxopt import matrix, solvers
import numpy as np

A = [[0.0, 0.17, -4.69], [-0.17, 0.0, 1.0], [4.69, -1.0, 0.0]]
A = matrix(A)

A = matrix([[A], [-1., -1., -1.]])

A = -A
print (A)

A = np.array(A)
print (A)
newrow = [1., 1., 1., 0.]
A = np.vstack([A, newrow])
newrow = [-1., -1., -1., 0]
A = np.vstack([A, newrow])
A = matrix(A)
print (A)
add = np.hstack([np.eye(3) * -1, np.zeros((3, 1))])
A = np.vstack([A, add])
A = matrix(A)



c = matrix([0., 0., 0., -1.])
b = matrix([0., 0., 0., 1., -1., 0., 0., 0.])



sol = solvers.lp(c,A,b)

# sol = solvers.lp(c,A,b, solver='glpk')

print (sol['x'])
a = [sol['x'][0], sol['x'][1], sol['x'][2]]
print (a)
