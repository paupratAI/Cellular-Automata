import numpy as np

a = np.array([[[0,0.4,0] for _ in range(100)] for _ in range(100)], dtype=float)
print(a[(0,2),(5,1)])
a[(0,2),(5,1)] = 4
print(a)