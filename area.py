import math
import numpy as np

def x(t):
    return 8*math.cos(t) - 3*math.cos(11*t/2)
def y(t):
    return 8*math.sin(t) - 3*math.sin(11*t/2)

v3 = 0
u3 = 0
intervalo = np.arange(v3, u3, (u3-v3)/1000)

def areaTriangulo(A,B):
    determinante = abs(A[0]*B[1] - A[1]*B[0])
    return 0.5*determinante

pontos = []

for t in intervalo:
    pontos.append([x(t),y(t)])
    
area = 0
i = 1
while i < len(pontos):
    area += areaTriangulo(pontos[i],pontos[i-1])
    i+=1
print(area)