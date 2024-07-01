#include <cstdint>
#include <ctime>
#include <iostream>
#include <random>
#include <unordered_set>
#include <sstream>
#include <fstream>
#include <vector>
#include <algorithm>

using gener = std::uniform_int_distribution<int64_t>;

std::string cab = "### Simulacion ";
std::string sa = "a=";
std::string sm = "m=";
std::string sx0 = "X0=";

std::vector<int64_t> generados{};

int64_t congruencialMultiplicativo(int64_t a, int64_t m, int64_t X0) {
    return (a * X0) % m;
}

// Función para calcular el período
int64_t calcularPeriodo(int64_t a, int64_t m, int64_t X0) {
    std::unordered_set<int64_t> generados;
    int64_t Xn = X0;
    int64_t periodo = 0;

    // Generar números hasta encontrar una repetición
    while (generados.find(Xn) == generados.end()) {
        generados.insert(Xn);
        Xn = congruencialMultiplicativo(a, m, Xn);
        printf("%ld\n", Xn);
        periodo++;
    }

    return periodo;
}

void exec(int64_t a, int64_t m, std::ofstream &file) {
    std::random_device rd;
    std::mt19937 gen(rd());

    gener distx0(0, m - 1);
    int64_t X0 = distx0(gen);

    int64_t periodo = calcularPeriodo(a, m, X0);
    
    file << sa << a << '\n';
    file << sm << m << '\n';
    file << sx0 << X0 << '\n';
    file << "Periodo: " << periodo << '\n';

    generados.push_back(periodo);
}

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());

    gener dista(1, pow(2, 20));
    gener distm(1, pow(2, 20));
    int64_t a{0};
    int64_t m{0};

    std::ofstream file;
    file.open("Resultados.md");
    if (!file.is_open()) {
        std::cerr << "Error al abrir el archivo" << std::endl;
        return 1;
    }


    for (int i = 0; i < 50; i++) {
        file << cab << i << std::endl;
        a = dista(gen);
        m = distm(gen);
        exec(a, m, file);
    }

    int64_t max = *std::max_element(generados.begin(), generados.end());
    file << "\n\n**El periodo maximo es: " << max << "**\n";
    file.close();
}