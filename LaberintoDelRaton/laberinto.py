import pygame
import random

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Color para la entrada (inicio)
GREEN = (0, 255, 0)  # Color para la salida

# Dimensiones del laberinto
LABYRINTH_WIDTH, LABYRINTH_HEIGHT = 30, 30

# Tamaño de cada celda del laberinto
CELL_SIZE = 20

# Tamaño de la ventana
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 720  # Ajustando el ancho de la ventana

# Posición del laberinto centrado en la ventana
LABYRINTH_X = (WINDOW_WIDTH - LABYRINTH_WIDTH * CELL_SIZE) // 2
LABYRINTH_Y = (WINDOW_HEIGHT - LABYRINTH_HEIGHT * CELL_SIZE) // 2

# Inicialización de Pygame
pygame.init()
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Laberinto")

# Clase que representa una celda en el laberinto
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = LABYRINTH_X + col * CELL_SIZE
        self.y = LABYRINTH_Y + row * CELL_SIZE
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

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

# Función principal
def main():
    grid = [[Cell(row, col) for col in range(LABYRINTH_WIDTH)] for row in range(LABYRINTH_HEIGHT)]
    current_cell = grid[0][0]
    generate_maze(grid, current_cell)

    # Establecer la entrada (inicio) en la esquina inferior izquierda
    start_cell = grid[LABYRINTH_HEIGHT - 1][0]
    start_cell.visited = True

    # Establecer la salida en las 4 celdas del medio del laberinto
    exit_cells = [grid[LABYRINTH_HEIGHT // 2][LABYRINTH_WIDTH // 2 - 1],
                  grid[LABYRINTH_HEIGHT // 2][LABYRINTH_WIDTH // 2],
                  grid[LABYRINTH_HEIGHT // 2 - 1][LABYRINTH_WIDTH // 2 - 1],
                  grid[LABYRINTH_HEIGHT // 2 - 1][LABYRINTH_WIDTH // 2]]
    for cell in exit_cells:
        cell.walls = {"top": False, "right": False, "bottom": False, "left": False}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze(grid)

        # Dibujar la entrada (inicio) en azul y la salida en verde
        pygame.draw.rect(WIN, BLUE, (start_cell.x, start_cell.y, CELL_SIZE, CELL_SIZE))
        for cell in exit_cells:
            pygame.draw.rect(WIN, GREEN, (cell.x, cell.y, CELL_SIZE, CELL_SIZE))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()