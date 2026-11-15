import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический мусорщик")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Цвета
BLACK = (10, 10, 30)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)
BLUE = (50, 150, 255)
GRAY = (130, 130, 130)

# Игрок
player = pygame.Rect(380, 500, 40, 40)
player_speed = 5

# Объекты
resources = []
meteors = []

for i in range(5):
    resources.append(pygame.Rect(random.randint(20, 760), random.randint(-600, 0), 20, 20))

for i in range(4):
    meteors.append(pygame.Rect(random.randint(20, 760), random.randint(-600, 0), 35, 35))

score = 0
lives = 3
game_over = False

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                score = 0
                lives = 3
                game_over = False
                player.x = 380
                player.y = 500

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        player.clamp_ip(screen.get_rect())

        for item in resources:
            item.y += 3

            if item.y > HEIGHT:
                item.x = random.randint(20, 760)
                item.y = random.randint(-200, -20)

            if player.colliderect(item):
                score += 10
                item.x = random.randint(20, 760)
                item.y = random.randint(-200, -20)

        for meteor in meteors:
            meteor.y += 4

            if meteor.y > HEIGHT:
                meteor.x = random.randint(20, 760)
                meteor.y = random.randint(-300, -20)

            if player.colliderect(meteor):
                lives -= 1
                meteor.x = random.randint(20, 760)
                meteor.y = random.randint(-300, -20)

                if lives <= 0:
                    game_over = True

    # Рисование
    screen.fill(BLACK)

    # Звезды
    for i in range(40):
        x = (i * 97) % WIDTH
        y = (i * 53 + pygame.time.get_ticks() // 30) % HEIGHT
        pygame.draw.circle(screen, WHITE, (x, y), 1)

    # Корабль
    pygame.draw.polygon(
        screen, BLUE,
        [(player.centerx, player.top),
         (player.left, player.bottom),
         (player.centerx, player.bottom - 10),
         (player.right, player.bottom)]
    )

    # Ресурсы
    for item in resources:
        pygame.draw.circle(screen, YELLOW, item.center, 10)

    # Метеориты
    for meteor in meteors:
        pygame.draw.circle(screen, GRAY, meteor.center, 18)

    # Счет и жизни
    screen.blit(font.render(f"Очки: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Жизни: {lives}", True, WHITE), (650, 20))

    if game_over:
        text = font.render("ИГРА ОКОНЧЕНА", True, RED)
        restart = font.render("Нажми R для перезапуска", True, WHITE)

        screen.blit(text, (270, 250))
        screen.blit(restart, (230, 300))

    pygame.display.flip()