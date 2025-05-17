import pygame
import heapq
import random

# Game Constants
MAZE_SIZE = 9
CELL_SIZE = 64
WINDOW_SIZE = CELL_SIZE * MAZE_SIZE
COLORS = {
    'wall': (40, 40, 40),
    'path': (255, 255, 255),
    'rat': (255, 100, 100),
    'man': (100, 100, 255),
    'hole': (100, 255, 100),
    'trap': (255, 165, 0),
    'text': (0, 0, 0),
    'border': (200, 200, 200)
}


class MazeGame:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        self.game_active = True
        self.message = ""
        self.maze, self.elements = self.generate_maze()

    def generate_maze(self):
        maze = [
            [
                'W' if i in (0, MAZE_SIZE - 1) or j in (0, MAZE_SIZE - 1) else ' '
                for j in range(MAZE_SIZE)
            ]
            for i in range(MAZE_SIZE)
        ]

        # Add random walls
        for _ in range(4 + self.difficulty * 2):
            i, j = random.randint(1, MAZE_SIZE - 2), random.randint(1, MAZE_SIZE - 2)
            if maze[i][j] == ' ':
                maze[i][j] = 'W'

        # Place elements
        empty = [(i, j) for i in range(MAZE_SIZE) for j in range(MAZE_SIZE) if maze[i][j] == ' ']
        random.shuffle(empty)

        return maze, {
            'rat': empty.pop(),
            'man': empty.pop(),
            'hole': empty.pop(),
            'traps': [empty.pop() for _ in range(1 + self.difficulty)]
        }

    def check_collisions(self):
        rat_pos = self.elements['rat']
        if rat_pos == self.elements['hole']:
            self.game_active = False
            self.message = "YOU WIN! Press R to restart"
            self.difficulty = min(self.difficulty + 1, 5)
            return True
        if rat_pos in self.elements['traps']:
            self.game_active = False
            self.message = "TRAPPED! Press R to restart"
            self.difficulty = max(1, self.difficulty - 1)
            return True
        if rat_pos == self.elements['man']:
            self.game_active = False
            self.message = "CAUGHT! Press R to restart"
            self.difficulty = max(1, self.difficulty - 1)
            return True
        return False

    def a_star(self, start, end):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 4-directional

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < MAZE_SIZE and
                        0 <= neighbor[1] < MAZE_SIZE and
                        self.maze[neighbor[0]][neighbor[1]] != 'W'):

                    tentative_g = g_score.get(current, float('inf')) + 1
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + self.heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update_positions(self):
        """Move AI one step per rat move"""
        if self.game_active:
            path = self.a_star(self.elements['man'], self.elements['rat'])
            if path and len(path) > 1:
                self.elements['man'] = path[1]
            self.check_collisions()


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Maze Escape")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

game = MazeGame()


def draw_maze():
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            rect = (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if game.maze[i][j] == 'W':
                pygame.draw.rect(screen, COLORS['wall'], rect)
            else:
                pygame.draw.rect(screen, COLORS['path'], rect)

    # Grid borders
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, COLORS['border'], (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, COLORS['border'], (0, y), (WINDOW_SIZE, y))


def draw_elements():
    # Hole (diamond)
    hx, hy = game.elements['hole']
    points = [
        (hy * CELL_SIZE + CELL_SIZE // 2, hx * CELL_SIZE + 10),
        (hy * CELL_SIZE + CELL_SIZE - 10, hx * CELL_SIZE + CELL_SIZE // 2),
        (hy * CELL_SIZE + CELL_SIZE // 2, hx * CELL_SIZE + CELL_SIZE - 10),
        (hy * CELL_SIZE + 10, hx * CELL_SIZE + CELL_SIZE // 2)
    ]
    pygame.draw.polygon(screen, COLORS['hole'], points)

    # Traps (skulls)
    for tx, ty in game.elements['traps']:
        pygame.draw.circle(screen, COLORS['trap'], (ty * CELL_SIZE + CELL_SIZE // 2, tx * CELL_SIZE + CELL_SIZE // 2),
                           15)
        pygame.draw.rect(screen, (0, 0, 0),
                         (ty * CELL_SIZE + CELL_SIZE // 2 - 5, tx * CELL_SIZE + CELL_SIZE // 2 - 10, 10, 10))
        pygame.draw.circle(screen, (0, 0, 0),
                           (ty * CELL_SIZE + CELL_SIZE // 2 - 8, tx * CELL_SIZE + CELL_SIZE // 2 - 5), 2)
        pygame.draw.circle(screen, (0, 0, 0),
                           (ty * CELL_SIZE + CELL_SIZE // 2 + 8, tx * CELL_SIZE + CELL_SIZE // 2 - 5), 2)

    # Rat (triangle)
    rx, ry = game.elements['rat']
    points = [
        (ry * CELL_SIZE + CELL_SIZE // 2, rx * CELL_SIZE + 10),
        (ry * CELL_SIZE + 10, rx * CELL_SIZE + CELL_SIZE - 10),
        (ry * CELL_SIZE + CELL_SIZE - 10, rx * CELL_SIZE + CELL_SIZE - 10)
    ]
    pygame.draw.polygon(screen, COLORS['rat'], points)

    # Man (square)
    mx, my = game.elements['man']
    pygame.draw.rect(screen, COLORS['man'], (my * CELL_SIZE + 15, mx * CELL_SIZE + 15, CELL_SIZE - 30, CELL_SIZE - 30))


def draw_text():
    if game.message:
        text = font.render(game.message, True, COLORS['text'])
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        screen.blit(text, text_rect)

    diff_text = font.render(f"Difficulty: {game.difficulty}", True, COLORS['text'])
    screen.blit(diff_text, (10, 10))


running = True
move_cooldown = 0  # Movement rate control

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not game.game_active:
                game = MazeGame(difficulty=game.difficulty)

    # Arrow key movement with cooldown
    keys = pygame.key.get_pressed()
    if move_cooldown <= 0 and game.game_active:
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dx = -1
        elif keys[pygame.K_DOWN]:
            dx = 1
        elif keys[pygame.K_LEFT]:
            dy = -1
        elif keys[pygame.K_RIGHT]:
            dy = 1

        if dx != 0 or dy != 0:
            new_rat = (game.elements['rat'][0] + dx, game.elements['rat'][1] + dy)
            if (0 <= new_rat[0] < MAZE_SIZE and
                    0 <= new_rat[1] < MAZE_SIZE and
                    game.maze[new_rat[0]][new_rat[1]] != 'W'):
                # Move rat
                game.elements['rat'] = new_rat
                if game.check_collisions():
                    move_cooldown = 15  # Reset on collision
                    continue
                # Move AI once
                game.update_positions()
                move_cooldown = 15  # 15-frame cooldown

    if move_cooldown > 0:
        move_cooldown -= 1

    # Draw everything
    screen.fill(COLORS['path'])
    draw_maze()
    draw_elements()
    draw_text()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()