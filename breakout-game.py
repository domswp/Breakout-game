import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta layar
SCREEN_WIDTH = 647
SCREEN_HEIGHT = 600

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Ukuran paddle, bola, dan blok
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 20
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 30

# Kecepatan paddle
PADDLE_SPEED = 5

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout Game')

# Posisi awal paddle
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

# Posisi awal bola
ball_x = paddle_x + (PADDLE_WIDTH // 2) - (BALL_SIZE // 2)
ball_y = paddle_y - BALL_SIZE
ball_speed_x = 0
ball_speed_y = 0

# Membuat blok-blok
blocks = []
for row in range(5):
    for col in range(10):
        block = pygame.Rect(col * (BLOCK_WIDTH + 5), row * (BLOCK_HEIGHT + 5), BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append(block)

# Life point
life_point = 3

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Memulai permainan saat menekan tombol SPACE
    keys = pygame.key.get_pressed()
    if not ball_speed_x and not ball_speed_y:
        if keys[pygame.K_SPACE]:
            ball_speed_x = random.choice([-5, 5])
            ball_speed_y = -5

    # Pindahkan paddle sesuai input keyboard
    if keys[pygame.K_LEFT]:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        paddle_x += PADDLE_SPEED

    # Batasi paddle agar tidak keluar dari layar
    paddle_x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, paddle_x))

    # Pindahkan bola mengikuti paddle saat permainan dimulai
    if not ball_speed_x and not ball_speed_y:
        ball_x = paddle_x + (PADDLE_WIDTH // 2) - (BALL_SIZE // 2)

    # Pindahkan bola
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Pemantulan bola saat mengenai tepi layar
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_SIZE:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y

    # Deteksi tabrakan bola dengan paddle
    if (
        paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH
        and paddle_y <= ball_y <= paddle_y + PADDLE_HEIGHT
    ):
        ball_speed_y = -ball_speed_y

    # Deteksi tabrakan bola dengan blok
    for block in blocks[:]:
        if (
            block.left <= ball_x <= block.right
            and block.top <= ball_y <= block.bottom
        ):
            ball_speed_y = -ball_speed_y
            blocks.remove(block)
            break

    # Deteksi bola jatuh di bawah layar
    if ball_y >= SCREEN_HEIGHT:
        life_point -= 1
        ball_speed_x = 0
        ball_speed_y = 0
        ball_x = paddle_x + (PADDLE_WIDTH // 2) - (BALL_SIZE // 2)
        ball_y = paddle_y - BALL_SIZE
        if life_point == 0:
            running = False

    # Gambar elemen-elemen permainan
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_SIZE)
    for block in blocks:
        pygame.draw.rect(screen, WHITE, block)

    # Tampilkan jumlah life point
    font = pygame.font.Font(None, 36)
    text = font.render(f"Life: {life_point}", True, WHITE)
    screen.blit(text, (10, 10))

    # Update layar
    pygame.display.flip()

    # Batasi kecepatan frame
    clock.tick(60)

pygame.quit()

