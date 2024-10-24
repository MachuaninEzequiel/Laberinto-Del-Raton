import pygame

# Definir colores
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Definir dimensiones en una escala menor
CELL_SIZE = 30  # Tamaño de la celda en milímetros
WALL_HEIGHT = 5  # Altura de la pared en milímetros
WALL_THICKNESS = 1  # Grosor de la pared en milímetros

# Dimensiones del laberinto
LABYRINTH_WIDTH = 16
LABYRINTH_HEIGHT = 16

# Inicializar Pygame
pygame.init()

# Configurar ventana
WIN_WIDTH = LABYRINTH_WIDTH * CELL_SIZE
WIN_HEIGHT = LABYRINTH_HEIGHT * CELL_SIZE
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Laberinto")

# Dibujar suelo
WIN.fill(BLACK)

# Dibujar paredes exteriores
pygame.draw.rect(WIN, WHITE, (0, 0, WIN_WIDTH, WALL_THICKNESS))  # Pared superior
pygame.draw.rect(WIN, WHITE, (0, 0, WALL_THICKNESS, WIN_HEIGHT))  # Pared izquierda
pygame.draw.rect(WIN, WHITE, (0, WIN_HEIGHT - WALL_THICKNESS, WIN_WIDTH, WALL_THICKNESS))  # Pared inferior
pygame.draw.rect(WIN, WHITE, (WIN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WIN_HEIGHT))  # Pared derecha

# Dibujar paredes interiores
for row in range(LABYRINTH_HEIGHT):
    for col in range(LABYRINTH_WIDTH):
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        # Dibujar pared superior
        if row == 0:
            pygame.draw.rect(WIN, WHITE, (x, y, CELL_SIZE, WALL_THICKNESS))
        # Dibujar pared izquierda
        if col == 0:
            pygame.draw.rect(WIN, WHITE, (x, y, WALL_THICKNESS, CELL_SIZE))
        # Dibujar pared inferior
        if row == LABYRINTH_HEIGHT - 1:
            pygame.draw.rect(WIN, WHITE, (x, y + CELL_SIZE - WALL_THICKNESS, CELL_SIZE, WALL_THICKNESS))
        # Dibujar pared derecha
        if col == LABYRINTH_WIDTH - 1:
            pygame.draw.rect(WIN, WHITE, (x + CELL_SIZE - WALL_THICKNESS, y, WALL_THICKNESS, CELL_SIZE))

# Dibujar paredes interiores verticales
for row in range(LABYRINTH_HEIGHT - 1):
    for col in range(LABYRINTH_WIDTH - 1):
        x = col * CELL_SIZE + WALL_THICKNESS
        y = row * CELL_SIZE + WALL_THICKNESS
        pygame.draw.rect(WIN, WHITE, (x, y, WALL_THICKNESS, CELL_SIZE - WALL_THICKNESS))

# Dibujar paredes interiores horizontales
for row in range(LABYRINTH_HEIGHT - 1):
    for col in range(LABYRINTH_WIDTH - 1):
        x = col * CELL_SIZE + WALL_THICKNESS
        y = row * CELL_SIZE + WALL_THICKNESS
        pygame.draw.rect(WIN, WHITE, (x, y, CELL_SIZE - WALL_THICKNESS, WALL_THICKNESS))

# Dibujar paredes superiores de altura WALL_HEIGHT
for row in range(LABYRINTH_HEIGHT):
    for col in range(LABYRINTH_WIDTH - 1):
        x = col * CELL_SIZE + WALL_THICKNESS
        y = row * CELL_SIZE
        pygame.draw.rect(WIN, ORANGE, (x, y, CELL_SIZE - WALL_THICKNESS, WALL_HEIGHT))

# Dibujar paredes laterales de altura WALL_HEIGHT
for row in range(LABYRINTH_HEIGHT - 1):
    for col in range(LABYRINTH_WIDTH):
        x = col * CELL_SIZE
        y = row * CELL_SIZE + WALL_THICKNESS
        pygame.draw.rect(WIN, ORANGE, (x, y, WALL_HEIGHT, CELL_SIZE - WALL_THICKNESS))

# Dibujar meta (puerta)
meta_x = (LABYRINTH_WIDTH // 2) * CELL_SIZE + WALL_THICKNESS
meta_y = (LABYRINTH_HEIGHT // 2) * CELL_SIZE
pygame.draw.rect(WIN, BLACK, (meta_x, meta_y, CELL_SIZE - WALL_THICKNESS, WALL_THICKNESS))

# Dibujar marca de la meta en el suelo
pygame.draw.line(WIN, WHITE, (meta_x, meta_y + WALL_THICKNESS // 2), (meta_x + CELL_SIZE - WALL_THICKNESS, meta_y + WALL_THICKNESS // 2), 2)

# Actualizar la ventana
pygame.display.update()

# Mantener la ventana abierta hasta que se cierre manualmente
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Cerrar Pygame
pygame.quit()
