from math import sin, cos, pi

def eqs(u,id):
    if id == 8:
        return (cos(pi/9)/cos(11*pi/18))*8*sin(u/2)-3*sin(11/4*u)

def bissec(a,b):
    # E faz o papel de x, não é preciso passar ele como parametro para esssa função
    # seja p o ponto médio de a e b
    p = (a+b)/2
    
    aux1 = eqs(a,8)
    aux2 = eqs(p,8)
    
    if aux1*aux2 < 0:
        # temos a raiz nesse intervalo
        b = p
    else:
        # a raiz está no outro intervalo
        a = p
    # a função retorna os novos intervalos a e b
    return a,b

def error_bi(a,b):
    # o erro para a bisseção é a metade do intervalo de busca
    e = abs((b-a))/2
    return e

def solvBissec(a,b,er,retorno):
    # parametros a e b do intervalo de busca
    # er o valor do erro
    # retorno é variavel booleana, se for true retorna a raiz
    # e o valor do erro
    # se não apenas a raiz
    # também devemos informar a exentricidade e a Anomalia Media "M"
    # POIS A FUNÇAO bissec e h usão esses parametros

    # variavel aux para o while
    check = True

    while check:
        
        erro = error_bi(a,b)

        if erro <= er:
            check = False
        else:
            a, b = bissec(a,b)
            g = (a+b)/2
    if retorno:
        return g, erro
    return g

print(solvBissec(6,6.1,10**-7,True))