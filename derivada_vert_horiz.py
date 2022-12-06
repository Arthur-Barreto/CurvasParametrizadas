import math; import numpy as np

def remove_repetidos(lista):
    l = []
    for i in lista: # filtrando os repetidos
        if i not in l:
            l.append(i) # adicionando os elementos únicos
    l.sort() # ordenando a lista
    l_linha = [lista[0]] # adicionando o primeiro elemento
    for i in range(1, len(lista)): # filtrando os números que são muito próximos
        if lista[i] - lista[i-1] > 0.2: 
            l_linha.append(lista[i])
    return l_linha

def gama(t): # função gama
    return (6*math.cos(t) - 7*math.cos(3*t)), (6*math.sin(t) - 7*math.sin(3*t))

def gama_linha(t): # derivada de gama
    return (21*math.sin(3*t) - 6*math.sin(t)), (6*math.cos(t) - 21*math.cos(3*t))

dominio = np.linspace(0, 2*math.pi, 10**3) # domínio da função gama
pontos_na_vertical = [] # lista para armazenar os pontos em que Y da derivada é zero

for t in dominio: 
    t = round(t, 2) # arredondando para 2 casas decimais
    x, y = gama_linha(t) # derivada de gama
    if round(y) == 0: # se Y da derivada for zero
        pontos_na_vertical.append(t) # adiciona o ponto na lista
pontos_na_vertical = remove_repetidos(pontos_na_vertical) # removendo os repetidos

print(f'Raíz em Y encontradas em: {pontos_na_vertical}')
print(f'Número de raízes encontradas: {len(pontos_na_vertical)}')

for ponto in pontos_na_vertical: # imprimindo os pontos em que X da derivada é zero
    print(f'X = {round(gama(ponto)[0], 3)} | Y = {round(gama(ponto)[1], 3)}')