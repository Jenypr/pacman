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

# Grade do jogo (1 = parede, 0 = caminho, 2 = pílula)
# Reinicializa a grade (reseta as pílulas)
grid = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,1,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,1,1,1,2,1,2,1,2,1,2,1,1,1,1],
        [1,1,1,1,2,1,2,2,2,1,2,1,1,1,1],
        [1,1,1,1,2,1,2,1,2,1,2,1,1,1,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,1,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
# Definição dos fantasmas
ghosts = [
    {"name": "blinky", "x": 7 * CELL_SIZE, "y": 7 * CELL_SIZE, "dx": CELL_SIZE, "dy": 0},
    {"name": "pinky", "x": 7 * CELL_SIZE, "y": 8 * CELL_SIZE, "dx": -CELL_SIZE, "dy": 0},
    {"name": "inky", "x": 6 * CELL_SIZE, "y": 7 * CELL_SIZE, "dx": 0, "dy": CELL_SIZE},
    {"name": "clyde", "x": 8 * CELL_SIZE, "y": 7 * CELL_SIZE, "dx": 0, "dy": -CELL_SIZE}
]
# Função para resetar o jogo
def reset_game():
    global pacman_x, pacman_y, score, ghosts, grid
    pacman_x, pacman_y = CELL_SIZE, CELL_SIZE
    score = 0
    
# Reinicializa a grade (reseta as pílulas)
    grid = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,1,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,1,1,1,2,1,2,1,2,1,2,1,1,1,1],
        [1,1,1,1,2,1,2,2,2,1,2,1,1,1,1],
        [1,1,1,1,2,1,2,1,2,1,2,1,1,1,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,1,1,1,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,1,1,2,1,2,1,2,1,2,1,1,2,1],
        [1,2,2,2,2,2,2,1,2,2,2,2,2,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

# Função para desenhar os fantasmas
def draw_ghosts():
    for ghost in ghosts:
        screen.blit(ghost_images[ghost["name"]], (ghost["x"], ghost["y"]))

# Variável de controle da velocidade dos fantasmas
ghost_speed = 2  # Quanto maior o número, mais devagar os fantasmas se movem
ghost_timer = 0  # Contador de frames

def move_ghosts(pacman_x, pacman_y):
    global ghosts, ghost_timer
    ghost_timer += 1  # Incrementa o contador de frame
    
    if ghost_timer % ghost_speed == 0:  # Apenas move os fantasmas a cada X ciclos do loop
        for ghost in ghosts:
            if random.randint(0, 3) == 0:
                ghost["dx"], ghost["dy"] = random.choice([
                    (CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)
                ])

            new_x = ghost["x"] + ghost["dx"]
            new_y = ghost["y"] + ghost["dy"]

            col, row = new_x // CELL_SIZE, new_y // CELL_SIZE
            if grid[row][col] != 1:  # Evita paredes
                ghost["x"], ghost["y"] = new_x, new_y