import random
import pygame

# Dimensiones del laberinto y tamaño de las celdas
LABYRINTH_WIDTH = 10
LABYRINTH_HEIGHT = 10
CELL_SIZE = 40
LABYRINTH_X = 20
LABYRINTH_Y = 20

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clase que representa una celda en el laberinto
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = LABYRINTH_X + col * CELL_SIZE
        self.y = LABYRINTH_Y + row * CELL_SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.path = False

    @property
    def center(self):
        return (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2)

    @property
    def top_left(self):
        return (self.x, self.y)

    @property
    def top_right(self):
        return (self.x + CELL_SIZE, self.y)

    @property
    def bottom_left(self):
        return (self.x, self.y + CELL_SIZE)

    @property
    def bottom_right(self):
        return (self.x + CELL_SIZE, self.y + CELL_SIZE)

    def remove_wall(self, other):
        if self.row == other.row:
            if self.col - other.col == 1:
                self.walls["left"] = False
                other.walls["right"] = False
            elif self.col - other.col == -1:
                self.walls["right"] = False
                other.walls["left"] = False
        elif self.col == other.col:
            if self.row - other.row == 1:
                self.walls["top"] = False
                other.walls["bottom"] = False
            elif self.row - other.row == -1:
                self.walls["bottom"] = False
                other.walls["top"] = False

    def get_neighbors(self, grid):
        neighbors = []
        if self.row > 0:
            neighbors.append(grid[self.row - 1][self.col])
        if self.row < LABYRINTH_HEIGHT - 1:
            neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0:
            neighbors.append(grid[self.row][self.col - 1])
        if self.col < LABYRINTH_WIDTH - 1:
            neighbors.append(grid[self.row][self.col + 1])
        return neighbors

# Función para dibujar el laberinto
def draw_maze(grid):
    WIN.fill(WHITE)
    for row in grid:
        for cell in row:
            if cell.visited:
                pygame.draw.rect(WIN, WHITE, (cell.x, cell.y, CELL_SIZE, CELL_SIZE))
                if cell.walls["top"]:
                    pygame.draw.line(WIN, BLACK, cell.top_left, cell.top_right)
                if cell.walls["right"]:
                    pygame.draw.line(WIN, BLACK, cell.top_right, cell.bottom_right)
                if cell.walls["bottom"]:
                    pygame.draw.line(WIN, BLACK, cell.bottom_left, cell.bottom_right)
                if cell.walls["left"]:
                    pygame.draw.line(WIN, BLACK, cell.top_left, cell.bottom_left)
            if cell.path:
                pygame.draw.circle(WIN, GRAY, cell.center, 2)  # Dibujar el camino recorrido

# Función para generar el laberinto utilizando Recursive Backtracking
def generate_maze(grid, current_cell):
    current_cell.visited = True

    # Obtener las celdas vecinas no visitadas
    neighbors = [cell for cell in current_cell.get_neighbors(grid) if not cell.visited]

    # Si hay celdas vecinas no visitadas
    while neighbors:
        next_cell = random.choice(neighbors)
        current_cell.remove_wall(next_cell)
        generate_maze(grid, next_cell)
        neighbors = [cell for cell in current_cell.get_neighbors(grid) if not cell.visited]

# Función para mover el ratón de forma autónoma
def move_mouse(grid, current_cell):
    neighbors = [cell for cell in current_cell.get_neighbors(grid) if not any(cell.walls.values())]

    if neighbors:
        next_cell = random.choice(neighbors)
        current_cell.path = False
        next_cell.path = True
        return next_cell
    else:
        return current_cell

# Crear ventana de Pygame
pygame.init()
WIN_WIDTH = LABYRINTH_X * 2 + LABYRINTH_WIDTH * CELL_SIZE
WIN_HEIGHT = LABYRINTH_Y * 2 + LABYRINTH_HEIGHT * CELL_SIZE
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Laberinto")

# Crear matriz de celdas
grid = [[Cell(row, col) for col in range(LABYRINTH_WIDTH)] for row in range(LABYRINTH_HEIGHT)]

# Generar laberinto
generate_maze(grid, grid[-1][-1])  # Comenzar desde la esquina inferior derecha
grid[LABYRINTH_HEIGHT // 2][LABYRINTH_WIDTH // 2].path = True  # Marcar celda de salida en el medio del laberinto

# Dibujar laberinto
draw_maze(grid)

# Dibujar celda de inicio y celda de salida
start_cell = grid[-1][0]  # Celda de arranque en la esquina inferior izquierda
end_cell = grid[LABYRINTH_HEIGHT // 2][LABYRINTH_WIDTH // 2]  # Celda de salida en el medio del laberinto
pygame.draw.rect(WIN, RED, (start_cell.x, start_cell.y, CELL_SIZE, CELL_SIZE))  # Pintar la celda de arranque de rojo
pygame.draw.rect(WIN, GREEN, (end_cell.x, end_cell.y, CELL_SIZE, CELL_SIZE))  # Pintar la celda de salida de verde

# Posición inicial del ratón (esquina inferior izquierda)
mouse_cell = grid[-1][0]

# Mantener abierta la ventana hasta que el ratón llegue a la celda de salida
running = True
clock = pygame.time.Clock()  # Para limitar la velocidad de actualización
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.time.delay(100)  # Retraso para una mejor visualización
    
    mouse_cell = move_mouse(grid, mouse_cell)
    
    draw_maze(grid)
    
    # Dibujar el ratón como un punto negro
    pygame.draw.circle(WIN, BLACK, mouse_cell.center, 5)
    
    pygame.display.update()
    clock.tick(10)  # Limitar la velocidad de actualización a 10 FPS

    print(f"Ratón en la celda: ({mouse_cell.row}, {mouse_cell.col})")  # Imprimir la posición actual del ratón

pygame.quit()