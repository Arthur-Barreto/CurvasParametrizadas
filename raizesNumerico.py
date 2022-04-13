from numpy import arange
from math import pi, cos, sin, isclose

listaIntervalo = arange(0,4*pi,10e-5)
print("Intervalo Criado")

eixoX = lambda x: 8*cos(x)-3*cos((11*x)/2)
eixoY = lambda x: 8*sin(x)-3*sin((11*x)/2)
listaValoresX = []
listaValoresX2 = []
listaValoresY = []
listaValoresY2 = []
listaValoresfor = []
print("Listas Criadas")
for intervalo in listaIntervalo:
    X = eixoX(intervalo)
    Y = eixoY(intervalo)
    listaValoresX.append(round(X,4))
    listaValoresY.append(round(Y,4))

res = set([x for x in listaValoresX if listaValoresX.count(x) > 1])

print("For concluído")
print(res)
