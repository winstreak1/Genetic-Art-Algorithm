import random


class Triagain:
    #declares upper and lower bounds of image or superframe
    def __init__(self, img_width, img_height):
        x = random.randint(0, int(img_width))
        y = random.randint(0, int(img_height))
#initializes each of the three points of the triangle
        self.points = [
            (x + random.randint(-50, 50), y + random.randint(-50, 50)),
            (x + random.randint(-50, 50), y + random.randint(-50, 50)),
            (x + random.randint(-50, 50), y + random.randint(-50, 50))]
#initializes color range of triangle
        self.color = (
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256)
        )
#save img_width and im g_height to new variables
        self._img_width = img_width
        self._img_height = img_height
#output triangle statement
    def __repr__(self):
        return "Trangle: %s in color %s" % (','.join([str(p) for p in self.points]), str(self.color))
#mutates each triangle based on shift, point, color, and reset
    def mutate(self, sigma=1.0):
        mutations = ['shift', 'point', 'color', 'reset']
        weights = [30, 35, 30, 5]

        mutation_type = random.choices(mutations, weights=weights, k=1)[0]
#conditional statement for shift, point and color
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

            self.points = new_triangle.points
            self.color = new_triangle.color