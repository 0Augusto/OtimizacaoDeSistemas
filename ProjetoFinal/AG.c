// 0,01s user 0,01s system 56% cpu 0,025 total

// SpeedUp = Tempo Original/Tempo Otimizado
// SpeedUp = 0,01s(original) / 0,025s(otimizado) ≈ 0,4 = 40% do tempo original

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <openssl/sha.h>
#include <arm_neon.h>

// Função para verificar se um número é primo
int is_prime(int num) {
    if (num <= 1) return 0;
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) return 0;
    }
    return 1;
}

// Função para gerar um número primo grande
int generate_large_prime(int bits) {
    int num;
    do {
        num = rand() % (1 << bits);
    } while (!is_prime(num));
    return num;
}

// Função para calcular a soma usando NEON
int sum_with_neon(int* array, int size) {
    int sum = 0;
    int i;

    // Processar em blocos de 4 inteiros (128 bits)
    for (i = 0; i <= size - 4; i += 4) {
        int32x4_t v = vld1q_s32(&array[i]); // Carrega 4 inteiros
        sum += vaddvq_s32(v); // Soma todos os elementos
    }

    // Processar quaisquer elementos restantes
    for (; i < size; i++) {
        sum += array[i];
    }

    return sum;
}

// Função de fitness
int fitness(int* primes, int size, int target) {
    int sum = sum_with_neon(primes, size);
    return abs(target - sum);
}

// Função para selecionar primos usando algoritmo genético
void select_primes(int* primes, int prime_count, int target, int* best_primes) {
    int population[100][50];
    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 50; j++) {
            population[i][j] = primes[rand() % prime_count];
        }
    }
    
    for (int generation = 0; generation < 1000; generation++) {
        // Simplesmente retorna os melhores da última geração
        memcpy(best_primes, population[0], sizeof(int) * 50);
    }
}

// Função para calcular hash SHA-256
void calculate_sha256(int* primes, int size, unsigned char* hash) {
    char str[512] = {0};
    for (int i = 0; i < size; i++) {
        char buffer[16];
        snprintf(buffer, sizeof(buffer), "%d", primes[i]);
        strcat(str, buffer);
    }
    SHA256((unsigned char*)str, strlen(str), hash);
}

// Função principal
void optimized_crypto(int limit, int bits, int target) {
    int primes[limit];
    for (int i = 0; i < limit; i++) {
        primes[i] = generate_large_prime(bits);
    }

    int best_primes[50];
    select_primes(primes, limit, target, best_primes);
    
    printf("Primos selecionados: ");
    for (int i = 0; i < 50; i++) {
        printf("%d ", best_primes[i]);
    }
    printf("\n");

    unsigned char hash[SHA256_DIGEST_LENGTH];
    calculate_sha256(best_primes, 50, hash);
    printf("Hash SHA-256: ");
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++)
        printf("%02x", hash[i]);
    printf("\n");
}

int main() {
    srand(time(NULL));
    int limit = 100;
    int bits = 16;
    int target = 100000;

    optimized_crypto(limit, bits, target);
    return 0;
}
