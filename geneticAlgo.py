import secrets
import collections
import random
import os

Menu = collections.namedtuple(
    'Menu', ['nama', 'protein', 'lemak', 'karbo', 'kalori'])

menu_laukHewani = [
    Menu('Ayam bakar', 23, 15, 0.1, 226),
    Menu('Lele goreng', 17.57, 14.53, 8.54, 240),
    Menu('Telur ceplok', 14, 15, 0.9, 196),
    Menu('Empal daging', 36.2, 6.90, 10.1, 248),
    Menu('Rendang sapi', 22.6, 7.9, 7.8, 193),
    Menu('Ikan Patin bakar', 17.50, 6.30, 4.30, 144),
    Menu('Ayam goreng kentucky', 32.10, 16.10, 1.10, 286),
]
menu_laukNabati = [
    Menu('Tahu bacem', 1.90, 1.47, 1.09, 24),
    Menu('Tahu goreng', 9.7, 8.50, 2.50, 115),
    Menu('Tempe goreng tepung', 3.83, 4.23, 5.85, 72),
    Menu('Tempe orek', 13.11, 8.2, 15.6, 175),
    Menu('Tempe bacem', 3.73, 3.1, 2.23, 49),
    Menu('Bakwan', 8.20, 10.20, 39, 280),
]
menu_sayur = [
    Menu('Tumis kangkung', 2.6, 2.7, 3.1, 39),
    Menu('Sayur asem', 0.7, 0.6, 5, 29),
    Menu('Sayur sop', 1.3, 2, 1, 27),
    Menu('Cap cay', 5.8, 6.30, 4.20, 97),
    Menu('Tumis buncis', 1.97, 3.45, 8.15, 65),
    Menu('Tumis jamur', 3.87, 0.36, 4.36, 28),
    Menu('Tumis kol', 1.30, 2.60, 6, 45),
]
menu_nasi = [
    Menu('Nasi merah', 2.8, 0.4, 32.5, 149),
    Menu('Nasi putih', 3, 0.3, 39.8, 180),
]


def generate_menuSatuHari():
    menu_satuHari = []

    genome_nasi = secrets.choice(menu_nasi)
    genome_hewani = secrets.choice(menu_laukHewani)
    genome_nabati = secrets.choice(menu_laukNabati)
    genome_sayur = secrets.choice(menu_sayur)

    menu_satuHari.insert(0, genome_nasi)
    menu_satuHari.insert(1, genome_hewani)
    menu_satuHari.insert(2, genome_nabati)
    menu_satuHari.insert(3, genome_sayur)

    return menu_satuHari


def generate_genome(size: int):
    genome = []
    for i in range(0, size):
        for j in range(0, 3):
            menu_satuHari = []

            genome_nasi = secrets.choice(menu_nasi)
            genome_hewani = secrets.choice(menu_laukHewani)
            genome_nabati = secrets.choice(menu_laukNabati)
            genome_sayur = secrets.choice(menu_sayur)

            menu_satuHari.insert(0, genome_nasi)
            menu_satuHari.insert(1, genome_hewani)
            menu_satuHari.insert(2, genome_nabati)
            menu_satuHari.insert(3, genome_sayur)

        genome.insert(j, menu_satuHari)
    return genome


def generate_population(size: int):
    population = []
    for i in range(size):
        population.insert(i, generate_genome(21))  # 21 = 7 hari * 3 kali makan
    return population


def generate_fitness(limit_kalori: int, population: list):
    fitness = []
    idx = 0

    for genome in population:
        fitness_pct = 0
        kalori = 0

        for hari in (genome):
            for i in hari:
                kalori += i.kalori

        fitness_pct = (kalori/limit_kalori) * 100
        if (kalori > limit_kalori):
            fitness.insert(idx, 0)
        else:
            fitness.insert(idx, fitness_pct)
        idx += 1

    return fitness


def selection(fitness: list):

    fitness_clone = fitness[:]

    parent1 = max(fitness_clone, key=float)
    parent1_index = fitness.index(parent1)

    fitness_clone.pop(parent1_index)

    parent2 = max(fitness_clone, key=float)
    parent2_index = fitness.index(parent2)

    return [parent1_index, parent2_index]


def crossover(parent1: list, parent2: list):
    child1 = parent1[:]
    child2 = parent2[:]

    crossover_point = round(len(child1)/2)

    child1[0:crossover_point] = parent2[0:crossover_point]
    child2[0:crossover_point] = parent1[0:crossover_point]

    return [child1, child2]


def mutation(child: list, mutation_rate: int):
    mutant = child[:]

    for i in range(len(mutant)):
        if(random.uniform(0, 1) <= mutation_rate):
            mutant[i] = generate_menuSatuHari()

    return mutant


def regeneration(population: list, fitness: list, mutant1: list, mutant2: list):
    min_selection1 = min(fitness, key=float)
    min_selection1_index = fitness.index(min_selection1)

    fitness.pop(min_selection1_index)
    population.pop(min_selection1_index)

    min_selection2 = min(fitness, key=float)
    min_selection2_index = fitness.index(min_selection2)

    fitness.pop(min_selection2_index)
    population.pop(min_selection2_index)

    population.append(mutant1)
    population.append(mutant2)

    return population


def main():

    # Asumsi BMR = 1565 kalori/hari * 7
    limit_kalori = 10962
    mutation_rate = 0.2
    isLooping = True

    population = generate_population(10)
    fitness = generate_fitness(limit_kalori, population)

    generation = 0
    while(isLooping):
        parents = selection(fitness)
        parent1 = population[parents[0]]
        parent2 = population[parents[1]]

        [child1, child2] = crossover(parent1, parent2)

        mutant1 = mutation(child1, mutation_rate)
        mutant2 = mutation(child2, mutation_rate)

        population = regeneration(population, fitness, mutant1, mutant2)
        fitness = generate_fitness(limit_kalori, population)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Best Fitness: {max(fitness)}")

        generation += 1
        if(max(fitness) == 100):
            isLooping = False
            population_index = fitness.index(max(fitness))
            kalori_sementara = 0

            print(f"Best solution found at {generation} generations!")
            print(f"=========================")

            # Uncomment kalau mau liat menunya
            # for i in population[population_index]:
            #     print(i)
            #     for j in i:
            #         kalori_sementara += j.kalori

            # print(kalori_sementara)


if __name__ == "__main__":
    main()
