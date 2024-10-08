import numpy as np
from scipy.optimize import linprog

class BranchAndBound:
    def __init__(self, c, A, b, int_vars):
        self.c = c                # Coeficientes da função objetivo
        self.A = A                # Matriz de restrições
        self.b = b                # Vetor de termos constantes
        self.int_vars = int_vars  # Índices das variáveis inteiras
        self.best_solution = None # Melhor solução encontrada
        self.best_obj_value = -np.inf  # Melhor valor objetivo encontrado
        self.subproblems = []     # Lista de subproblemas
    
    def solve_relaxed_lp(self):
        # Resolve o problema de Programação Linear relaxado (sem restrições de integralidade)
        result = linprog(c=self.c, A_ub=self.A, b_ub=self.b, method='highs')
        return result
    
    def branch(self, subproblem):
        # Método para fazer o branching (dividir o problema)
        frac_var_index = subproblem['frac_var']
        lower_bound = np.floor(subproblem['solution'][frac_var_index])
        upper_bound = np.ceil(subproblem['solution'][frac_var_index])
        
        # Subproblema 1 (variável inferior)
        subproblem_1 = subproblem.copy()
        subproblem_1['b'] = np.append(subproblem_1['b'], lower_bound)
        subproblem_1['A'] = np.append(subproblem_1['A'], [[0]], axis=1)  # Acrescenta restrição para a variável
        subproblem_1['int_vars'] = [frac_var_index] # Restringe para inteiro
        
        # Subproblema 2 (variável superior)
        subproblem_2 = subproblem.copy()
        subproblem_2['b'] = np.append(subproblem_2['b'], upper_bound)
        subproblem_2['A'] = np.append(subproblem_2['A'], [[0]], axis=1)
        subproblem_2['int_vars'] = [frac_var_index]
        
        self.subproblems.append(subproblem_1)
        self.subproblems.append(subproblem_2)
        
    def solve(self):
        # Inicia o algoritmo Branch and Bound
        relaxed_result = self.solve_relaxed_lp()
        
        if relaxed_result.success:
            solution = relaxed_result.x
            obj_value = relaxed_result.fun
            
            if self.is_integer(solution):
                # Se a solução já for inteira, atualiza o melhor valor
                self.best_solution = solution
                self.best_obj_value = obj_value
            else:
                # Caso não seja inteira, realiza o branching
                frac_var = self.get_fractional_var(solution)
                self.branch({
                    'solution': solution,
                    'obj_value': obj_value,
                    'frac_var': frac_var,
                    'A': self.A,
                    'b': self.b,
                    'int_vars': self.int_vars
                })
            
            # Resolve os subproblemas
            while self.subproblems:
                subproblem = self.subproblems.pop()
                sub_result = self.solve_relaxed_lp(subproblem)
                
                if sub_result.success:
                    solution = sub_result.x
                    obj_value = sub_result.fun
                    
                    if self.is_integer(solution):
                        if obj_value > self.best_obj_value:
                            self.best_solution = solution
                            self.best_obj_value = obj_value
        return self.best_solution, self.best_obj_value

    def is_integer(self, solution):
        # Verifica se todas as variáveis inteiras são inteiras
        for i in self.int_vars:
            if not np.isclose(solution[i], np.round(solution[i])):
                return False
        return True
    
    def get_fractional_var(self, solution):
        # Encontra a variável com valor fracionário mais próximo de 0.5
        for i in self.int_vars:
            if not np.isclose(solution[i], np.round(solution[i])):
                return i
        return None


# Definição de um exemplo de problema

c = np.array([1, 2, 3])  # Coeficientes da função objetivo
A = np.array([[1, 2, 1], [3, 2, 1]])  # Matriz de restrições
b = np.array([4, 6])  # Vetor do lado direito das restrições
int_vars = [0, 2]  # Índices das variáveis inteiras

# Instanciando o algoritmo de Branch and Bound
bb = BranchAndBound(c, A, b, int_vars)

# Resolvendo o problema
solution, obj_value = bb.solve()

print("Solução ótima:", solution)
print("Valor da função objetivo:", obj_value)

