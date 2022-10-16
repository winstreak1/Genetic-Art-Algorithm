from PIL import Image
from evol import Evolution, Population
import random
import os
from copy import deepcopy
from NatSelect import Color_Fill

# FITNESS function that measures difference from previous to current image as a score
def fitness(x: Color_Fill) -> float:
    current_fitness = x.image_diff(x.target_image)
    print(".", end='', flush=True)
    return current_fitness

#SELECTION function that selectively guesses new Color_Fill based on previous guesses
def selection(pop, maximize=False):
    evaluated_individuals = tuple(filter(lambda x: x.fitness is not None, pop))
    if len(evaluated_individuals) > 0:
        maternal = max(evaluated_individuals, key=lambda x: x.fitness if maximize else -x.fitness)
    else:
        maternal = random.choice(pop)
    paternal = random.choice(pop)
    return maternal, paternal

#function to randomly select inheritance of Color_Fill to either maternal or paternal
def choose_random(pop):
    maternal = random.choice(pop)
    paternal = random.choice(pop)
    return maternal, paternal

#GENETIC OPERATIONS: function that contains parameters that determine mutation rate

#MUTATION: mutation of a single individual
def mutate_image(x: Color_Fill, rate=0.04, swap=0.5, sigma=1) -> Color_Fill:
    x.mutate_triangles(rate=rate, swap=swap, sigma=sigma)
    return deepcopy(x)

#CROSSOVER: crossover of two individuals
def crossover(mom: Color_Fill, dad: Color_Fill):
    child_a, child_b = Color_Fill.crossover(mom, dad)

    return deepcopy(child_a)

#function to output images along with updated data while program is running
def console_output(pop, img_template="output%d.png", checkpoint_path="output") -> Population:
    avg_fitness = sum([i.fitness for i in pop.individuals])/len(pop.individuals)

    print("\nCurrent generation %d, best fitness %f, pop. avg. %f " % (pop.generation,
                                                                     pop.current_best.fitness,
                                                                     avg_fitness))
    # output conditions for image based on modulus value
    if pop.generation % 500 == 0 or pop.generation == 1:
        img = pop.current_best.chromosome.draw()
        img.save(img_template % pop.generation, 'PNG')

   # if pop.generation % 1000 == 0:
      #  pop.checkpoint(target=checkpoint_path, method='pickle')

    return pop

#conditional statement that defines location of image and output folder for image updates
if __name__ == "__main__":
    target_image_path = "./img/banksy.png"
    checkpoint_path = "./banksy/"
    image_template = os.path.join(checkpoint_path, "tri900pop20_%05d.png")
    target_image = Image.open(target_image_path).convert('RGBA')
#variable values
    num_triangles = 900
    population_size = 20

    pop = Population(chromosomes=[Color_Fill(num_triangles, target_image, background_color=(255, 255, 255)) for _ in range(population_size)],
                     eval_function=fitness, maximize=False, concurrent_workers=6)
#defines early, mid, late and final stages of evolution based on given parameters

    stage_one = (Evolution()
                .survive(fraction=0.05)
                .breed(parent_picker=selection, combiner=crossover, population_size=population_size)
                .mutate(mutate_function=mutate_image, rate=0.05, swap=0.25)
                .evaluate(lazy=False)
                .callback(console_output,
                          img_template=image_template,
                          checkpoint_path=checkpoint_path))

#pop.evolve parameters set
    pop = pop.evolve(stage_one, n=10000)
