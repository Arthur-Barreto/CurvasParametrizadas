import numpy as np
import math

from numpy.lib.function_base import append
from scipy.integrate import quad

#  criando as funções necessárias para o projeto
#########################################################################
###### funções para o sistema linear, usando o metodo LU ################
def decompLU(A):

    '''
    Decomposição da matriz lu,
    como dito em aula, vamos sobreescrever esta matriz,
    perdendo assim os dados da mesma, por outro lado
    ganharemos memoria no sistema
    '''
    # calcular a ordem da matriz de dados
    n = len(A)

    for j in range(n):
        for i in range(n):

            # lower da matriz
            if i >= j:
                s = 0
                for k in range(0,j):
                    s += A[i][k]*A[k][j]
                A[i][j] -= s

            # parte upper da matriz
            else:
                s = 0
                for k in range(0,i):
                    s += A[i][k] * A[k][j]
                # fazemos o casting para float para garantir as casas decimais
                # na divisão
                A[i][j] = (A[i][j] - s)/float(A[i][i])

def calcLU(LU,B):
    
    # Vamos de fato resolver o nosso sistema após organizado
    # no final retorna o vetor solução

    # calculando a ordem da matriz
    n = len(LU)
    assert len(B) == n

    #     
    # criando o vetor y
    y = np.zeros(n,dtype=float)
    for i in range(n):
        s = 0
        for j in range(0,i):
            s += LU[i][j]*y[j]
        # fazendo casting dos dados para float 
        y[i] = (B[i] - s)/float(LU[i][i])

    # descomente o print para visualizar o vetor intermediario y
    # print("O vetor y é: {}".format(y))

    # com o vetor y vamos voltar ao problema e finalmente
    # encontrar o vetor solução, Ux = y

    # criando o vetor x 
    x = np.zeros(n,dtype=float)
    for i in range(n-1,-1,-1):
        s = 0
        for j in range(i+1,n):
            s += LU[i][j]*x[j]
        x[i] = y[i] - s
    
    # agora temos o sistema resolvido, retornar o vetor solução

    return x

def lu(A,B):
    # a matriz A é a matriz dos coeficientes
    # a matriz B é a matriz dos valores
    
    # ajustando a matriz A
    decompLU(A)

    # descomente o for para visualizar a matriz LU

    # for i in range(len(A)):
    #     print("{}\n".format(A[i]))

    temp = calcLU(A,B)
    return temp
#############################################################################
########### fim das funções para a solução do sistema linear ################

############################################################################
########## funções para o metodo da bisseção e newton ######################

# função que retorna o valor de f(h)

def h(u):
    value = -8*math.sin(u) + (33/2)*math.sin((11/2)*u)
    return value

def bissec(a,b):
    # E faz o papel de x, não é preciso passar ele como parametro para esssa função
    # seja p o ponto médio de a e b
    p = (a+b)/2
    
    aux1 = h(a)
    aux2 = h(p)
    
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

# função que retorna a derivada de h(E)
def dh(u):
    derivada = -8*math.cos(u) + (363/4)*math.cos((11/2)*u)
    return derivada

# função que retorna o erro  para o metodo de newton
def error_ne(x):
    value = abs(x[1] - x[0])
    return value

def solvNEWTON(ini,er,retorno):

    # ini é o chute inicial
    # er é o erro máximo da solução
    # e é a exentricidade da elipse
    # M é anomalia Média
    # retorno é variavel booleana para retornar apenas a solução ou solução com erro junto

    # variavel aux para o while
    check = True

    # a segunda possição é o chute inicial, a primeira inicializamos como zero

    x = [0,ini]

    while check:
        
        erro = error_ne(x)

        if erro <= er:
            check = False
        else:
            # seja xa a raiz anterior
            # seja xp a raiz posterior
            xa = x[1]
            aux1 = h(xa)
            aux2 = dh(xa)
            xp = xa - aux1/aux2
            x = [xa,xp]
    
    if retorno:
        return xp,erro
    return xp

#################################################################################
################## fim das funções dos metodos de newton e bisseção #############

#################################################################################
########## funções para determinar a posição orbital do satelite ################

def anomaliaMEDIA(P,t):
    # informar o periodo e o instante de tempo t
    M = (2*math.pi/P)*t
    return M

def anomaliaEXCTRIC(e,er,P,t,retorno):
    # e é a exentricidade da elpise
    # er é o erro maximo permitido
    # P é o periodo do sistema
    # t é o instante de tempo para calculo da anomalia media

    # retorno é variavel booleana para retorna o erro junto
    # se verdadeira retorna o erro da medida, se não apenas a raiz

    # aqui usamos o metodo da bissecção para calcular um chute inicial, com um erro "grande"
    # apos isso usamos essa raiz aproximada e calculamos a raiz mais exata com o metodo de newton
    
    M = anomaliaMEDIA(P,t)

    # na variavel chute temos a solução aproximada pelo metodo da bissecção, agora usar o metodo de newton
    chute = solvBissec(0,2*math.pi,1e-1,e,M,False)
    raiz, erro = solvNEWTON(chute,er,e,M,True)

    if retorno:
        return raiz,erro
    else:
        return raiz

def anomaliaVERDADEIRA(e,er,P,t):
    # devemos receber todos os parametros para o calculo da anomalia exentrica

    E = anomaliaEXCTRIC(e,er,P,t,False)
    # tan_2 é a tangente de teta sobre/2
    tan_2 = math.sqrt((1+e)/(1-e))*math.tan(E/2)
    teta_2 = math.atan(tan_2)
    teta = 2*teta_2
    return teta

def calcR(e,er,P,t,a):
    # recebemos todos os parametros da anomalia verdadeira
    # adicinal do teta obitdo na anomalia verdadeira e do semi eixo maior da elpse

    teta = anomaliaVERDADEIRA(e,er,P,t)
    dist = a*((1-e**2)/(1+e*math.cos(teta)))

    return dist

def posCARTESIANA(e,er,P,t,a,xc,f):
    # recebemos todos os parametros usados para o calculo da posição
    # mais a posição do centro da elpse e o foco da mesma

    r = calcR(e,er,P,t,a)
    teta = anomaliaVERDADEIRA(e,er,P,t)

    x = r*math.cos(teta) + xc + f
    y = r*math.sin(teta)

    # a função retorna os valores de x e y naquele instante de tempo

    return x,y 
#######################################################################################
########## fim das funções para o calculo da posição orbital do satelite ##############

#######################################################################################
################ inicio das funções para a interpolação da curva ######################

def coef_spline(x,y):    
    # o algoritmo será implementado para o metodo livre
    # portando a segunda derivada será nula nos extremos

    # calculando o grau do polinomio
    n = len(x)

    a = y.copy()
    h = np.zeros(n-1)
    for i in range(n-1):
        h[i] = x[i+1] - x[i]

    # matrizes a resolver
    A = np.zeros((n,n))
    B = np.zeros(n)

    # parte de contorno
    for i in range(1,n-1):
        A[i][i-1] = h[i-1]
        A[i][i] = 2*(h[i-1] + h[i])
        A[i][i+1] = h[i]
        B[i] = 3.0*(a[i+1] - a[i])/float(h[i]) - 3.0*(a[i] - a[i-1])/float(h[i-1])

    A[0][0]  = 1.0
    A[-1][1] = 1.0

    # encontrando os coeficientes
    c = np.linalg.solve(A,B)
    b = np.zeros(n-1)
    d = np.zeros(n-1)
    for i in range(n-1):
        b[i] = (a[i+1]  -a[i])/float(h[i]) - h[i]*(2*c[i] + c[i+1])/3.0
        d[i] = (c[i+1] - c[i])/(3.0*h[i])
    
    coef = np.zeros((n-1,4))
    for i in range(n-1):
        coef[i][0] = a[i]
        coef[i][1] = b[i]
        coef[i][2] = c[i]
        coef[i][3] = d[i]
    
    return coef

def calc_pol_spline(x,X,coef):
    '''
    coef vem da matriz de coef, calculados na função coef_spline
    x é o vetor com os dados
    X ponto onde calcular a spline (pode ser ponto ou vetor)
    '''

    y = 0

    try:
        # usuario passando vetor de entrada
        n = len(X)
        y = np.zeros(n)
        for i in range(n):
            y[i] = calc_pol_spline(x,X[i],coef)
    except:
        # se for escalar entra aqui
        k = np.searchsorted(x,X)

        if k > 0: 
            k -= 1
        if k == len(x):
            k -= 1
        
        H = X - x[k]
        ak = coef[k][0]
        bk = coef[k][1]
        ck = coef[k][2]
        dk = coef[k][3]
        y = ak + H*(bk + H*(ck + H*dk))

    return y

def gauss_legendre_coef(n):

    # dado o grau do polinomio, 2<=n<=5, 
    # a função retorna os coef 
    
    r = np.zeros(n)
    c = np.zeros(n)

    if n == 2:
        r[0] = np.sqrt(3)/3.0
        r[1] = -r[0]

        c[0] = 1.0
        c[1] = c[0]
    
    elif n == 3:
        r[0] = 0.0
        r[1] = np.sqrt(15)/5.0
        r[2] = -r[1]

        c[0] = 8.0/9.0
        c[1] = 5.0/9.0
        c[2] = c[1]

    elif n == 4:
        s30 = np.sqrt(30)

        r[0] = np.sqrt(525 - 70*s30)/35.0
        r[1] = -r[0]
        r[2] = np.sqrt(525 + 70*s30)/35.0
        r[3] = -r[2]

        c[0] = (18 + s30)/36.0
        c[1] = c[0]
        c[2] = (18 - s30)/36.0
        c[3] = c[2]

    elif n == 5:
        s70 = np.sqrt(70)

        r[0] = 0
        r[1] = np.sqrt(245 - 14*s70)/21.0
        r[2] = -r[1]
        r[3] = np.sqrt(245 + 14*s70)/21.0
        r[4] = -r[3]

        c[0] = 128.0/255.0
        c[1] = (322 + 13*s70)/21.0
        c[2] = c[1]
        c[3] = (322 - 13*s70)/900.0
        c[4] = c[3]

    return r,c 

def gauss_legendre(f,a,b,n):
    # calcula a integral usando o metodo de gauss legendre
    # f é a função a ser integrada
    # a e b são os inervalor da integração

    I = 0
    r,c = gauss_legendre_coef(n)

    for i in range(n):
        x = ((b-a)*r[i] + (a+b))/2.0
        y = f(x)
        m = c[i]*y
        I += m

    I *= (b-a)/2.0

    return I

def integrand(x, a, b, xc):
    A = (-b**2)/(a**2)
    B = ((2*b**2)/(a**2))*xc
    C = (b**2(a**2 - xc**2))/a**2
    # y_2 representa a equação 6 do roteiro
    y_2 = A*x**2 + B*x + C
    return math.sqrt(y_2)

def area(X,Y,i,j,incremento,a,b,xc,spline):

    # X,Y são os vetor espaçado da orbita, os pontos vermelhos
    # i e j são os indices do intervalo a ser integrado
    # dx é o quão pequeno se deseja fazer  intervalo da interpolação
    # se spline == true, area será calculada pelo metodo da spline
    # se spline == false, area será calculada usando a eq 6

    ax = X[i]
    bx = X[j]

    ay = Y[i]
    by = Y[j]

    if spline:
        # definindo o intervalo de x
        vecx = np.linspace(ax,bx,incremento)
        vecy = np.linspace(ay,by,incremento)

        # caclulando o coef da spline
        coef = coef_spline(vecx,vecy)
        # calculando o polinomio spline
        polinomio_spline = calc_pol_spline([ax,bx],vecx,coef)

        print(polinomio_spline)

        # agora podemos calcular a integral, uma vez que o polinomio foi definido
        integral = gauss_legendre(polinomio_spline,ax,bx,3)

    else:

        # vamos calular a integral usando a equação 6 do roteiro
        A = (-b**2)/(a**2)
        B = ((2*b**2)/(a**2))*xc
        C = (b**2(a**2 - xc**2))/a**2
        # vamos usar essa biblioteca para calcular a integral da eq 6
        # a mesma é uma raiz quadrada de uma expressão, por isso vamos usar quad
        # o primeiro parametro é o nome da função, depois os intevalos de integração
        # como argumento damos as constantes que multiplicam a varivel na ordem descrescente de potencia
        integral = quad(integrand,ax,bx,args=(A,B,C))

    return integral