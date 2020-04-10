import random as rd
import numpy as np
import time

n = 100
ls = np.zeros(n, int)

for i in range(n):
    a = rd.randrange(0, n)
    ls[a] += 1
    rd.seed(a + time.time() + rd.random())

t = 0
for j in ls:
    pass

print(n - list(ls).count(0))
print(ls.reshape((10, 10)))
