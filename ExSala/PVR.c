#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define MAX_CITIES 100
#define INF 1000000
#define BOX_WEIGHT 10  // Peso de cada caixa em quilos
#define TOTAL_WEIGHT 550  // Quantidade total de quilos (50 caixas)

// Estrutura para armazenar a matriz de distâncias
int dist[MAX_CITIES][MAX_CITIES];

// Número de cidades
int numCities;
int totalBoxes = TOTAL_WEIGHT / BOX_WEIGHT;  // Número total de caixas

// Função para inicializar a matriz de distâncias
void initializeDistances() {
    for (int i = 0; i < numCities; i++) {
        for (int j = 0; j < numCities; j++) {
            dist[i][j] = (i == j) ? 0 : INF;  // Inicializar distâncias
        }
    }
}

// Algoritmo de Clarke-Wright para otimização de rotas partindo do centro de distribuição
void clarkeWright() {
    #pragma omp parallel for // Paralelização com OpenMP
    for (int i = 2; i <= numCities; i++) {  // Começa de 2, já que o vértice 1 é o centro de distribuição
        for (int j = i + 1; j <= numCities; j++) {
            if (dist[i][j] < INF) {
                // Calcular economia de rota e ajustar
                int saving = dist[1][i] + dist[1][j] - dist[i][j];  // Usando vértice 1 como origem
                printf("Saving for route from center (1) to (%d, %d): %d\n", i, j, saving);
                // Aqui aplicaríamos as melhorias de rota baseadas no algoritmo Clarke-Wright
            }
        }
    }
}

int main() {
    numCities = 7;  // Exemplo de número de cidades (incluindo o centro de distribuição)

    // Inicializar distâncias (exemplo fictício)
    initializeDistances();
    dist[1][2] = 6; dist[1][3] = 5; dist[1][4] = 7; dist[1][5] = 8;
    dist[1][6] = 10; dist[1][7] = 7;  // Distâncias do centro de distribuição (vértice 1)
    dist[2][3] = 5; dist[3][4] = 5; dist[4][5] = 6; dist[5][6] = 5; dist[6][7] = 8;  // Exemplo de distâncias

    // Verificar se a quantidade total de caixas (50) é transportada
    printf("Distribuindo %d caixas a partir do centro de distribuição (vértice 1).\n", totalBoxes);

    // Chamar a função de otimização
    clarkeWright();

    return 0;
}
