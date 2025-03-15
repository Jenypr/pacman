import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()

# Definições de tela e cores
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 15
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Cores disponíveis para o Pac-Man
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# Carregar imagens do Pac-Man em diferentes cores
pacman_images = {
    YELLOW: pygame.image.load("images/pacman-yellow.png"),
    PURPLE: pygame.image.load("images/pacman-purple.png"),
    CYAN: pygame.image.load("images/pacman-cyan.png")
}

for color in pacman_images:
    pacman_images[color] = pygame.transform.scale(pacman_images[color], (80, 80))

# Carregar imagens dos fantasmas
ghost_images = {
    "blinky": pygame.image.load("images/blinky.png"),
    "pinky": pygame.image.load("images/pinky.png"),
    "inky": pygame.image.load("images/inky.png"),
    "clyde": pygame.image.load("images/clyde.png")
}
for ghost in ghost_images:
    ghost_images[ghost] = pygame.transform.scale(ghost_images[ghost], (40, 40))

# Variáveis do Pac-Man
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_speed = 3
direction = "RIGHT"

# Animação da boca
pacman_mouth_angle = 30
mouth_opening = True
