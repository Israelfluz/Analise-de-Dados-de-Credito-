# Importação da biblioteca random para gerar números aleatórios
import random

# Importação da biblioteca numpy para realizar cálculos matemáticos
import numpy

# Importação da biblioteca deap para algoritmos genéticos
from deap import base

# Importação da biblioteca deap e suas ferramentas
from deap import creator
from deap import algorithms
from deap import tools

# Importação da biblioteca matplotlib para gerar gráficos
import matplotlib.pyplot as plt

# Criação da classe
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor

# Criando a lista de produtos para análise no algoritmo de otimização        
lista_produtos = []
lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))


# Criação de listas específicas
espacos = []
valores = []
nomes = []
for produto in lista_produtos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nomes.append(produto.nome)

# Variável que mostra o limite da litragem cúbica do transporte
limite = 3

# Variáveis 
toolbox = base.Toolbox()
creator.create("FitnessMax", base.Fitness, weights=(1.0, )) # FitnessMax - quanto maior o valor do produto maior a otimização
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, n=len(espacos))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# Função de avaliação que vai indicar se uma solução é boa ou não
def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
       if individual[i] == 1:
           nota += valores[i]
           soma_espacos += espacos[i]
    if soma_espacos > limite:
        nota = 1
    return nota / 100000,


# Criando os registros dentro da biblioteca deap
toolbox.register("evaluate", avaliacao)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01)
toolbox.register("select", tools.selRoulette)


# Diferenciando onde está o método principal
if __name__ == "__main__":
    #random.seed(1)
    populacao = toolbox.population(n = 20)
    probabilidade_crossover = 1.0
    probabilidade_mutacao = 0.01
    numero_geracoes = 100
    
    # Obtendo estatísticas
    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    estatisticas.register("max", numpy.max)
    estatisticas.register("min", numpy.min)
    estatisticas.register("med", numpy.mean)
    estatisticas.register("std", numpy.std)
    
    
    # Rodando o algoritmo com os parâmetros
    populacao, info = algorithms.eaSimple(populacao, toolbox,
                                          probabilidade_crossover,
                                          probabilidade_mutacao,
                                          numero_geracoes, estatisticas)
    
    # Com essa variável melhores é possível buscar o melhor indivíduo de cada uma das gerações
    melhores = tools.selBest(populacao, 1)
    for individuo in melhores:
        print(individuo)
        print(individuo.fitness)
        #print(individuo[1])
        soma = 0
        for i in range(len(lista_produtos)):
            if individuo[i] == 1:
                soma += valores[i]
                print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                           lista_produtos[i].valor))
        print("Melhor solução: %s" % soma)
    
    # Gerando um gráfico com o acompanhamento dos valores    
    valores_grafico = info.select("max")
    plt.plot(valores_grafico)
    plt.title("Acompanhamento dos valores")
    plt.show()
    