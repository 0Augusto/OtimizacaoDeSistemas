import random
from sympy import isprime

# Função para gerar números primos abaixo de um limite
def gerar_primos(limite):
    return [num for num in range(2, limite + 1) if isprime(num)]

# Função de fitness para o algoritmo genético
def fitness(primos, target):
    return abs(target - sum(primos))

# Função para selecionar um conjunto de primos usando algoritmo genético
def selecionar_primos(primos, target, geracoes=1000):
    populacao = [random.sample(primos, len(primos) // 2) for _ in range(100)]
    for geracao in range(geracoes):
        populacao = sorted(populacao, key=lambda x: fitness(x, target))
        nova_populacao = populacao[:10]  # Seleciona os melhores
        while len(nova_populacao) < 100:
            # Crossover e mutação
            pai = random.choice(populacao[:50])
            mae = random.choice(populacao[:50])
            filho = pai[:len(pai)//2] + mae[len(mae)//2:]
            if random.random() < 0.1:  # 10% chance de mutação
                filho[random.randint(0, len(filho)-1)] = random.choice(primos)
            nova_populacao.append(filho)
        populacao = nova_populacao
    return populacao[0]

# Implementação de curto-circuito para otimizar a verificação de primos
def criptografia_otimizada(limite, target):
    primos = gerar_primos(limite)
    
    # Otimizando a seleção de primos via curto-circuito
    if primos and target > 0:  # Se houver primos e o alvo for positivo
        melhores_primos = selecionar_primos(primos, target)
        print(f"Primos selecionados: {melhores_primos}")
        print(f"Fitness final: {fitness(melhores_primos, target)}")
    else:
        print("Limite muito baixo ou alvo inválido")

# Parâmetros para o sistema
limite_superior = 1000  # Limite para geração de primos
alvo_criptografico = 5000  # Alvo para o algoritmo genético

criptografia_otimizada(limite_superior, alvo_criptografico)

