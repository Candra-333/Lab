import sys
import pygame
import random

pygame.init()

# Window & Grid Settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

COLORS = [RED, BLUE, GREEN, CYAN, ORANGE, PURPLE]

# Tetromino Shapes
SHAPES = [
    # I Shape
    [
        ['.....',
         '.....',
         'OOOO.',
         '.....',
         '.....'],
        ['..O..',
         '..O..',
         '..O..',
         '..O..',
         '.....']
    ],
    # T Shape
    [
        ['.....',
         '..O..',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....']
    ],
    # Z Shape
    [
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    # L Shape
    [
        ['.....',
         '..O..',
         '..O..',
         '..OO.',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....']
    ]
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    @property
    def current_rotation(self):
        return self.shape[self.rotation % len(self.shape)]


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        return Tetromino(self.width // 2 - 2, 0, shape)

    def valid_move(self, piece, x_offset, y_offset, rotation_offset):
        next_rotation = (piece.rotation + rotation_offset) % len(piece.shape)
        shape_matrix = piece.shape[next_rotation]

        for i, row in enumerate(shape_matrix):
            for j, cell in enumerate(row):
                if cell == 'O':
                    new_x = piece.x + j + x_offset
                    new_y = piece.y + i + y_offset

                    # Check boundary collisions
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False

                    # Check collision with existing blocks on the board
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        return True

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_grid)

        # Add new empty rows at the top
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])

        self.grid = new_grid
        return lines_cleared

    def lock_piece(self, piece):
        shape_matrix = piece.current_rotation
        for i, row in enumerate(shape_matrix):
            for j, cell in enumerate(row):
                if cell == 'O':
                    board_y = piece.y + i
                    board_x = piece.x + j
                    if board_y >= 0:
                        self.grid[board_y][board_x] = piece.color

        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100
        self.current_piece = self.new_piece()

        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True

    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    def draw(self, screen, x_offset, y_offset):
        # Draw board grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = (x_offset + x * GRID_SIZE, y_offset + y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
                if cell:
                    pygame.draw.rect(screen, cell, rect)
                else:
                    pygame.draw.rect(screen, (30, 30, 30), rect, 1)

        # Draw active falling piece
        if self.current_piece and not self.game_over:
            matrix = self.current_piece.current_rotation
            for i, row in enumerate(matrix):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        px = x_offset + (self.current_piece.x + j) * GRID_SIZE
                        py = y_offset + (self.current_piece.y + i) * GRID_SIZE
                        pygame.draw.rect(screen, self.current_piece.color, (px, py, GRID_SIZE - 1, GRID_SIZE - 1))


def draw_score(screen, score, x, y):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (x, y))


def draw_game_over(screen, x, y):
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over - Press Any Key", True, RED)
    screen.blit(text, (x, y))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    board_x_offset = (WIDTH - BOARD_WIDTH * GRID_SIZE) // 2
    board_y_offset = (HEIGHT - BOARD_HEIGHT * GRID_SIZE) // 2

    game = Tetris(BOARD_WIDTH, BOARD_HEIGHT)

    fall_time = 0
    fall_speed = 500  # milliseconds per drop

    while True:
        delta_time = clock.tick(60)
        fall_time += delta_time

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    game = Tetris(BOARD_WIDTH, BOARD_HEIGHT)
                else:
                    if event.key == pygame.K_LEFT and game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT and game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1
                    elif event.key == pygame.K_DOWN and game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                    elif event.key == pygame.K_UP and game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1
                    elif event.key == pygame.K_SPACE:
                        while game.valid_move(game.current_piece, 0, 1, 0):
                            game.current_piece.y += 1
                        game.lock_piece(game.current_piece)

        if fall_time >= fall_speed and not game.game_over:
            game.update()
            fall_time = 0

        game.draw(screen, board_x_offset, board_y_offset)
        draw_score(screen, game.score, 20, 20)

        if game.game_over:
            draw_game_over(screen, WIDTH // 2 - 200, HEIGHT // 2)

        pygame.display.flip()


if __name__ == '__main__':
    main()