import pygame
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FINISH_LINE_COLOR = (255, 215, 0)  

NUM_SQUARES = 12  
SQUARE_SIZE = 30
MAX_SPEED = 4
MIN_SPEED = 1

class Square:
    def __init__(self, name):
        self.name = name
        
        start_x = random.randint(0, SCREEN_WIDTH // 4)
        start_y = random.randint(0, SCREEN_HEIGHT - SQUARE_SIZE)
        
        self.dx = random.uniform(MIN_SPEED, MAX_SPEED)
        self.dy = random.uniform(MIN_SPEED, MAX_SPEED) * random.choice([-1, 1])

        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("testS")
    clock = pygame.time.Clock()

    squares = [Square(f"-{i+1}") for i in range(NUM_SQUARES)]

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

                for j in range(i + 1, len(squares)):
                    other_square = squares[j]
                    if square.rect.colliderect(other_square.rect):
                        square.dx, other_square.dx = other_square.dx, square.dx
                        square.dy, other_square.dy = other_square.dy, square.dy

                if square.rect.colliderect(finish_line_rect):
                    winner = square 
        screen.fill(BLACK) 

        for square in squares:
            square.draw(screen)

        pygame.draw.rect(screen, FINISH_LINE_COLOR, finish_line_rect)

        if winner:
            font = pygame.font.Font(None, 80)
            text_surface = font.render(f"{winner.name}!", True, winner.color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            
            background_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, BLACK, background_rect)
            pygame.draw.rect(screen, winner.color, background_rect, 3) # borda
            
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