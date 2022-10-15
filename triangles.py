import random
#Establishes the size and color range (rgb 1-255) of each triangle
class Triangle:
    def __init__(self, img_width, img_height):
        x = random.randint(0, int(img_width))
        y = random.randint(0, int(img_height))
#adjusted triangle range from -50,50 to -10105 to increase evolution
        self.points = [
            (x + random.randint(-25, 25), y + random.randint(-25, 25)),
            (x + random.randint(-25, 25), y + random.randint(-25, 25)),
            (x + random.randint(-25, 25), y + random.randint(-25, 25))]
#color variation chosen for each point and color fill
        self.color = (
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256)
        )
#include self to access the attributes and methods of the class in python
        self._img_width = img_width
        self._img_height = img_height
#function returning an output statement of triangle # and color
    def __repr__(self):
        return "Triangle: %s in color %s" % (','.join([str(p) for p in self.points]), str(self.color))
#mutation parameters for triangle
    def mutate(self, sigma=1.0):
        mutations = ['shift', 'point', 'color', 'reset']
        weights = [30, 35, 30, 5]

        mutation_type = random.choices(mutations, weights=weights, k=1)[0]
#conditional statements
        if mutation_type == 'shift':
            x_shift = int(random.randint(-50, 50)*sigma)
            y_shift = int(random.randint(-50, 50)*sigma)
            self.points = [(x + x_shift, y + y_shift) for x, y in self.points]
        elif mutation_type == 'point':
            index = random.choice(list(range(len(self.points))))

            self.points[index] = (self.points[index][0] + int(random.randint(-50, 50)*sigma),
                                  self.points[index][1] + int(random.randint(-50, 50)*sigma),)
        elif mutation_type == 'color':
            self.color = tuple(
                c + int(random.randint(-50, 50)*sigma) for c in self.color
            )

            # Ensure color is within correct range
            self.color = tuple(
                min(max(c, 0), 255) for c in self.color
            )
        else:
            new_triangle = Triangle(self._img_width, self._img_height)

# include self to access the attributes and methods of the class in python
            self.points = new_triangle.points
            self.color = new_triangle.color