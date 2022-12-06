from math import sin, cos, pi

def eqs(u):
    return 6*sin(u/2) - 7*sin((3*u/2))

def bissec(a,b):
    # E faz o papel de x, não é preciso passar ele como parametro para esssa função
    # seja p o ponto médio de a e b
    p = (a+b)/2
    
    aux1 = eqs(a)
    aux2 = eqs(p)
    
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
            g = round((a+b)/2, 5)
    if retorno:
        return g, erro
    return g

print(solvBissec(0,6.28,10**-7,True))