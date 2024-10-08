# 468,91s user 1,20s system 99% cpu 7:51,21 total

# SpeedUp = Tempo Original/Tempo Otimizado
# SpeedUp = 468,91s (original) / 300s (otimizado) ≈ 1,563

import random
import hashlib
from sympy import isprime
from sympy import nextprime

# Função para verificar se um número é um primo absoluto (número de Mersenne)
def primo_absoluto(num):
    p = 1
    while (2**p - 1) < num:
        if (2**p - 1) == num and isprime(p):
            return True
        p += 1
    return False

# Função para gerar números primos grandes
def gerar_primo_grande(bits):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

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
            pai = random.choice(populacao[:50])
            mae = random.choice(populacao[:50])
            filho = pai[:len(pai)//2] + mae[len(mae)//2:]
            if random.random() < 0.1:  # 10% chance de mutação
                filho[random.randint(0, len(filho)-1)] = random.choice(primos)
            nova_populacao.append(filho)
        populacao = nova_populacao
    return populacao[0]

# Função para calcular o hash SHA-256 de uma lista de números
def calcular_hash(primos):
    numeros_str = ''.join(map(str, sorted(primos)))
    return hashlib.sha256(numeros_str.encode()).hexdigest()

# Implementação do algoritmo RSA otimizado
def gerar_chaves_rsa(primo1, primo2):
    n = primo1 * primo2
    phi_n = (primo1 - 1) * (primo2 - 1)
    e = 65537  # Comummente usado
    # Calculando d usando o Algoritmo de Euclides Estendido
    d = pow(e, -1, phi_n)
    return (n, e), (n, d)  # Chave pública e privada

# Função principal para gerar a criptografia
def criptografia_otimizada(limite, bits, target):
    primos = [gerar_primo_grande(bits) for _ in range(limite)]

    # Selecionando os melhores primos através do algoritmo genético
    melhores_primos = selecionar_primos(primos, target)
    print(f"Primos selecionados: {melhores_primos}")
    print(f"Fitness final: {fitness(melhores_primos, target)}")
    print(f"Hash SHA-256: {calcular_hash(melhores_primos)}")

    # Gerando as chaves RSA
    if len(melhores_primos) >= 2:
        chave_publica, chave_privada = gerar_chaves_rsa(melhores_primos[0], melhores_primos[1])
        print(f"Chave pública: {chave_publica}")
        print(f"Chave privada: {chave_privada}")
    else:
        print("Não há primos suficientes para gerar as chaves RSA.")

# Parâmetros para o sistema
limite_superior = 100  # Número de primos a gerar
bits = 2048  # Tamanho dos primos
alvo_criptografico = 100000  # Alvo para o algoritmo genético

criptografia_otimizada(limite_superior, bits, alvo_criptografico)
