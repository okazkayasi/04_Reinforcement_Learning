from cvxopt import matrix
A = matrix([1., 2., 3., 4., 5., 6.], (2,3))
print(A)

A.size


B = matrix([[1., 2.], [3., 4.]])
print(B)

print (matrix([ [A] , [B] ])) # this adds  next columns

# spmatrix creates a sparce matrix

from cvxopt import spmatrix

D = spmatrix([1., 2.], [0, 1], [0, 1], (4,2))
print (D)

A = matrix(range(16), (4,4))
print (A)

print (A[[0,1,2,3], [0,2]]) # take index 0 and 2 as col

print (A[0,2]) # take only 0,2

print (A[1, :]) # double indexing

print (A[::-1, ::-1])

# numpy and CVXOPT

from numpy import array
A = matrix([[1,2,3], [4,5,6]])
B = array(A)
type(B)

C = matrix(B)
type(C)

