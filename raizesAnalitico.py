from math import sin, cos, pi, log, ceil
from concurrent.futures import ThreadPoolExecutor

def rootsearch(f,a,b,dx):
    x1 = a; f1 = f(a)
    x2 = a + dx; f2 = f(x2)
    while f1*f2 > 0.0:
        if x1 >= b:
            return None,None
        x1 = x2; f1 = f2
        x2 = x1 + dx; f2 = f(x2)
    return x1,x2

def bisect(f,x1,x2,switch=0,epsilon=1.0e-7):
    f1 = f(x1)
    if f1 == 0.0:
        return x1
    f2 = f(x2)
    if f2 == 0.0:
        return x2
    if f1*f2 > 0.0:
        print('Root is not bracketed')
        return None
    n = int(ceil(log(abs(x2 - x1)/epsilon)/log(2.0)))
    for i in range(n):
        x3 = 0.5*(x1 + x2); f3 = f(x3)
        if (switch == 1) and (abs(f3) >abs(f1)) and (abs(f3) > abs(f2)):
            return None
        if f3 == 0.0:
            return x3
        if f2*f3 < 0.0:
            x1 = x3
            f1 = f3
        else:
            x2 =x3
            f2 = f3
    return (x1 + x2)/2.0

def roots(f, a, b, eps=1e-7):
    print ('The roots on the interval [%f, %f] are:' % (a,b))
    while 1:
        x1,x2 = rootsearch(f,a,b,eps)
        if x1 != None:
            a = x2
            root = bisect(f,x1,x2,1)
            if root != None:
                pass
                Resultado = round(root,-int(log(eps, 10)))
                print(Resultado)
        else:
            print ('\nDone')
            break


if __name__ == "__main__":

    with ThreadPoolExecutor(2) as executor:
        Y_zero = lambda x: 8*sin(x) - 3*sin((11*x)/2)
        X_zero = lambda x: 8*cos(x) - 3*cos((11*x)/2)

        X_linhax = lambda x: 8*cos(x) - 3*(11/2)*cos((11*x/2))
        Y_linhaz = lambda x: -8*sin(x) + 3*(11/2)*sin((11*x/2))

        eq6 = lambda x: 8*sin(x/2) + 3*sin((11*x)/4)
        eq7 = lambda x: 8*sin(x/2) - 3*sin((11*x)/4)
        # executor.map(roots(eq6, 0, 4*pi))
        executor.map(roots(eq7, 0, 4*pi))