import pygame
import sys
from math import ceil

from Map import Map


class Game:

    def __init__(self, map, p_0, p):
        pygame.init()
        self.is_running = True
        # L'écran
        self.w, self.h = (1000, 500)

        # Les surfaces
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.rect = pygame.Rect((0, 0), (self.w, self.h))
        pygame.display.set_caption("Drôles de Toboggan")
        self.font = pygame.font.Font(None, 30)

        self.Map = Map(map, p_0, p, (self.w, self.h ))
        self.scroll_speed = 10

    def draw_map(self):
        there_x = False
        dict = {"X": [], "Z": []}
        for y in range(len(self.Map.map)):
            for x in range(len(self.Map.map[y])):
                char = self.Map.map[y][x]
                if char in self.Map.images:
                    if char in self.Map.double_type:
                        there_x = True
                        dict[char].append((x, y))

                    else:
                        cell_width, cell_height = self.Map.dim
                        self.screen.blit(self.Map.images[char],
                                         (x * cell_width + self.Map.top[0], y * cell_height + self.Map.top[1]))

        if there_x:
            for char, pos in dict.items():
                cell_width, cell_height = self.Map.dim
                for position in pos:
                    x, y = position
                    self.screen.blit(self.Map.images[char],
                                     (x * cell_width + self.Map.top[0], y * cell_height + self.Map.top[1]))

    def draw_props(self):
        for y in range(len(self.Map.prop)):
            for x in range(len(self.Map.prop[y])):
                txt = self.font.render(str(self.Map.prop[y][x]), True, self.Map.font_color)
                cell_width, cell_height = self.Map.dim
                self.screen.blit(txt,
                                 ((x) * cell_width + self.Map.top[0], (y - 1) * cell_height + self.Map.top[1] + 80))

    def go(self):
        # Parcourir chaque toboggan
        for y in range(len(self.Map.prop) - 1):
            for x in range(len(self.Map.prop[y])):
                if self.Map.map[y][x] == "I":
                    # Toboggan I : l'eau passe sans changement
                    self.Map.prop[y + 1][x] = self.Map.prop[y][x]
                elif self.Map.map[y][x] == "Z":
                    # Toboggan Z : échange de position
                    self.Map.prop[y + 1][x] = self.Map.prop[y][x + 1]
                    self.Map.prop[y + 1][x + 1] = self.Map.prop[y][x]
                elif self.Map.map[y][x] == "X":
                    # Toboggan X : proportion de l'eau
                    total_eau = self.Map.prop[y][x] + self.Map.prop[y][x + 1]
                    self.Map.prop[y + 1][x] = round(self.Map.p_X * total_eau, 4)
                    self.Map.prop[y + 1][x + 1] = round ((1 - self.Map.p_X) * total_eau, 4)

    def set_t(self, pos, type_):
        x, y = pos
        # On ne peut mettre un tobo sur l'extrémité
        if type_ in self.Map.double_type and len(self.Map.map[y]) - 1 <= x:
            return

        # Cas dans lequel la case précédente est un double type
        if self.Map.map[y][x - 1] in self.Map.double_type:
            self.Map.map[y][x - 1] = "I"

        # Cas dans lequel le tobo est un double (gérer les alentours
        if type_ in self.Map.double_type:

            # Gérer le cas dans lequel le tobo suivant est double
            if self.Map.map[y][x + 1] in self.Map.double_type:
                self.Map.map[y][x + 2] = "I"
            self.Map.map[y][x + 1] = 0
        if type_ in self.Map.double_type and len(self.Map.map[y]) - 1 > x:
            self.Map.map[y][x] = type_
        elif not (type_ in self.Map.double_type):
            if self.Map.map[y][x] in self.Map.double_type: self.Map.map[y][x + 1] = "I"
            self.Map.map[y][x] = type_

    def get_coor(self, pos):

        x, y = pos
        x = ceil((x - self.Map.top[0]) / self.Map.dim[0])
        y = ceil((y - self.Map.top[1]) / self.Map.dim[1])

        return x, y

    def add(self, pos, char):

        x, y = self.get_coor(pos)
        self.set_t((x - 1, y - 1), char)

    def main_loop(self):
        while self.is_running:

            # MAJ des variables
            self.Map.bottom_max = self.Map.top[1] + self.Map.dim[1] * len(self.Map.map)
            self.Map.bottom = min(self.Map.bottom_max, self.h)
            self.Map.add_rect = pygame.Rect((self.Map.top[0] - self.Map.decallage, self.Map.bottom),
                                        (self.Map.map_dim[0], self.h- self.Map.bottom ))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 5 :
                        self.Map.top[1] -= self.scroll_speed
                    elif event.button == 4 :
                        self.Map.top[1] += self.scroll_speed


            # Click droit
            if pygame.mouse.get_pressed()[0] and self.Map.map_rect.collidepoint(pygame.mouse.get_pos()):
                self.add(pygame.mouse.get_pos(), "I")
            if pygame.mouse.get_pressed()[0] and self.Map.add_rect.collidepoint(pygame.mouse.get_pos()):
                self.Map.add_height()

            # Click Gauche
            elif pygame.mouse.get_pressed()[1] and self.Map.map_rect.collidepoint(pygame.mouse.get_pos()):
                self.add(pygame.mouse.get_pos(), "X")
            if pygame.mouse.get_pressed()[2] and self.Map.map_rect.collidepoint(pygame.mouse.get_pos()):
                self.add(pygame.mouse.get_pos(), "Z")

            self.Map.map_rect = pygame.Rect(
                (self.Map.top[0] - self.Map.decallage, self.Map.top[1] - self.Map.decallage), self.Map.map_dim)

            self.go()

            self.screen.fill(self.Map.bc, rect=self.rect)
            self.screen.fill(self.Map.map_color, rect=self.Map.map_rect)
            self.screen.fill(self.Map.rect_color, rect=self.Map.add_rect)
            self.draw_map()
            self.draw_props()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game((12, 3), 1, 0.9)
    game.main_loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
