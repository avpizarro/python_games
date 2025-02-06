from pygame import *
from random import randint, choice
# import numpy as np # Imported numpy to manage image pixels and change colour - TBC

# Initialise the font
font.init()
score_font = font.Font(None,45)

# Set the variables
# Screen
WIDTH = 800
HEIGHT = 800

# Colours
COLOUR_BK = ((238, 238, 238))
COLOUR = ((0, 0, 0))

# Wall
wall_thickness = 10
gap = 60
num_of_walls = int(((WIDTH-gap)/(gap+10)) + 1)

# Coins
coins_collected = 0

#Set the display
#Size
screen = display.set_mode((WIDTH, HEIGHT))
# Game name
display.set_caption("Tragamonedas 💰")

# Get the clock going
clock = time.Clock() # Remember to call it in the loop - otherwise the app crashes

# A class to create the wall segments as sprites
class Wall(sprite.Sprite):
  def __init__(self, x, y, width, height, colour):
    super().__init__()
    print(f"Creating surface with size: {width} x {height} in x: {x}, y: {y}")  # Debugging
    self.image = Surface((width, height))
    self.image.fill(colour)
    self.rect = self.image.get_rect(topleft=(x, y))    

# Class to calculate the different wall positions and to draw them 
class Border():
  def __init__(self, gap, colour, x, y, length, full_length, wall_thickness):
    self.gap = gap
    self.colour = colour
    self.x = x
    self.y = y
    self.length = length
    self.thickness = wall_thickness
    self.full_length = full_length
    self.walls = sprite.Group() # Store wall segments
  
  def build_horizontal_wall(self):
    sibling_x = self.x + self.length + self.gap  # Calculate the x position of the second side of the wall
    sibling_length = self.full_length - self.gap - self.length  # Calculate the length of the second side of the wall
    self.walls.add(Wall(self.x, self.y, self.length, self.thickness, self.colour)) # Draw the left rectangle
    self.walls.add(Wall(sibling_x, self.y, sibling_length, self.thickness, self.colour)) # Draw the right rectangle
  
  def build_vertical_wall(self):
    sibling_y = self.y + self.length + self.gap # Calculate y position, x remains the same, but y needs to change
    sibling_length = self.full_length - self.gap - self.length # Calculate the length of the second side of the wall
    self.walls.add(Wall(self.x, self.y, self.thickness, self.length, self.colour)) # Draw the first rectangle
    self.walls.add(Wall(self.x, sibling_y, self.thickness, sibling_length, self.colour)) # Draw the second rectangle
    
# Coin Class
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
    
# Super Class to make the Ghost and Player sprites
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
  
  def reset(self):
    screen.blit(self.image, 15, 15)
    
class Ghosts(Props): 
  def move(self): 
    # the ghost moves vertically and horizontally

    # Move right
    # if self.rect.right < WIDTH:
    #   self.rect.move_ip(self.speed, 0)
    # Move left
    if self.rect.left > 0:
      self.rect.move_ip(-self.speed, 0)
    # Move up
    # self.rect.move_ip(0, -self.speed)
    # Move down
    # self.rect.move_ip(0, self.speed)
    
      
  def change_direction(self):
    self.speed = -self.speed

# Define the Player class with the method to control the movement
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
    
# Create the maze
maze = sprite.Group()

for i in range(1, 6):
  
  # Get the full length we have to build the walls, 
  full_length = int(WIDTH - gap*2*i) # (This is passed as a param to calculate the second side of the wall length)
  
  # Array with random ints to get the length of the first side of the wall
  first_wall_lengths = [randint(0, full_length-gap) for i in range(4)]
  
  # Create four walls for each side of the screen
  wall_top = Border(gap, COLOUR, gap*i + 10, gap*i + 10, first_wall_lengths[0], full_length, wall_thickness) # top
  wall_bottom = Border(gap, COLOUR, gap*i + 10, HEIGHT - gap*i, first_wall_lengths[1], full_length, wall_thickness) # bottom
  wall_left = Border(gap, COLOUR, gap*i + 10, gap*i + 10, first_wall_lengths[2], full_length, wall_thickness) # left
  wall_right = Border(gap, COLOUR, WIDTH - gap*i + 10, gap*i + 10, first_wall_lengths[3], full_length, wall_thickness) # right
  
  # Build the walls, this is what creates the Sprites!!!!
  wall_top.build_horizontal_wall()
  wall_bottom.build_horizontal_wall()
  wall_left.build_vertical_wall()
  wall_right.build_vertical_wall()
  
  # Add the walls to the walls array to display they in the game loop
  maze.add(wall_top.walls.sprites())
  maze.add(wall_bottom.walls.sprites())
  maze.add(wall_left.walls.sprites())
  maze.add(wall_right.walls.sprites())

# Add walls to the maze sprite group
print(f"maze: {maze}")

# create a coin instance
coins = sprite.Group()

# store the possible coin positions
pos = [15, 95]
i = 95
while len(pos) < 13:
  i += 60
  pos.append(i)
  
# Create the wallet prop
wallet = Props(0, "wallet.png", choice(pos), choice(pos))

# Create the ghost and assign a random position
ghost = Ghosts(2, "ghost.png", choice(pos), choice(pos))

# Create the player and assign the home position
player = Player(2, "player.png", 15, 15)

# Create the randomly positioned coins    
for i in range(12):
  coin = Coin("coin.png", choice(pos), choice(pos))
  coins.add(coin)

# Variable to start and stop the loop
running = True

# Start the game loop
while running:
  
  # Quit game when pressing X on the window
  for e in event.get():
    if e.type == QUIT:
      quit()
      running = False
      
  # Add a colour to the display
  screen.fill(COLOUR_BK)
  
  # Build the walls
  maze.draw(screen)
  
  # Draw the wallet
  wallet.update()
  
  #Draw the group of coins
  coins.draw(screen)
  
  # Draw the ghost
  ghost.update()
  ghost.move() # Get the ghost moving
  
  # Draw the player
  player.update()
  player.controls() # control the player with the arrow keys
  
  # Pick up the coins
  coin_hit_list = sprite.spritecollide(player, coins, True)
  for coin in coin_hit_list:
    coins_collected += 1 # Add them to the list to check for a win
  
  # Return the player home if it touches the walls or the ghost
  if sprite.spritecollide(player, maze, False):
    player.rect.x = 15
    player.rect.y = 15
  
  # Check that all the coins have been collected, now the player can get the wallet
  if coins_collected == 12:
    win = Rect.colliderect(player.rect, wallet.rect)
    # Game over screen if the player wins
    if win == True:
      game_over = score_font.render("GAME OVER", True, "orange")
      screen.blit(game_over, (WIDTH/2 - 77, HEIGHT/2 - 10))
      display.flip() # Update the screen
      time.delay(5000) # Show Game over for 5 seconds
      running = False
  
  display.update()
  clock.tick(60)
  
quit()
