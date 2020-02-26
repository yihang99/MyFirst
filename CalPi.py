#exercise


from random import *

try:
    r = int(eval(input('Input range:')))
    nin = 0
    a = -1
    for i in range(r):
        x = random()
        y = random()
        if x**2 + y**2 < 1:
            nin += 1
        x = (50*(i+1))//r
        if x != a:
            a = x
            b = 50 - a
            pro = '|'+a*'*'+b*'.'+'|'
            print('\r{:>5.1f}% '.format(2*a)+pro,end = '')
    pi = 4*nin/r
    print("\nπ={:.9f}".format(pi))
except:
    print('error')
