import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load("py.png"))

ball = pygame.image.load("pacman.png")
angle = 0;
running = True
while running:
    angle += 1
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    screen.blit(pygame.transform.rotate(ball, angle), (200, 150))
    pygame.display.update()
