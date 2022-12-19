import os
import pygame

# Init game modules
pygame.font.init()
pygame.mixer.init()

# WINDOW
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('First Game!')
FPS = 60

# EVENTS
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# SOUNDS
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))

# FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# COLORS
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_YELLOW = (255,255,0)

# GAME OBJECTS

# Middle border
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Spaceships
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
  # Draw background
  WIN.blit(SPACE, (0,0))

  # Draw middle border
  pygame.draw.rect(WIN, COLOR_BLACK, BORDER)

  # Display spaceships health
  red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, COLOR_WHITE)
  yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, COLOR_WHITE)
  WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
  WIN.blit(yellow_health_text, (10, 10))

  # Draw spaceships
  WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
  WIN.blit(RED_SPACESHIP, (red.x, red.y))

  # Draw bullets
  for bullet in red_bullets:
    pygame.draw.rect(WIN, COLOR_RED, bullet)
  for bullet in yellow_bullets:
    pygame.draw.rect(WIN, COLOR_YELLOW, bullet)
  
  # Update the game view
  pygame.display.update()

# Handle Yellow player movement with ZQSD
def yellow_handle_movement(keys_pressed, yellow):
  if keys_pressed[pygame.K_q] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
  if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
    yellow.x += VEL
  if keys_pressed[pygame.K_z] and yellow.y - VEL > 0: #UP
    yellow.y -= VEL
  if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
    yellow.y += VEL

# Handle Red player movement with arrow keys
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x  + BORDER.width: #LEFT
      red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
      red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
      red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15: #DOWN
      red.y += VEL

# Handle bullets movement and collision
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
  for bullet in yellow_bullets:
    bullet.x += BULLET_VEL
    if red.colliderect(bullet):
      pygame.event.post(pygame.event.Event(RED_HIT))
      yellow_bullets.remove(bullet)
    elif bullet.x > WIDTH:
      yellow_bullets.remove(bullet)
  for bullet in red_bullets:
    bullet.x -= BULLET_VEL
    if yellow.colliderect(bullet):
      pygame.event.post(pygame.event.Event(YELLOW_HIT))
      red_bullets.remove(bullet)
    elif bullet.x < 0:
      red_bullets.remove(bullet)

# Handle game over
def draw_winner(text):
  draw_text = WINNER_FONT.render(text, 1, COLOR_WHITE)
  WIN.blit(draw_text, (WIDTH / 2 -  draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
  pygame.display.update()
  pygame.time.delay(5000)

def main():
  red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
  yellow = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
  clock = pygame.time.Clock()
  red_bullets = []
  yellow_bullets = []
  red_health = 10
  yellow_health = 10
  run = True

  while run:
    # Sync clock to Frames per Second value
    clock.tick(FPS)
    # Listen to events
    for event in pygame.event.get():
      # QUIT event
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
      # KEYDOWN event : Fire bullet
      if event.type == pygame.KEYDOWN:
        if  event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
          bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5 )
          yellow_bullets.append(bullet)
          BULLET_FIRE_SOUND.play()
        if event.key == pygame.K_RCTRL  and len(red_bullets) < MAX_BULLETS:
          bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
          red_bullets.append(bullet)
          BULLET_FIRE_SOUND.play()

      # USER event : player hit
      if event.type == RED_HIT:
        red_health -= 1
        BULLET_HIT_SOUND.play()
      if event.type == YELLOW_HIT:
        yellow_health -= 1
        BULLET_HIT_SOUND.play()
    
    winner_text = ''
    if red_health <= 0:
      winner_text = "Yellow Wins!"
    if yellow_health <= 0:
      winner_text = "Red Wins!"
    
    if winner_text != '':
      draw_winner(winner_text)
      break
    # Handle player movement
    keys_pressed = pygame.key.get_pressed()
    yellow_handle_movement(keys_pressed, yellow)
    red_handle_movement(keys_pressed, red)

    # Handle bullets
    handle_bullets(yellow_bullets, red_bullets, yellow, red)

    # Draw/update the game
    draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
  # Restart main loop if game over
  main()

if __name__ == '__main__':
  main()