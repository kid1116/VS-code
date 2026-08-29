import numpy as np
X = np.array([1,2,3])    
W1 = np.array([[1,2,3],
               [4,5,6],
               [7,8,9]])
print(W1)       
print(X @ W1)
print(X @ W1 + 1)                     
print((X @ W1).shape)             