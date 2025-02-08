from pygame import *
from random import randint, choice
# import numpy as np # Imported numpy to manage image pixels and change colour - TBC

# Initialise the music
mixer.init()

# Load and play background music
mixer.music.load("./sounds/game-music-150676.mp3")
mixer.music.play(-1) # -1 causes the music to loop indefinitely
mixer.music.set_volume(0.2) # Set the volume to 20%

# Load the coin sound
coin_sound = mixer.Sound("./sounds/retro-coin-4-236671.mp3")

# Load the slide sound
slide_sound = mixer.Sound("./sounds/089048_woosh-slide-in-88642.mp3")

# Load the winning sound
win_sound = mixer.Sound("./sounds/game-bonus-144751.mp3")

# Load the loosing sound -- Add a timer to create a loosing situation
lose_sound = mixer.Sound("./sounds/sweet-game-over-sound-effect-230470.mp3")

# Initialise the font
font.init()
status_font = font.Font(None,45)
amount_font = font.Font(None,25)
winning_text = status_font.render("WINNER 🎉", True, "orange")
game_over = status_font.render("GAME OVER", True, "orange")

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

# Player
lives = 3

#Set the display
#Size
screen = display.set_mode((WIDTH, HEIGHT))
# Add background image
bg = transform.scale(image.load("./images/ai-generated-9088888_1280.jpg"), (WIDTH, HEIGHT))
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
    self.original_image = transform.smoothscale(image.load(img), (30,30)).convert_alpha()
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
    self.rect.x = 25
    self.rect.y = 25
    
class Ghosts(Props):
  def __init__(self, speed, img, x, y):
    super().__init__(speed, img, x, y)
    self.collide_rect = self.rect.inflate(-15,-15) # Smaller collision area
    self.direction = "left"
    self.vertical_direction = "up"
    
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
      
  def move_vertical(self, walls):
    """Moves the ghost and changes direction upon collision."""
    
    # Get the ghost moving
    if self.vertical_direction == "up":
      self.rect.y -= self.speed
    else:
      self.rect.y += self.speed
    
    # Check for collitions with walls
    if sprite.spritecollide(self, walls, False):
      # Undo movement
      if self.vertical_direction == "up":
        self.rect.y += self.speed # Move back
        self.vertical_direction = "down" # Change direction
      else:
        self.rect.y -= self.speed # Move back
        self.vertical_direction = "up" # Change direction
          
    # Handle screen bounderies separately:  
    if self.rect.y >= HEIGHT - self.rect.h:
      self.vertical_direction = "up"
    if self.rect.y  <= 5:
      self.vertical_direction = "down"
          
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

# Create and store the possible coins, wallet and ghosts positions
pos = [25, 110]
i = 110
while len(pos) < 10:
  i += 80
  pos.append(i)

# Create the wallet prop
wallet = Props(0, "./images/banking-4318911_640.png", choice(pos), choice(pos))

# Create a group of ghosts
ghosts = sprite.Group()
ghosts_vertical = sprite.Group()

# Change to avoid the ghost hitting the player at home
ghost_pos = pos.copy()
ghost_pos.remove(25)
print(ghost_pos)
# Create the ghost and assign a random position
for i in range(ghost_number):
  ghost_coordinate = choice(ghost_pos)
  ghost = Ghosts(5, "./images/hacker.png", ghost_coordinate, ghost_coordinate)
  ghosts.add(ghost)
  
# Add ghosts to the group that will move vertically
for i in range(ghost_number):
  ghost_coordinate = choice(ghost_pos)
  ghost = Ghosts(5, "./images/hacker.png", ghost_coordinate, ghost_coordinate)
  ghosts_vertical.add(ghost)

# Create the player and assign the home position
# player = Player(5, "player.png", 15, 15)
player = Player(5, "./images/developer.png", 25, 25)

# Create the randomly positioned coins    
for i in range(12):
  # coin = Coin("coin.png", choice(pos), choice(pos))
  coin = Coin("./images/bitcoin.png", choice(pos), choice(pos))
  coins.add(coin)

# Variable to start and stop the loop
running = True
end = False

# Start the game loop
while running:
  
  # Quit game when pressing X on the window
  for e in event.get():
    if e.type == QUIT:
      quit()
      running = False
  
  if end != True:   
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
    
    # Add number of lives to screen
    lives_text = status_font.render(str(lives), True, (255,255,255))
    screen.blit(lives_text, (WIDTH - 50, 25))
    # Draw the ghost
    for ghost in ghosts:
        ghost.move(maze) # Get the ghosts moving
    for ghost in ghosts_vertical:
        ghost.move_vertical(maze) # Get 4 ghosts moving vertical
        
    ghosts.draw(screen)
    ghosts_vertical.draw(screen)
    
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
    if sprite.spritecollide(player, maze, False) or sprite.spritecollide(player, ghosts, False) or sprite.spritecollide(player, ghosts_vertical, False):
      slide_sound.play()
      lives -= 1
      player.rect.x = 25
      player.rect.y = 25
    
    # Check that all the coins have been collected, now the player can get the wallet
    if coins_collected == 12 and Rect.colliderect(player.rect, wallet.rect):
      end = True
      win = True
      screen.blit(winning_text, (WIDTH/2 - 70, HEIGHT/2 - 10))
      win_sound.play()
      player.rect.x = 25
      player.rect.y = 25
      time.delay(5000)
    
    if lives == 0:
      end = True
      win = False
      screen.blit(game_over, (WIDTH/2 - 77, HEIGHT/2 - 10))
      lose_sound.play()
  
  else:
    end = False
    lives = 3
    if win == True:
      coins_collected = 0
      for c in coins:
        c.kill()
      # Create the randomly positioned coins    
      for i in range(12):
        coin = Coin("./images/bitcoin.png", choice(pos), choice(pos))
        coins.add(coin)
    time.delay(3000)
  
  display.update()
  clock.tick(60)
  
quit()