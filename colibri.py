from pygame import *
from random import randint

font.init()
score_font = font.Font(None,45)

# Get the variables
WIDTH = 1200
HEIGHT = 800

# Bird initial position
bird_width = 80
bird_height = 80
bird_x = WIDTH/4
bird_y = HEIGHT/2
step = 10
speed = 2

# Pipe variables
pipe_width = 150
pipe_x = WIDTH/2
gap = 200
COLOUR = (255, 145, 77, 200)

# Score
score = 0

# Set the display
# Size
screen = display.set_mode((WIDTH, HEIGHT))
# Game name
display.set_caption("Colibrí")
# Add a background image
background = transform.scale(image.load("mountains.jpg"), (WIDTH,HEIGHT))

clock = time.Clock()
running = True


# Define a class to load the image props into the game
class Props():
  def __init__(self, speed, img, x, y):
    self.speed = speed
    self.original_img = transform.scale(image.load(img), (bird_width, bird_height))
    self.img = self.original_img
    self.rect = self.img.get_rect()
    self.rect.center= x, y
    
  def update(self, screen):
    if self.rect.x < WIDTH - self.rect.w:
      self.rect.move_ip(0, speed) # Moves in place
    screen.blit(self.img, (self.rect.x, self.rect.y))
    
# Define Bird Class
class Bird(Props):
  def __init__(self,speed, img, x, y):
    super().__init__(speed, img, x, y)
    self.angle = 0
    
  def control(self):
    keys = key.get_pressed()
    if keys[K_SPACE] and self.rect.y > 5 and self.rect.y < HEIGHT-bird_height:
      self.rect.y -= 10
      self.angle = 15
  
  def rotate(self, screen, new_angle):
    """ Rotate towards a target angle and stop when reached"""
    if self.angle < new_angle:
      self.angle += self.speed
      if self.angle > new_angle:
        self.angle = new_angle
    if self.angle > new_angle:
      self.angle -= speed
      if self.angle < new_angle:
        self.angle = new_angle

    self.img = transform.rotate(self.original_img, self.angle) # Rotate from original
    self.rect = self.img.get_rect(center=self.rect.center) # Keep the center
    screen.blit(self.img, self.rect)
    
    # Update the mask after rotating
    self.mask = mask.from_surface(self.img)


# Pipe class
class Pipes():
  def __init__(self, speed, width, gap, pipe_x=pipe_x):
    self.speed = speed
    self.width = width
    self.height = randint(50, 450)
    self.top = Rect(pipe_x, 0, self.width, self.height)
    self.bottom = Rect(pipe_x, HEIGHT-(HEIGHT - (self.height + gap)), self.width, HEIGHT - (self.height + gap))
    self.passed = False
    
  # Method to move the pipes
  def update(self):
    self.top.move_ip(-self.speed, 0)
    self.bottom.move_ip(-self.speed, 0)
  
  #Method to draw the pipes onto the screen
  def draw_pipes(self, screen):
    # Make a transparent rectangle
    # Start by creating a surface the size of the rectangle
    s = Surface(self.top.size, SRCALPHA)
    # Draw the rectangle on this surface, in this case we added rounded corners
    draw.rect(s, COLOUR, s.get_rect(), 0, 0, -1, -1, 20, 20)
    #Add a mark to the pipe
    self.top_mask = mask.from_surface(s)
    # Add the surface to the screen 
    screen.blit(s, (self.top.x, self.top.y))
    
    #As above but for the bottom rectangle
    s_bottom = Surface(self.bottom.size, SRCALPHA)
    draw.rect(s_bottom, COLOUR, s_bottom.get_rect(), 0, 0, 20, 20, -1, -1)
    self.bottom_mask = mask.from_surface(s_bottom)
    screen.blit(s_bottom, (self.bottom.x, self.bottom.y))
    
  def reset(self):
    if self.top.x == 0:
      self.top.x = WIDTH
      self.bottom.x = WIDTH
      self.passed = False
   
# Load the bird image;
bird = Bird(speed, "colibri_pixelate.png", bird_x, bird_y)

# Create the pipes
pipe1 = Pipes(2, pipe_width, gap)
pipe2 = Pipes(2, pipe_width, gap, pipe_x+pipe_width*2)
pipe3 = Pipes(2, pipe_width, gap, pipe_x+(pipe_width*2)*2)
pipe4 = Pipes(2, pipe_width, gap, pipe_x+(pipe_width*2)*3)

# Function to move the bird
def move_bird(bird_rect, speed):
  if bird_rect.x < WIDTH - bird_rect.w:
    bird_rect.move_ip(speed, 0) # Moves in place
  
while running:
  
  dt = clock.tick(60) / 1000  # Get time passed in seconds
  
  # Add background and bird t screen
  screen.blit(background, (0,0));

  # Quit event to use the X to end the game
  for e in event.get():
    if e.type == QUIT:
      quit()
      running = False
  
  
  # Move the bird
  bird.control()
  bird.update(screen)
  bird.rotate(screen, -15)
  # screen.blit(bird.img, bird.rect)
  
  
  if bird.rect.right > pipe1.top.right and not pipe1.passed:
    print("Case 1")
    pipe1.passed = True
    score += 1
  if bird.rect.right > pipe2.top.right and not pipe2.passed:
    print("Case 2")
    pipe2.passed = True
    score += 1
  if bird.rect.right > pipe3.top.right and not pipe3.passed:
    print("Case 3")
    pipe3.passed = True
    score += 1
  if bird.rect.right > pipe4.top.right and not pipe4.passed:
    print("Case 4")
    pipe4.passed = True
    score += 1
    
  # Draw pipes
  pipe1.draw_pipes(screen)
  pipe1.update()
  pipe1.reset()
  pipe2.draw_pipes(screen)
  pipe2.update()
  pipe2.reset()
  pipe3.draw_pipes(screen)
  pipe3.update()
  pipe3.reset()
  pipe4.draw_pipes(screen)
  pipe4.update()
  pipe4.reset()
  
  score_text = score_font.render(str(score), True, (0, 0, 0))
  screen.blit(score_text, (WIDTH - 50, 50))
                                 
  if bird.rect.y >= HEIGHT - bird.rect.h:
    game_over = score_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (WIDTH/2 - 90, HEIGHT/2 + 40))
    display.flip() # Update the screen
    time.delay(2000) # Show Game over for 5 seconds
    running = False
  
  if bird.mask.overlap(pipe1.top_mask, (pipe1.top.x - bird.rect.x, pipe1.top.y - bird.rect.y)) or bird.mask.overlap(pipe1.bottom_mask, (pipe1.bottom.x - bird.rect.x, pipe1.bottom.y - bird.rect.y)):
    game_over = score_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (WIDTH/2 - 90, HEIGHT/2 + 40))
    display.flip() # Update the screen
    time.delay(2000) # Show Game over for 5 seconds
    running = False
    
  if bird.mask.overlap(pipe2.top_mask, (pipe2.top.x - bird.rect.x, pipe2.top.y - bird.rect.y)) or bird.mask.overlap(pipe2.bottom_mask, (pipe2.bottom.x - bird.rect.x, pipe2.bottom.y - bird.rect.y)):
    game_over = score_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (WIDTH/2 - 90, HEIGHT/2 + 40))
    display.flip() # Update the screen
    time.delay(2000) # Show Game over for 5 seconds
    running = False
    
  if bird.mask.overlap(pipe3.top_mask, (pipe3.top.x - bird.rect.x, pipe3.top.y - bird.rect.y)) or bird.mask.overlap(pipe3.bottom_mask, (pipe3.bottom.x - bird.rect.x, pipe3.bottom.y - bird.rect.y)):
    game_over = score_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (WIDTH/2 - 90, HEIGHT/2 + 40))
    display.flip() # Update the screen
    time.delay(2000) # Show Game over for 5 seconds
    running = False
    
  if bird.mask.overlap(pipe4.top_mask, (pipe4.top.x - bird.rect.x, pipe4.top.y - bird.rect.y)) or bird.mask.overlap(pipe4.bottom_mask, (pipe4.bottom.x - bird.rect.x, pipe4.bottom.y - bird.rect.y)):
    game_over = score_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (WIDTH/2 - 90, HEIGHT/2 + 40))
    display.flip() # Update the screen
    time.delay(2000) # Show Game over for 5 seconds
    running = False
  
  display.flip()
quit()