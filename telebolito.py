# Import pygame
from pygame import *
from time import sleep
from random import choice, randint

init()
# Background size variables
WIDTH = 600
HEIGHT = 400
# Colour variables (Do we change the color as the points increase?)
COLOUR_BK = (255, 165, 0, 0.8)
COLOUR = (0,0,0,0.8)
COLOUR_LN = (0,0,0,0.1)

# Starting coordinates for the paddles
paddle_width = 10
paddle_height = 60
paddle_x = 20
paddle_y = 170
comp_paddle_x = WIDTH - (paddle_x + 10)
comp_paddle_y = 170
circle_x = WIDTH / 2 - 8
circle_y = HEIGHT / 2 - 7.5
direction = 1
direction_x = 1
direction_y = 1

step = 15
speed = 5
speed_increment = 0
score_tracker = 5

# Variables to store the points
player = 0
computer = 0

# Set the background
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Telebolito")

clock = time.Clock()

text_font = font.SysFont(None, 40)

# Function to write the scores
def draw_text(text, font, text_col, x, y, col_bk):
  img = font.render(text, True, text_col, col_bk)
  screen.blit(img, (x, y))

# Function to draw a paddle
def draw_paddle(surface, color, x, y, width, height):
  return draw.rect(surface, color, Rect(x, y, width, height))

# Function to draw the ball
def draw_bolito(surface, color, x, y, size):
  return draw.rect(surface, color, Rect(x, y, size, size))

# Function to move the paddle
def move_comp_paddle(paddle, speed, direction, direction_x, direction_y):
  paddle.move_ip(0, speed * direction) # Start the movement
  
  # Reverse direction when hitting the top or bottom limit
  if (paddle.y > HEIGHT-65):
    direction = -1
  elif (paddle.y < 5):
    direction = 1
  elif (direction_x == 1 and direction_y == 1):
    direction = 1
  elif (direction_x == 1 and direction_y == -1):
    direction = -1
  return paddle, direction

# Function to reset the ball position 
def reset_bolito(bolito):
  bolito =  bolito.update(circle_x, circle_y, 15, 15)
  return  bolito

# Function to move the bolito
def move_bolito(bolito, speed, direction_x, direction_y, paddle, comp_paddle, player, computer):
  bolito.move_ip(speed * direction_x, speed * direction_y)
  
  if (bolito.x < 0):
    computer += 1
    direction_x = choice([-1, 1])
    direction_y = choice([-1, 1])
    print("Case 1:", direction_x, direction_y)
    reset_bolito(bolito)
    
  elif (bolito.x > 600):
    player += 1
    direction_x = choice([-1, 1])
    direction_y = choice([-1, 1])
    print("Case 2:", direction_x, direction_y)
    reset_bolito(bolito)
    
  elif (bolito.colliderect(paddle)):
    direction_x = 1
    
  elif (bolito.colliderect(comp_paddle)):
    direction_x = -1
    
  elif (bolito.y < 10):
    direction_y = 1
    
  elif(bolito.y > HEIGHT - 10):
    direction_y = -1
  
  return bolito, direction_x, direction_y, player, computer

# Draw the computer paddle 
computer_paddle = draw_paddle(screen, COLOUR, comp_paddle_x,comp_paddle_y,paddle_width,paddle_height)

 # Draw bolito  
bolito = draw_bolito(screen, COLOUR, circle_x, circle_y, 15)

# Variable to start the game loop
running = True

while running:
  for e in event.get():
    if e.type == QUIT:
      quit()
      running = False

  screen.fill(COLOUR_BK)
  
  
  # Draw middle line
  for y in range(10, HEIGHT, HEIGHT//10):
    draw.rect(screen, COLOUR_LN, Rect(WIDTH/2 - 3.5, y, 5, HEIGHT//20))
  
  # Draw player paddle
  player_paddle = draw_paddle(screen, COLOUR, paddle_x, paddle_y, paddle_width, paddle_height)
  
  # Move and update the computer paddle
  computer_paddle, direction = move_comp_paddle(computer_paddle, 5, direction, direction_x, direction_y) # Update position
  
  draw.rect(screen, COLOUR, computer_paddle);
  
  # Move and update the ball position
  bolito, direction_x, direction_y, player, computer = move_bolito(bolito, speed, direction_x, direction_y, player_paddle, computer_paddle, player, computer)
  
  draw.rect(screen, COLOUR, bolito)
  
  # Render text
  draw_text(str(player), text_font, COLOUR, 150, 10, COLOUR_BK)  
  draw_text(str(computer), text_font, COLOUR, 450, 10, COLOUR_BK)
  
  # Logic to use the up and dowm arrays to move the player's paddle
  keys = key.get_pressed()
  if keys[K_UP] and paddle_y > 5:
    paddle_y -= step
  if keys[K_DOWN] and paddle_y < HEIGHT-65:
    paddle_y += step
  
  if (player == computer and player > score_tracker and computer > score_tracker):
    speed_increment += 0.001
    speed += speed_increment
    score_tracker += 5

  display.flip()
  
  clock.tick(40)

quit()