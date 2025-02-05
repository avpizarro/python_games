from pygame import *
from random import randint, choice
import numpy as np

# Get the variables
WIDTH = 800
HEIGHT = 800
COLOUR_BK = ((238, 238, 238))
COLOUR = ((0, 0, 0))

# Wall
wall_thickness = 10
gap = 60
num_of_walls = int(((WIDTH-gap)/(gap+10)) + 1)

#Set the display
#Size
screen = display.set_mode((WIDTH, HEIGHT))
# Game name
display.set_caption("Tragamonedas 💰")

# Get the clock going
clock = time.Clock()

class Border(sprite.Sprite):
  def __init__(self, gap, colour, x, y, length, full_width):
    sprite.Sprite.__init__(self)
    self.gap = gap
    self.colour = colour
    self.x = x
    self.y = y
    self.length = length
    self.thickness = wall_thickness
    self.full_width = full_width
  
  def build_wall_horizontal(self):
    sibling_x = self.x + self.length + gap  # Calculate the x position of the second side of the wall
    sibling_length = self.full_width - gap - self.length  # Calculate the length of the second side of the wall
    draw.rect(screen, self.colour, (self.x, self.y, self.length, self.thickness)) # Draw the first rectangle
    draw.rect(screen, self.colour, (sibling_x, self.y, sibling_length, self.thickness)) # Draw the second rectangle
    
  def build_wall_vertical(self):
    sibling_y = self.y + self.length + gap # Calculate y position, x remains the same, but y needs to change
    sibling_length = self.full_width - gap - self.length # Calculate the length of the second side of the wall
    draw.rect(screen, self.colour, (self.x, self.y, self.thickness, self.length)) # Draw the first rectangle
    draw.rect(screen, self.colour, (self.x, sibling_y, self.thickness, sibling_length)) # Draw the second rectangle

class Coin(sprite.Sprite):
  def __init__(self, img, x_pos, y_pos):
    sprite.Sprite.__init__(self)
    self.original_image = transform.scale(image.load(img), (40,40)).convert_alpha()
    self.image = self.original_image.copy()
    self.rect = self.image.get_rect()
    self.rect.x = x_pos
    self.rect.y = y_pos
      
  def draw_coin(self, position):
    screen.blit(self.image, position)
    
  def add_color(self, color=(0,255,0)):
    self.image = self.original_image.copy()
    arr = surfarray.pixels3d(self.image).astype(np.uint8) # Get a pixel array
    alpha = surfarray.pixels_alpha(self.image).astype(np.uint8) # Alpha channel
    mask = (arr[:, :, 0] > 10) | (arr[:, :, 1] > 10) | (arr[:, :, 2] > 10) # ignore near balck pixels
    
    # Apply color while keeping original brightness
    arr[:, :, 0][mask] =(arr[:, :, 0][mask] // 2) + (color[0] // 2)
    arr[:, :, 1][mask] =(arr[:, :, 1][mask] // 2) + (color[1] // 2)
    arr[:, :, 2][mask] =(arr[:, :, 2][mask] // 2) + (color[2] // 2)
    
    # Restore the modified RGB back to the surface
    surfarray.blit_array(self.image, arr)
    
   # Restore transparency
    alpha_surface = Surface(self.image.get_size(), SRCALPHA)
    alpha_surface.fill((255, 255, 255, 0))  # Fully transparent base
    alpha_surface.blit(self.image, (0, 0))  # Copy the image with tint
    self.image = alpha_surface  # Replace the original image

    # Restore alpha channel separately
    self.image.set_alpha(255)  # Ensure full visibility
    self.image.set_colorkey((0, 0, 0))  # Make black transparent  
    
class Props(sprite.Sprite):
  def __init__(self, speed, img, x, y):
    sprite.Sprite.__init__(self)
    self.speed = speed
    self.image = transform.scale(image.load(img), (40,40))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  
  def update(self):
    screen.blit(self.image, (self.rect.x, self.rect.y))
    
class Ghosts(Props): 
  def move(self): # I need to have many conditions to have the ghost moving vertically and horizontally
    #and changing directions
    if self.rect.x >= 0 and self.rect.x <= 800 - self.rect.w and self.rect.y >= 0 and self.rect.y <= 800 - self.rect.h:
      self.rect.move_ip(self.speed, self.speed)
    
  def change_direction(self):
    self.speed = -self.speed

class Player(Props):
  def controls(self):
    keys = key.get_pressed()
    if keys[K_UP] and self.rect.top > 0:
      self.rect.y -= self.speed
    if keys[K_DOWN] and self.rect.bottom < HEIGHT:
      self.rect.y += self.speed
    if keys[K_LEFT] and self.rect.left >= 0:
      self.rect.x -= self.speed
    if keys[K_RIGHT] and self.rect.right < WIDTH:
      self.rect.x += self.speed
    
    
# Create the groups to 
walls_horizontal = []
walls_vertical = []

for i in range(1, 6):
  
  # Get the full length we have to build the walls, 
  full_length = int(WIDTH - gap*2*i) # (This is passed as a param to calculate the second side of the wall length)
  
  # Array with random ints to get the length of the first side of the wall
  first_wall_lengths = [randint(0, full_length) for i in range(4)]
  
  # Draws walls for each side of the screen
  wall_top = Border(gap, COLOUR, gap*i + 10, gap*i + 10, first_wall_lengths[0], full_length) # top
  wall_bottom = Border(gap, COLOUR, gap*i + 10, HEIGHT - gap*i, first_wall_lengths[1], full_length) # bottom
  wall_top_left = Border(gap, COLOUR, gap*i + 10, gap*i + 10, first_wall_lengths[2], full_length) # left
  wall_top_right = Border(gap, COLOUR, WIDTH - gap*i + 10, gap*i + 10, first_wall_lengths[3], full_length) # right
  
  # Add the walls to the walls array to display they in the game loop
  walls_horizontal.append(wall_top)  
  walls_horizontal.append(wall_bottom)
  walls_vertical.append(wall_top_left)
  walls_vertical.append(wall_top_right)

# create a coin instance
coins = sprite.Group()

# Create a group for the Wallet
wallet = sprite.Group()

# store the possible coin positions
pos = [15, 95]
i = 95
while len(pos) < 13:
  i += 60
  pos.append(i)
  
# Create the wallet prop
wallet_icon = Props(0, "wallet.png", choice(pos), choice(pos))
# Add the wallet to the coins group to display it
coins.add(wallet_icon)

# Create the ghost and assign a random position
ghost = Ghosts(2, "ghost.png", choice(pos), choice(pos))

# Create the player and assign the home position
player = Player(2, "player.png", 15, 15)
    
for i in range(12):
  coin = Coin("coin.png", choice(pos), choice(pos))
  coins.add(coin)

# Variable to start and stop the loop
running = True

while running:
  
  # Quit game when pressing X on the window
  for e in event.get():
    if e.type == QUIT:
      quit()
      running = False
      
  # Add a colour to the display
  screen.fill(COLOUR_BK)
  
  # Build the walls
  for wall in walls_horizontal:
    wall.build_wall_horizontal()
  for wall in walls_vertical:
    wall.build_wall_vertical()
  
  # Draw coins
  coins.draw(screen)
  ghost.update()
  ghost.move()
  player.update()
  player.controls()
        
  display.update()
  clock.tick(60)
  
quit()
