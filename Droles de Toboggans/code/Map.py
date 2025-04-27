import pygame
from random import randint

class Map:

    def __init__(self, map, p_0, p, size):
        self.map = [[]]
        self.s_w, self.s_h = size
        self.w, self.h = map
        self.gen_map(self.w, self.h)


        # Les couleurs
        self.bc = (255,255,255) # (250, 225, 223)
        self.map_color = (255, 255, 255)
        self.font_color = (0, 0, 0)
        self.rect_color = (255,255,255)#(0,0,0)

        # Variables de la map
        self.double_type = ["X", "Z"]
        self.dim = [80, 110]
        self.map_dim = [self.w * self.dim[0], self.h * self.dim[1] + 20]
        self.images = {
            "X": pygame.image.load('./../assets/tiles/X_.PNG'),
            "I": pygame.image.load('./../assets/tiles/I.PNG'),
            "Z": pygame.image.load('./../assets/tiles/Z_.PNG'),
            0: pygame.image.load('./../assets/tiles/0.PNG')
        }


        self.top = [40, 60]
        self.decallage = 30
        self.top_max = 0
        self.bottom_max = self.top[1]+ self.dim[1] * len(self.map)
        self.bottom = min(self.bottom_max, self.s_h)

        self.map_rect = pygame.Rect((self.top[0] - self.decallage, self.top[1] - self.decallage), self.map_dim)
        self.add_rect = pygame.Rect((self.top[0]-self.decallage, self.bottom),
                                    (self.map_dim[0],self.h-self.decallage-self.dim[1]))

        # Proportions d'eau
        self.prop = [[]]
        self.gen_prop(self.w, self.h, p_0)
        self.p_X = p

    def gen_map(self, w, h):
        self.map = [["I" for i in range(w)] for k in range(h)]


        # self.cell_width = self.w // w
        # self.cell_height = self.h // h

    def gen_prop(self, w, h, p):
        self.prop = [[0 for i in range(w)] for k in range(h + 1)]
        self.prop[0][0] = p
        #for k in range(len(self.prop[0])):
        #    self.prop[0][k] = round(1/w, 3)


    def add_height(self):
        self.map.append(["I" for i in range(self.w)])
        self.h = len(self.map)
        self.map_dim = [self.w * self.dim[0], self.h * self.dim[1] + 20]
        self.prop.append([0 for i in range(self.w)])
