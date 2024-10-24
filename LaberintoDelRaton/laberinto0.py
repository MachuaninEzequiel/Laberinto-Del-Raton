import random

class Maze:
    # Bit mapped directions
    class Direction:
        N = 1 << 0
        E = 1 << 1
        S = 1 << 2
        W = 1 << 3

    # Wall configuration at constructor
    class WallInit:
        NoneType = 0
        Perimeter = 1
        Full = 2

    # Possible wall configurations
    Cell_0 = 0
    Cell_N = 1
    Cell_E = 2
    Cell_S = 4
    Cell_W = 8
    Cell_NE = 3
    Cell_NS = 5
    Cell_NW = 9
    Cell_ES = 6
    Cell_EW = 10
    Cell_SW = 12
    Cell_NES = 7
    Cell_NEW = 11
    Cell_NSW = 13
    Cell_ESW = 14
    Cell_NESW = 15

    def __init__(self, cols, rows, init):
        self.cols = cols
        self.rows = rows
        self.count = rows * cols
        self.cells = [0] * self.count

        if init == self.WallInit.Perimeter:
            br = rows - 1
            for c in range(cols):
                self[c, 0] |= self.Direction.N
                self[c, br] |= self.Direction.S

            bc = cols - 1
            for r in range(rows):
                self[0, r] |= self.Direction.W
                self[bc, r] |= self.Direction.E
        elif init == self.WallInit.Full:
            for r in range(rows):
                for c in range(cols):
                    self[r, c] = self.Cell_NESW

    def __getitem__(self, index):
        row, col = index
        return self.cells[(row * self.cols) + col]

    def __setitem__(self, index, value):
        row, col = index
        self.cells[(row * self.cols) + col] = value

    def is_open(self, col, row, wall):
        cell = self[col, row]
        mask = wall
        return (cell & mask) == 0

    def set_wall(self, col, row, wall):
        self[col, row] |= wall
        if wall == self.Direction.N and row > 0:
            self.set_wall(col, row - 1, self.Direction.S)
        elif wall == self.Direction.W and col > 0:
            self.set_wall(col - 1, row, self.Direction.E)
        elif wall == self.Direction.S and row < self.rows - 1:
            self.set_wall(col, row + 1, self.Direction.N)
        elif wall == self.Direction.E and col < self.cols - 1:
            self.set_wall(col + 1, row, self.Direction.W)

    def unset_wall(self, col, row, wall):
        self[col, row] &= ~wall
        if wall == self.Direction.N and row > 0:
            self.unset_wall(col, row - 1, self.Direction.S)
        elif wall == self.Direction.W and col > 0:
            self.unset_wall(col - 1, row, self.Direction.E)
        elif wall == self.Direction.S and row < self.rows - 1:
            self.unset_wall(col, row + 1, self.Direction.N)
        elif wall == self.Direction.E and col < self.cols - 1:
            self.unset_wall(col + 1, row, self.Direction.W)

    def __str__(self):
        return "\n".join(self.str_lines(4, 2, True))

    def str_lines(self, cell_size_width, cell_size_height, ab_marks):
        lines = []
        buffer = [[' ' for _ in range((self.cols * cell_size_width) + 1)] for _ in range((self.rows * cell_size_height) + 1)]

        for r in range(self.rows):
            for c in range(self.cols):
                self.build_string_cell(buffer, c, r, cell_size_width, cell_size_height)

        if ab_marks:
            buffer[cell_size_width // 2][self.cols * cell_size_height - 1] = 'S'
            buffer[(self.cols - 1) * cell_size_width // 2][(self.rows - 1) * cell_size_height // 2] = 'G'
            buffer[(self.cols - 1) * cell_size_width // 2][(self.rows + 1) * cell_size_height // 2] = 'G'
            buffer[(self.cols + 1) * cell_size_width // 2][(self.rows - 1) * cell_size_height // 2] = 'G'
            buffer[(self.cols + 1) * cell_size_width // 2][(self.rows + 1) * cell_size_height // 2] = 'G'
            buffer[self.cols * cell_size_width // 2][self.rows * cell_size_height // 2] = 'o'

        for r in range(self.rows):
            for rr in range(cell_size_height + 1):
                line_buffer = ""
                for c in range((self.cols * cell_size_width) + 1):
                    line_buffer += buffer[c][r * cell_size_height + rr]
                lines.append(line_buffer)

        return lines

    def build_string_cell(self, buffer, col, row, cell_size_width, cell_size_height):
        x = col * cell_size_width
        y = row * cell_size_height

        if not self.is_open(col, row, self.Direction.N):
            buffer[x][y] = 'o'
            for c in range(1, cell_size_width):
                buffer[x + c][y] = '-'
            buffer[x + cell_size_width][y] = 'o'

        if not self.is_open(col, row, self.Direction.S):
            buffer[x][y + cell_size_height] = 'o'
            for c in range(1, cell_size_width):
                buffer[x + c][y + cell_size_height] = '-'
            buffer[x + cell_size_width][y + cell_size_height] = 'o'

        if not self.is_open(col, row, self.Direction.W):
            buffer[x][y] = 'o'
            for c in range(1, cell_size_height):
                buffer[x][y + c] = '|'
            buffer[x][y + cell_size_height] = 'o'

        if not self.is_open(col, row, self.Direction.E):
            buffer[x + cell_size_width][y] = 'o'
            for c in range(1, cell_size_height):
                buffer[x + cell_size_width][y + c] = '|'
            buffer[x + cell_size_width][y + cell_size_height] = 'o'

    def depth_first_generate(self, start_col, start_row, straightforward=0.0):
        visited = [[False] * self.cols for _ in range(self.rows)]

        def visit_rec(col, row, previous):
            visited[col][row] = True
            pending = [self.Direction.N, self.Direction.E, self.Direction.S, self.Direction.W]
            previous_elegible = True

            while pending:
                direction = None

                if previous_elegible and random.random() < straightforward:
                    direction = previous
                    pending.remove(direction)
                    previous_elegible = False
                else:
                    index = random.randint(0, len(pending) - 1)
                    direction = pending.pop(index)

                c, r = col, row

                if direction == self.Direction.N:
                    r -= 1
                elif direction == self.Direction.E:
                    c += 1
                elif direction == self.Direction.S:
                    r += 1
                elif direction == self.Direction.W:
                    c -= 1

                if 0 <= c < self.cols and 0 <= r < self.rows and not visited[c][r]:
                    self.unset_wall(col, row, direction)
                    visit_rec(c, r, direction)

        visit_rec(start_col, start_row, self.Direction.N)


# Example usage:
maze = Maze(5, 5, Maze.WallInit.Full)
maze.depth_first_generate(0, 0, straightforward=0.1)
print(maze)