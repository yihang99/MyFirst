from time import *

s = 50

print('start'.center(s//2, '-'))
start = time()
for i in range(s+1):
    a = '*'*i
    b = '.'*(s-i)
    c = i/s*100
    dur = time() - start
    print("\r{:>6.1f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end = '')
    sleep(0.1)
print('\n'+'complete'.center(10, '-'))
