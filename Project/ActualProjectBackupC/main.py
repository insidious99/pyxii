import pygame
import random
from database import save_game, load_game

# Initialize Pygame
pygame.init()

# Load saved high score
high_score_data = load_game()
high_score = high_score_data[0] if isinstance(high_score_data, tuple) else high_score_data
print(f"[INFO] High Score: {high_score}")

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sierra Two: Space Shooter")

# Load assets
background = pygame.image.load("assets/images/background.png")
player_img = pygame.image.load("assets/images/player.png")
player_img = pygame.transform.scale(player_img, (120, 120))

bullet_img = pygame.image.load("assets/images/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (20, 40))
bullet_img = pygame.transform.rotate(bullet_img, 90)

enemy_img = pygame.image.load("assets/images/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))
enemy_img = pygame.transform.rotate(enemy_img, 270)

elite_enemy_img = pygame.image.load("assets/images/elite_enemy.png")
elite_enemy_img = pygame.transform.scale(elite_enemy_img, (80, 80))

# Load sounds
bullet_sound = pygame.mixer.Sound("assets/sounds/bullet.mp3")

# Load font
font = pygame.font.Font(None, 36)

def reset_game():
    global player_x, player_y, player_vel_x, bullets, enemies, enemy_speed, enemy_spawn_rate, frame_count
    global score, lives, kills, game_over, bullets_fired
    player_x = WIDTH // 2
    player_y = HEIGHT - 120
    player_vel_x = 0
    bullets = []
    enemies = []
    enemy_speed = 2
    enemy_spawn_rate = 60
    frame_count = 0
    score = 0
    lives = 5
    kills = 0
    game_over = False
    bullets_fired = 1

# Initialize game state
reset_game()

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    frame_count += 1
    
    screen.blit(background, (0, 0))
    
    if not game_over:
        keys = pygame.key.get_pressed()
        player_vel_x = 0

        if keys[pygame.K_a]:
            player_vel_x = -5
        if keys[pygame.K_d]:
            player_vel_x = 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > high_score:
                    save_game(score)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(bullets_fired):
                        bullet_x = player_x + player_img.get_width() // 2 - bullet_img.get_width() // 2 + (i * 10 - (bullets_fired - 1) * 5)
                        bullets.append(pygame.Rect(bullet_x, player_y, 20, 40))
                    bullet_sound.play()
    
        player_x += player_vel_x
        player_x = max(0, min(WIDTH - player_img.get_width(), player_x))
    
        for bullet in bullets:
            bullet.y -= 10
    
        bullets = [bullet for bullet in bullets if bullet.y > 0]
    
        if frame_count % enemy_spawn_rate == 0:
            enemy_x = random.randint(0, WIDTH - 60)
            enemies.append({'rect': pygame.Rect(enemy_x, 0, 60, 60), 'health': 1, 'elite': False})
            if enemy_spawn_rate > 20:
                enemy_spawn_rate -= 1
    
        if kills % 10 == 0 and kills > 0:
            enemy_x = random.randint(0, WIDTH - 80)
            enemies.append({'rect': pygame.Rect(enemy_x, 0, 80, 80), 'health': 3, 'elite': True})
            kills += 1
    
        for enemy in enemies:
            enemy['rect'].y += enemy_speed
    
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy['rect']):
                    bullets.remove(bullet)
                    enemy['health'] -= 1
                    if enemy['health'] <= 0:
                        enemies.remove(enemy)
                        score += 10 if not enemy['elite'] else 50
                        kills += 1
                        if kills % 6 == 0:
                            lives += 1
                    break
    
        for enemy in enemies[:]:
            if enemy['rect'].y >= HEIGHT:
                enemies.remove(enemy)
                lives -= 1
            elif enemy['rect'].colliderect(pygame.Rect(player_x, player_y, player_img.get_width(), 120)):
                enemies.remove(enemy)
                lives -= 1
    
        bullets_fired = min(1 + score // 500, 5)
    
        if lives <= 0:
            game_over = True
            if score > high_score:
                high_score = score
                save_game(high_score)
    
        screen.blit(player_img, (player_x, player_y))
        for bullet in bullets:
            screen.blit(bullet_img, (bullet.x, bullet.y))
        for enemy in enemies:
            img = elite_enemy_img if enemy['elite'] else enemy_img
            screen.blit(img, (enemy['rect'].x, enemy['rect'].y))
    
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))
    else:
        screen.blit(background, (0, 0))
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 80))

        # Handle restart or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    reset_game()
                elif event.key == pygame.K_q:  # Quit the game
                    running = False
    
    pygame.display.flip()
pygame.quit()
