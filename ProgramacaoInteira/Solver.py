from scipy.optimize import linprog

def solve_gasoline_problem():
    # Coeficientes da função objetivo (lucro)
    c = [-0.30, -0.25, -0.20]  # Negativo porque linprog minimiza

    # Coeficientes das restrições (as inequações são expressas como Ax <= b)
    A = [
        [0.22, 0.52, 0.74],   # Restrição de Pura (pura <= 9,6)
        [0.50, 0.34, 0.20],   # Restrição de Octana (octana <= 4,8)
        [0.28, 0.14, 0.06],   # Restrição de Aditivo (aditivo <= 2,2)
        [-1, 0, 16],          # Restrição: x3 >= 16 * x1  -> -x1 + x3 >= 0
        [0, -1, 0]            # Restrição: x2 <= 0,6
    ]

    # Lado direito das restrições (valores máximos dos recursos)
    b = [9.6, 4.8, 2.2, 0, 0.6]

    # Limitação das variáveis: x1, x2, x3 >= 0
    bounds = [(0, None), (0, None), (0, None)]  # Variáveis não negativas

    # Resolvendo o problema de Programação Linear usando linprog
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    # Verifica se o resultado foi bem-sucedido
    if result.success:
        # Resultado: quantidades ótimas de gasolina verde, azul e comum
        x1, x2, x3 = result.x
        lucro_maximo = -result.fun  # Valor positivo do lucro
        print("Solução ótima encontrada:")
        print(f"Gasolina verde (milhões de litros): {x1:.2f}")
        print(f"Gasolina azul (milhões de litros): {x2:.2f}")
        print(f"Gasolina comum (milhões de litros): {x3:.2f}")
        print(f"Lucro máximo: ${lucro_maximo:.2f}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Executando o solver
solve_gasoline_problem()

