import pygame
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRAVITY = 0.6
FPS = 60

# Colors (NES-style palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (240, 0, 0)
GREEN = (0, 160, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
SKIN = (255, 204, 102)
BLUE = (0, 100, 200)
LIGHT_BLUE = (135, 206, 235)

# Direction enum
class Direction(Enum):
    LEFT = -1
    RIGHT = 1
    IDLE = 0

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.vel_y = 0
        self.vel_x = 0
        self.jumping = False
        self.direction = Direction.RIGHT
        self.frame = 0
        self.animation_counter = 0
        
    def handle_input(self, keys):
        """Handle keyboard input for Mario"""
        self.vel_x = 0
        
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
            self.direction = Direction.LEFT
            self.animation_counter += 1
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 5
            self.direction = Direction.RIGHT
            self.animation_counter += 1
        else:
            self.animation_counter = 0
        
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -15
            self.jumping = True
    
    def update(self, platforms):
        """Update Mario's position"""
        # Apply gravity
        self.vel_y += GRAVITY
        self.vel_y = min(self.vel_y, 10)  # Terminal velocity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Screen boundaries (left/right)
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - self.width
        
        # Check collision with platforms
        self.jumping = True
        for platform in platforms:
            if self.collides_with(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0:  # Jumping
                    self.y = platform.y + platform.height
                    self.vel_y = 0
        
        # Fall off screen
        if self.y > WINDOW_HEIGHT:
            return False
        
        return True
    
    def collides_with(self, platform):
        """Check collision with platform"""
        return (self.x + self.width > platform.x and
                self.x < platform.x + platform.width and
                self.y + self.height > platform.y and
                self.y < platform.y + platform.height)
    
    def draw(self, screen):
        """Draw Mario"""
        # Body (red shirt)
        pygame.draw.rect(screen, RED, (self.x + 8, self.y + 16, 16, 20))
        
        # Head (skin tone)
        pygame.draw.rect(screen, SKIN, (self.x + 6, self.y + 4, 20, 12))
        
        # Eyes
        eye_offset = 4 if self.direction == Direction.RIGHT else -4
        pygame.draw.circle(screen, BLACK, (int(self.x + 12 + eye_offset), int(self.y + 8)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 18 + eye_offset), int(self.y + 8)), 2)
        
        # Mustache
        pygame.draw.line(screen, BLACK, (self.x + 12, self.y + 12), (self.x + 16, self.y + 12), 2)
        
        # Pants (blue)
        pygame.draw.rect(screen, BLUE, (self.x + 8, self.y + 36, 16, 12))
        
        # Shoes
        pygame.draw.rect(screen, BLACK, (self.x + 6, self.y + 44, 8, 4))
        pygame.draw.rect(screen, BLACK, (self.x + 18, self.y + 44, 8, 4))


class Platform:
    def __init__(self, x, y, width, height=16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen):
        """Draw platform in NES brick style"""
        # Draw green pipe-like platforms at bottom
        if self.width < 200:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (0, 120, 0), (self.x, self.y, self.width, 4))
        else:
            # Ground platform
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
            # Add brick pattern
            for i in range(0, int(self.width), 16):
                pygame.draw.line(screen, (100, 50, 0), (self.x + i, self.y + 8), (self.x + i + 16, self.y + 8), 1)
            for i in range(0, int(self.height), 8):
                pygame.draw.line(screen, (100, 50, 0), (self.x, self.y + i), (self.x + self.width, self.y + i), 1)


class HeartBlock:
    """Special block that gives hearts when hit"""
    def __init__(self, x, y, width=32, height=32):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
    
    def draw(self, screen):
        """Draw golden heart block with distinctive appearance"""
        if self.active:
            # Golden block background
            pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (200, 150, 0), (self.x, self.y, self.width, self.height), 3)
            
            # Draw heart symbol
            heart_x = self.x + self.width // 2
            heart_y = self.y + self.height // 2
            # Top half of heart
            pygame.draw.circle(screen, RED, (int(heart_x - 6), int(heart_y - 4)), 4)
            pygame.draw.circle(screen, RED, (int(heart_x + 6), int(heart_y - 4)), 4)
            # Bottom half of heart
            points = [
                (int(heart_x - 8), int(heart_y + 2)),
                (int(heart_x + 8), int(heart_y + 2)),
                (int(heart_x), int(heart_y + 8))
            ]
            pygame.draw.polygon(screen, RED, points)
    
    def collides_with(self, obj):
        """Check collision with object"""
        return (obj.x + obj.width > self.x and
                obj.x < self.x + self.width and
                obj.y + obj.height > self.y and
                obj.y < self.y + self.height)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.direction = Direction.LEFT
        self.speed = 2
    
    def update(self, platforms):
        """Update enemy position"""
        self.x += self.speed * self.direction.value
        
        # Check if enemy hits a platform edge
        on_platform = False
        for platform in platforms:
            if (self.x + self.width > platform.x and
                self.x < platform.x + platform.width and
                abs(self.y + self.height - platform.y) < 5):
                on_platform = True
                break
        
        # Turn around at screen edges or platform edges
        if self.x < 0 or self.x + self.width > WINDOW_WIDTH or not on_platform:
            self.direction = Direction(self.direction.value * -1)
    
    def draw(self, screen):
        """Draw enemy (Goomba style)"""
        # Body
        pygame.draw.ellipse(screen, BROWN, (self.x, self.y + 8, self.width, 20))
        
        # Head
        pygame.draw.ellipse(screen, BROWN, (self.x + 2, self.y, self.width - 4, 16))
        
        # Eyes
        eye_offset = 8 if self.direction == Direction.RIGHT else 16
        pygame.draw.circle(screen, WHITE, (int(self.x + eye_offset), int(self.y + 6)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + eye_offset), int(self.y + 6)), 1)


class MarioGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Super Mario - Vintage Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 48)
        self.reset_game()
    
    def reset_game(self):
        """Initialize or reset the game state"""
        self.mario = Mario(100, WINDOW_HEIGHT - 150)
        self.platforms = self.create_platforms()
        self.heart_blocks = self.create_heart_blocks()
        self.enemies = [Enemy(300, WINDOW_HEIGHT - 200), Enemy(500, WINDOW_HEIGHT - 250)]
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.game_over_reason = None
        self.level = 1
    
    def create_platforms(self):
        """Create platform layout"""
        platforms = [
            # Ground
            Platform(0, WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60),
            
            # Floating platforms
            Platform(200, WINDOW_HEIGHT - 200, 150, 16),
            Platform(500, WINDOW_HEIGHT - 250, 150, 16),
            Platform(150, WINDOW_HEIGHT - 350, 120, 16),
            Platform(550, WINDOW_HEIGHT - 350, 120, 16),
            Platform(350, WINDOW_HEIGHT - 450, 100, 16),
            
            # High platform (goal)
            Platform(300, WINDOW_HEIGHT - 550, 200, 20),
        ]
        return platforms
    
    def create_heart_blocks(self):
        """Create special heart blocks"""
        heart_blocks = [
            HeartBlock(100, WINDOW_HEIGHT - 350, 32, 32),
            HeartBlock(650, WINDOW_HEIGHT - 300, 32, 32),
        ]
        return heart_blocks
    
    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                    self.reset_game()
        return True
    
    def update(self):
        """Update game logic"""
        if self.game_over or self.game_won:
            return
        
        keys = pygame.key.get_pressed()
        self.mario.handle_input(keys)
        
        if not self.mario.update(self.platforms):
            self.game_over = True
        
        # Check collision with heart blocks
        for heart_block in self.heart_blocks:
            if heart_block.active and heart_block.collides_with(self.mario):
                self.score += 1500
                heart_block.active = False
        
        # Check if score reached 3000
        if self.score >= 3000:
            self.game_over = True
            self.game_over_reason = "score"
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.platforms)
        
        # Check collision with enemies
        for enemy in self.enemies:
            if (self.mario.x < enemy.x + enemy.width and
                self.mario.x + self.mario.width > enemy.x and
                self.mario.y < enemy.y + enemy.height and
                self.mario.y + self.mario.height > enemy.y):
                
                # If Mario jumps on enemy, defeat it
                if self.mario.vel_y > 0 and self.mario.y < enemy.y + 10:
                    self.enemies.remove(enemy)
                    self.mario.vel_y = -10
                    self.score += 100
                else:
                    self.game_over = True
                    self.game_over_reason = "enemy"
        
        # Check win condition (reach the high platform)
        if (self.mario.x + self.mario.width > 300 and
            self.mario.x < 500 and
            self.mario.y < WINDOW_HEIGHT - 550):
            self.game_won = True
            self.score += 1000
    
    def draw(self):
        """Draw game elements"""
        # Draw sky
        self.screen.fill(LIGHT_BLUE)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw heart blocks
        for heart_block in self.heart_blocks:
            heart_block.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw Mario
        self.mario.draw(self.screen)
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (WINDOW_WIDTH - 150, 10))
        
        # Draw game over message
        if self.game_over:
            if self.game_over_reason == "score":
                game_over_text = self.large_font.render("Happy 500 days, my Babe!", True, YELLOW)
                message_text = self.font.render("We did it! Hope you smile every day!", True, WHITE)
            else:
                game_over_text = self.large_font.render("Ohh! Babe hits a poop", True, RED)
                message_text = self.font.render("Please try again!", True, WHITE)
            
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            msg_rect = message_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(message_text, msg_rect)
            
            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        # Draw win message
        if self.game_won:
            win_text = self.large_font.render("YOU WIN!", True, YELLOW)
            text_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(win_text, text_rect)
            
            restart_text = self.font.render("Press SPACE to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = MarioGame()
    game.run()