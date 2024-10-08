import pulp

def solve_gasoline_problem_integer():
    # Definindo o problema como um problema de maximização
    prob = pulp.LpProblem("Maximizar_Lucro_Refinaria", pulp.LpMaximize)

    # Variáveis de decisão (quantidade de gasolina verde, azul e comum)
    x1 = pulp.LpVariable('x1', lowBound=0, cat='Integer')  # Gasolina verde
    x2 = pulp.LpVariable('x2', lowBound=0, cat='Integer')  # Gasolina azul
    x3 = pulp.LpVariable('x3', lowBound=0, cat='Integer')  # Gasolina comum

    # Função objetivo (lucro)
    prob += 0.30 * x1 + 0.25 * x2 + 0.20 * x3, "Lucro Total"

    # Restrições de recursos
    prob += 0.22 * x1 + 0.52 * x2 + 0.74 * x3 <= 9.6, "Pura"
    prob += 0.50 * x1 + 0.34 * x2 + 0.20 * x3 <= 4.8, "Octana"
    prob += 0.28 * x1 + 0.14 * x2 + 0.06 * x3 <= 2.2, "Aditivo"

    # Restrições adicionais
    prob += x3 >= 16 * x1, "Gasolina Comum >= 16x1"
    prob += x2 <= 0.6 * 1000, "Gasolina Azul <= 600 mil litros"  # Convertendo para litros

    # Resolvendo o problema
    prob.solve()

    # Verificando se a solução é ótima
    if pulp.LpStatus[prob.status] == 'Optimal':
        print("Solução ótima encontrada:")
        print(f"Gasolina verde (milhões de litros): {x1.varValue:.2f}")
        print(f"Gasolina azul (milhões de litros): {x2.varValue:.2f}")
        print(f"Gasolina comum (milhões de litros): {x3.varValue:.2f}")
        print(f"Lucro máximo: ${pulp.value(prob.objective):.2f}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Executando o solver com soluções inteiras
solve_gasoline_problem_integer()
