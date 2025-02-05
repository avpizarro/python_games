from pygame import *
from random import randint, choice

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
    self.image = transform.scale(image.load(img), (40,40))
    self.rect = self.image.get_rect()
    self.rect.x = x_pos
    self.rect.y = y_pos
      
  def draw_coin(self, position):
    screen.blit(self.img, position)
    
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

# store the possible coin positions
pos = [15, 95]
i = 95
while len(pos) < 13:
  i += 60
print(pos)
  
for i in range(12):
  coin = Coin("coin.png", choice(pos), choice(pos))
  coins.add(coin)

# Variable to start and stop the loop
running = True

while running:
  
  # Quit game when pressing X on the window
  for e in event.get():
    if e.type == QUIT:
      running = False
      quit()
      
  # Add a colour to the display
  screen.fill(COLOUR_BK)
  
  # Build the walls
  for wall in walls_horizontal:
    wall.build_wall_horizontal()
  for wall in walls_vertical:
    wall.build_wall_vertical()
  
  # Draw coins
  coins.draw(screen)
        
  display.flip()

quit()
