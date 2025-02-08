from pygame import *
from random import randint, choice
# import numpy as np # Imported numpy to manage image pixels and change colour - TBC

# Initialise the music
mixer.init()

# Load and play background music
mixer.music.load("game-music-150676.mp3")
mixer.music.play(-1) # -1 causes the music to loop indefinitely
mixer.music.set_volume(0.2) # Set the volume to 20%

# Load the coin sound
coin_sound = mixer.Sound("retro-coin-4-236671.mp3")

# Load the slide sound
slide_sound = mixer.Sound("089048_woosh-slide-in-88642.mp3")

# Load the winning sound
win_sound = mixer.Sound("game-bonus-144751.mp3")

# Load the loosing sound -- Add a timer to create a loosing situation
lose_sound = mixer.Sound("sweet-game-over-sound-effect-230470.mp3")

# Initialise the font
font.init()
game_over_font = font.Font(None,45)
amount_font = font.Font(None,25)

# Set the variables
# Screen
WIDTH = 800
HEIGHT = 800

# Colours
COLOUR = ("orange")

# Wall
wall_thickness = 10
gap = 80
num_of_walls = int(((WIDTH-gap)/(gap+10)) + 1)

# Ghost
ghost_number = 4

# Coins
coins_collected = 0

#Set the display
#Size
screen = display.set_mode((WIDTH, HEIGHT))
# Add background image
bg = transform.scale(image.load("ai-generated-9088888_1280.jpg"), (WIDTH, HEIGHT))
# Game name
display.set_caption("Tragamonedas 💰")

# Get the clock going
clock = time.Clock() # Remember to call it in the loop - otherwise the app crashes

# A class to create the wall segments as sprites
class Wall(sprite.Sprite):
  def __init__(self, x, y, width, height, colour):
    super().__init__()
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
    self.original_image = transform.smoothscale(image.load(img), (40,40)).convert_alpha()
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
    self.image = transform.smoothscale(image.load(img), (40, 40))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  
  def update(self):
    screen.blit(self.image, (self.rect.x, self.rect.y))
  
  def reset(self):
    screen.blit(self.image, 15, 15)
    
class Ghosts(Props):
  def __init__(self, speed, img, x, y):
    super().__init__(speed, img, x, y)
    self.collide_rect = self.rect.inflate(-15,-15) # Smaller collision area
    self.direction = "left"
    
  def move(self, walls):
    """Moves the ghost and changes direction upon collision."""
    
    # Get the ghost moving
    if self.direction == "left":
      self.rect.x -= self.speed
    else:
      self.rect.x += self.speed
    
    # Check for collitions with walls
    if sprite.spritecollide(self, walls, False):
      # Undo movement
      if self.direction == "left":
        self.rect.x += self.speed # Move back
        self.direction = "right" # Change direction
      else:
        self.rect.x -= self.speed # Move back
        self.direction = "left" # Change direction
          
    # Handle screen bounderies separately:  
    if self.rect.x >= WIDTH - self.rect.w:
      self.direction = "left"
    if self.rect.x  <= 5:
      self.direction = "right"
      
    
    # # Store old position in case we need to revert
    # old_x, old_y = self.rect.x, self.rect.y
    
    # direction = choice(["left", "right", "up", "down"])
    
    # # Move in the current direction
    # if direction == "right":
    #   self.rect.move_ip(self.speed, 0)
    # # Move left
    # elif direction == "left":
    #   self.rect.move_ip(-self.speed, 0)
    # # Move up
    # elif direction == "up":
    #  self.rect.move_ip(0, -self.speed)
    # # Move down
    # elif direction ==  "bottom":
    #   self.rect.move_ip(0, self.speed)
      
    # # Check for collisions with walls
    # if sprite.spritecollide(self, walls, False, sprite.collide_rect_ratio(0.8)) or not (0 <= self.rect.x <= WIDTH - self.rect.w and 0 <= self.rect.y <= HEIGHT - self.rect.h):
    #   # Revert movement if collision is detected
    #   self.rect.x, self.rect.y = old_x, old_y
      
    #   # Get a list of valid movement directions
    #   valid_directions = []
    #   test_moves = {
    #     "left": (self.rect.x - self.speed, self.rect.y),
    #     "right": (self.rect.x + self.speed, self.rect.y),
    #     "up": (self.rect.x, self.rect.y - self.speed),
    #     "down": (self.rect.x, self.rect.y + self.speed),
    #   }
      
    #   for direction, (new_x, new_y) in test_moves.items():
    #     self.rect.topleft = (new_x, new_y) # Temporarily move
    #     if not sprite.spritecollide(self, walls, False) and (0 <= new_x <= WIDTH - self.rect.w and 0 <= new_y <= HEIGHT):
    #       valid_directions.append(direction)
      
    #   self.rect.x, self.rect.y = old_x, old_y # Restore original position
      
    #   # If valid direction exist, choose a new one
    #   if valid_directions:
    #     direction = choice(valid_directions)
    #   else:
    #     direction = choice([["left", "right", "up", "down"]])
    
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

for i in range(1, 4):
  
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

# create a coin instance
coins = sprite.Group()

# store the possible coin positions
pos = [25, 110]
i = 110
while len(pos) < 10:
  i += 80
  pos.append(i)
  
print(pos)
# Create the wallet prop
# wallet = Props(0, "wallet.png", choice(pos), choice(pos))
wallet = Props(0, "banking-4318911_640.png", choice(pos), choice(pos))

# Create a group of ghosts
ghosts = sprite.Group()
# Create the ghost and assign a random position
# ghost = Ghosts(10, "ghost.png", choice(pos), choice(pos))
for i in range(ghost_number):
  ghost_coordinate = choice(pos)
  ghost = Ghosts(5, "hacker.png", ghost_coordinate, ghost_coordinate)
  ghosts.add(ghost)

# Create the player and assign the home position
# player = Player(5, "player.png", 15, 15)
player = Player(5, "developer.png", 25, 25)

# Create the randomly positioned coins    
for i in range(12):
  # coin = Coin("coin.png", choice(pos), choice(pos))
  coin = Coin("bitcoin.png", choice(pos), choice(pos))
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
  # screen.fill(COLOUR_BK)
  
  # Display the background
  screen.blit(bg, (0,0))
  
  # Build the walls
  maze.draw(screen)
  
  # Draw the wallet
  wallet.update()
  
  # Add coins collected amount
  coins_collected_text = amount_font.render(str(coins_collected), True, (255,255,255))
  screen.blit(coins_collected_text, (wallet.rect.centerx-5, wallet.rect.centery-2))
  
  #Draw the group of coins
  coins.draw(screen)
  
  # Draw the ghost
  for ghost in ghosts:
   ghost.move(maze) # Get the ghost moving
  ghosts.draw(screen)
  
  # Draw the player
  player.update()
  player.controls() # control the player with the arrow keys
  
  # Pick up the coins
  coin_hit_list = sprite.spritecollide(player, coins, True)
  if coin_hit_list:
    coin_sound.play()
      
  for coin in coin_hit_list:
    coins_collected += 1 # Add them to the list to check for a win
  
  # Return the player home if it touches the walls or the ghost
  if sprite.spritecollide(player, maze, False) or sprite.collide_mask(player, ghost):
    slide_sound.play()
    player.rect.x = 15
    player.rect.y = 15
  
  # Check that all the coins have been collected, now the player can get the wallet
  if coins_collected == 12:
    win = Rect.colliderect(player.rect, wallet.rect)
    # Game over screen if the player wins
    if win == True:
      game_over = game_over_font.render("GAME OVER", True, "orange")
      screen.blit(game_over, (WIDTH/2 - 77, HEIGHT/2 - 10))
      win_sound.play()
      display.flip() # Update the screen
      time.delay(5000) # Show Game over for 5 seconds
      running = False
  
  display.update()
  clock.tick(60)
  
quit()