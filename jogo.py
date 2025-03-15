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
    ghost_timer += 1  # Incrementa o contador de frames
    
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



def check_collision(pacman_x, pacman_y):
    for ghost in ghosts:
        if abs(pacman_x - ghost["x"]) < CELL_SIZE and abs(pacman_y - ghost["y"]) < CELL_SIZE:
            return True
    return False


def game_over_screen(score):
    screen.fill(BLACK)

    font = pygame.font.Font(None, 50)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, YELLOW)
    restart_text = font.render("Pressione ENTER para jogar:", True, WHITE)
    quit_text = font.render("Pressione Q para sair:", True, WHITE)
    

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT * 2 // 3 + 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Reiniciar sem mostrar a tela inicial
                    main(skip_intro=True)
                elif event.key == pygame.K_q:  # Fechar o jogo
                    pygame.quit()
                    sys.exit()
                    
# Variável de pontuação
score = 0

def show_start_screen():
    screen.fill(BLACK)

    # Carregar imagem do topo
    logo = pygame.image.load("images/pacman-logo-1.png")
    logo = pygame.transform.scale(logo, (300, 150))  # Ajuste o tamanho se necessário
    logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    
    # Texto "Pressione Enter para jogar"
    font = pygame.font.Font(None, 36)
    text = font.render("Pressione ENTER para jogar", True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # Texto "Desenvolvido por Jenyffer Danily"
    dev_text = font.render("Desenvolvido por Jenyffer Danily", True, WHITE)
    dev_text_rect = dev_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    
    # Exibir elementos na tela
    screen.blit(logo, logo_rect)
    screen.blit(text, text_rect)
    screen.blit(dev_text, dev_text_rect)
    pygame.display.flip()
    
    # Esperar o jogador pressionar Enter
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                 game_over_screen
                waiting = False

def draw_skin_selection():
    font = pygame.font.Font(None, 36)
    text = font.render("Escolha a skin do Pac-Man:", True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    
    colors = [YELLOW, PURPLE, CYAN]
    color_rects = []
    
    for i, color in enumerate(colors):
        rect = pygame.Rect(150 + i * 120, HEIGHT // 2, 80, 80)
        color_rects.append((rect, color))
    
    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        
        for rect, color in color_rects:
            screen.blit(pacman_images[color], rect.topleft)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, color in color_rects:
                    if rect.collidepoint(event.pos):
                        return color
pacman_mouth_angle = 30  # Ângulo inicial da boca
mouth_opening = True  # Alterna entre abrir e fechar a boca

def draw_pacman(x, y, color, mouth_angle):
    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 2 - 2)
    mouth_offset = CELL_SIZE // 2 - 2
    mouth_x = x + int(math.cos(math.radians(mouth_angle)) * mouth_offset)
    mouth_y = y + int(math.sin(math.radians(mouth_angle)) * mouth_offset)
    pygame.draw.polygon(screen, BLACK, [(x, y), (mouth_x, mouth_y), (x + int(math.cos(math.radians(-mouth_angle)) * mouth_offset), y + int(math.sin(math.radians(-mouth_angle)) * mouth_offset))])

def draw_grid():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 5)

def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def is_valid_move(x, y):
    global score
    col, row = x // CELL_SIZE, y // CELL_SIZE
    if grid[row][col] == 1:
        return False
    elif grid[row][col] == 2:
        grid[row][col] = 0
        score += 10
    return True

def main(skip_intro=False):
    global score
    score = 0  # Resetar pontuação ao reiniciar o jogo

    if not skip_intro:
        show_start_screen()  # Só exibe a tela inicial se `skip_intro` for False

    selected_color = draw_skin_selection()  # Escolher skin antes de resetar
    reset_game()  # Resetar o jogo antes de começar
    pacman_x, pacman_y = CELL_SIZE, CELL_SIZE
    pacman_speed = CELL_SIZE
    mouth_angle = 30
    mouth_closing = True
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_score()
        draw_ghosts()
        move_ghosts(pacman_x, pacman_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        new_x, new_y = pacman_x, pacman_y

        if keys[pygame.K_LEFT]:
            new_x -= pacman_speed
        if keys[pygame.K_RIGHT]:
            new_x += pacman_speed
        if keys[pygame.K_UP]:
            new_y -= pacman_speed
        if keys[pygame.K_DOWN]:
            new_y += pacman_speed

        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and is_valid_move(new_x, new_y):
            pacman_x, pacman_y = new_x, new_y

        draw_pacman(pacman_x + CELL_SIZE // 2, pacman_y + CELL_SIZE // 2, selected_color, mouth_angle)

        if check_collision(pacman_x, pacman_y):
            game_over_screen(score)  # Agora, a tela de game over segura o jogo até escolher

        if mouth_closing:
            mouth_angle -= 5
            if mouth_angle <= 5:
                mouth_closing = False
        else:
            mouth_angle += 5
            if mouth_angle >= 30:
                mouth_closing = True
        pygame.display.flip()
        
        draw_pacman(pacman_x + CELL_SIZE // 2, pacman_y + CELL_SIZE // 2, selected_color, mouth_angle)
        # Verifica colisão
        if check_collision(pacman_x, pacman_y):
            if game_over_screen(score):
                main()  # Reinicia o jogo
            else:
                running = False
        if mouth_closing:
            mouth_angle -= 5
            if mouth_angle <= 5:
                mouth_closing = False
        else:
            mouth_angle += 5
            if mouth_angle >= 30:
                mouth_closing = True
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()