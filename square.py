import pygame
import random
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FINISH_LINE_COLOR = (255, 215, 0)
OBSTACLE_COLOR = (100, 100, 120)

NUM_SQUARES = 12
SQUARE_SIZE = 30
INITIAL_SPEED = 3

WALL_WIDTH = 20
WALL_GAP_SIZE = 150 

class Square:
    def __init__(self, name, start_pos):
        self.name = name
        
        start_x, start_y = start_pos
        
        angle = random.uniform(-math.pi / 4, math.pi / 4)
        self.dx = INITIAL_SPEED * math.cos(angle)
        self.dy = INITIAL_SPEED * math.sin(angle)

        self.color = (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))
        
        self.rect = pygame.Rect(start_x, start_y, SQUARE_SIZE, SQUARE_SIZE)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def check_wall_collision(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.dx *= -1
            self.rect.left = max(0, self.rect.left)
            self.rect.right = min(SCREEN_WIDTH, self.rect.right)

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.dy *= -1
            self.rect.top = max(0, self.rect.top)
            self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)
            
    def check_obstacle_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                overlap_x = min(self.rect.right, obstacle.right) - max(self.rect.left, obstacle.left)
                overlap_y = min(self.rect.bottom, obstacle.bottom) - max(self.rect.top, obstacle.top)

                if overlap_x < overlap_y:
                    self.dx *= -1
                    if self.rect.centerx < obstacle.centerx: self.rect.right = obstacle.left
                    else: self.rect.left = obstacle.right
                else:
                    self.dy *= -1
                    if self.rect.centery < obstacle.centery: self.rect.bottom = obstacle.top
                    else: self.rect.top = obstacle.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def create_obstacle_walls():
    obstacles = []
    wall_positions_x = [int(SCREEN_WIDTH * 0.3), int(SCREEN_WIDTH * 0.55), int(SCREEN_WIDTH * 0.8)]
    
    for x_pos in wall_positions_x:
        gap_y_start = random.randint(0, SCREEN_HEIGHT - WALL_GAP_SIZE)
        gap_y_end = gap_y_start + WALL_GAP_SIZE
        
        top_wall = pygame.Rect(x_pos, 0, WALL_WIDTH, gap_y_start)
        bottom_wall = pygame.Rect(x_pos, gap_y_end, WALL_WIDTH, SCREEN_HEIGHT - gap_y_end)
        
        obstacles.append(top_wall)
        obstacles.append(bottom_wall)
        
    return obstacles

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Corrida com Desafios")
    clock = pygame.time.Clock()

    squares = []
    for i in range(NUM_SQUARES):
        while True:
            start_x = random.randint(20, SCREEN_WIDTH // 5)
            start_y = random.randint(20, SCREEN_HEIGHT - SQUARE_SIZE - 20)
            new_rect = pygame.Rect(start_x, start_y, SQUARE_SIZE, SQUARE_SIZE)

            if not any(s.rect.colliderect(new_rect) for s in squares):
                squares.append(Square(f"{i+1}", (start_x, start_y)))
                break
    
    obstacles = create_obstacle_walls()
    
    finish_line_rect = pygame.Rect(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT)

    running = True
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and winner:
                main()
                return 

        if not winner:
            for i, square in enumerate(squares):
                square.move()
                square.check_wall_collision()
                square.check_obstacle_collision(obstacles)

                for j in range(i + 1, len(squares)):
                    other_square = squares[j]
                    if square.rect.colliderect(other_square.rect):
                        square.dx, other_square.dx = other_square.dx, square.dx
                        square.dy, other_square.dy = other_square.dy, square.dy

                if square.rect.colliderect(finish_line_rect):
                    winner = square
                    
        screen.fill(BLACK) 
        for obstacle in obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
        for square in squares:
            square.draw(screen)
        pygame.draw.rect(screen, FINISH_LINE_COLOR, finish_line_rect)

        if winner:
            font = pygame.font.Font(None, 80)
            text_surface = font.render(f"{winner.name}!", True, winner.color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            
            background_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, winner.color, background_rect, 3)
            
            screen.blit(text_surface, text_rect)

            font_small = pygame.font.Font(None, 30)
            restart_surface = font_small.render("press", True, WHITE)
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
            screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()