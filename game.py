# Import the module pygame that we installed with pip3 install pygame
from pygame import *

FPS = 30
WIDTH = 600
HEIGHT = 600
plane_x = 480
plane_y = 240
speed = 20

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Flight 714")
clock = time.Clock()
background = transform.scale(image.load("desert.jpg"),(600,600))
plane = transform.scale(image.load("airplane.png"), (80,80))
dt = 0

run = True
while run:

  screen.blit(background, (0,0));
  screen.blit(plane, (plane_x, plane_y))
  
  # poll for events
  # QUIT event means the user clicked X to close your window
  for e in event.get():
    if e.type == QUIT:
      quit()
      run = False
      
    keys = key.get_pressed()
    if keys[K_LEFT] and plane_x > 5:
      plane_x -= speed
    if keys[K_RIGHT] and plane_x < WIDTH - 80:
      plane_x += speed
      
    if keys[K_UP] and plane_y > 5:
      plane_y -= speed
    if keys[K_DOWN] and plane_y < HEIGHT - 300:
      plane_y += speed

      
  # RENDER YOUR GAME HERE

    
  #filp() the display to put your work on screen
  display.flip()
  
  # limit FPS to 60
  # dt is delta time in seconds since last frame, used for framerate-independent physics 
  dt = clock.tick(60) / 1000

quit()