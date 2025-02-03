import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

bird = pygame.image.load("colibri.png").convert_alpha()
bird = pygame.transform.scale(bird, (50, 50))
bird_rect = bird.get_rect()
bird_rect.center = (100, 300)

def move_bird(bird_rect, speed):
    bird_rect.move_ip(speed, 0)  # Moves in place

running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen
    move_bird(bird_rect, 5)  # Move every frame
    screen.blit(bird, bird_rect)  # Draw bird
    pygame.display.flip()  # Update screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
