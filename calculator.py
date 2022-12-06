import math

A_list = [math.pi, math.pi, math.pi * 2, math.pi * 2]
B_list = [-3.52184, -2.76134, -4.6409, -1.64229]
for i in range(len(A_list)):
    A = A_list[i]
    B = B_list[i]
    v = (A - B)/2
    u = A - v
    print(f'v: {v}; u: {u}')
