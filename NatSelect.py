from triangles import Triangle
from random import shuffle, randint
from PIL import Image, ImageDraw
from imgcompare import image_diff
import random

#class to determine how many triangles to fill, the target image to reach and background color of each triangle
class Color_Fill:
    def __init__(self, num_triangles, target_image, background_color=(0, 0, 0)):
        self._img_width, self._img_height = target_image.size
        self.triangles = [Triangle(self._img_width, self._img_height) for _ in range(num_triangles)]
        self._background_color = (*background_color, 255)
        self.target_image = target_image
#getter for background color
    @property
    def get_background_color(self):
        return self._background_color[:3]

# getter for image width
    @property
    def get_img_width(self):
        return self._img_width

# getter for image height
    @property
    def get_img_height(self):
        return self._img_height
#getter for # of triangles
    @property
    def num_triangles(self):
        return len(self.triangles)
#function to output statement for # of triangles
    def __repr__(self):
        return "Painting with %d triangles" % self.num_triangles

#function to mutate triangles
    def mutate_triangles(self, rate=0.04, swap=0.5, sigma=1.0):
        total_mutations = int(rate*self.num_triangles)
        random_indices = list(range(self.num_triangles))
        shuffle(random_indices)

        # for loop to mutate triangles through the number of random indices, i
        for i in range(total_mutations):
            index = random_indices[i]
            self.triangles[index].mutate(sigma=sigma)

# randomly swap two triangles
        if random.random() < swap:
            shuffle(random_indices)
            self.triangles[random_indices[0]], self.triangles[random_indices[1]] = self.triangles[random_indices[1]], self.triangles[random_indices[0]]
#function to create the triangles
    def draw(self, scale=1) -> Image:
        image = Image.new("RGBA", (self._img_width*scale, self._img_height*scale))
        draw = ImageDraw.Draw(image)
#conditional statement to determine color of triangle if attributes are missing
        if not hasattr(self, '_background_color'):
            self._background_color = (0, 0, 0, 255)
#create triangle of random size
        draw.polygon([(0, 0), (0, self._img_height*scale), (self._img_width*scale, self._img_height*scale), (self._img_width*scale, 0)],
                     fill=self._background_color)
#creates new_triangle, tdraw and tdraw.polygon
        for t in self.triangles:
            new_triangle = Image.new("RGBA", (self._img_width*scale, self._img_height*scale))
            tdraw = ImageDraw.Draw(new_triangle)
            tdraw.polygon([(x*scale, y*scale) for x, y in t.points], fill=t.color)

            image = Image.alpha_composite(image, new_triangle)

        return image
#defines a static method in the class Color_Fill for the function _mate_possible
    @staticmethod
    def _mate_possible(a, b) -> bool:
        return all([a.num_triangles == b.num_triangles,
                   a.get_img_width == b.get_img_width,
                   a.get_img_height == b.get_img_height])

# defines a static method in the class Color_Fill for the function crossover
    @staticmethod
    def crossover(a, b):
        if not Color_Fill._mate_possible(a, b):
            raise Exception("Cannot crossover images with different dimensions or number of triangles")
#declarations
        ab = a.get_background_color
        bb = b.get_background_color
        new_background = (int((ab[i] + bb[i])/2) for i in range(3))

        child_a = Color_Fill(0, a.target_image, background_color=new_background)
        child_b = Color_Fill(0, a.target_image, background_color=new_background)
#for loop with conditional statements return child a and child b
        for at, bt in zip(a.triangles, b.triangles):
            if randint(0, 1) == 0:
                child_a.triangles.append(at)
                child_b.triangles.append(bt)
            else:
                child_a.triangles.append(bt)
                child_b.triangles.append(at)

        return child_a, child_b
#function to output the new image
    def image_diff(self, target: Image) -> float:
        source = self.draw()

        return image_diff(source, target)

