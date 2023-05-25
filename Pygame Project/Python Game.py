import pygame
import os
pygame.font.init()
pygame.mixer.init()

#BLUE SPACESHIP: fast/small bullets, less hp, fast move speed
#RED SPACESHIP: slow/big bullets, more hp, slow move speed

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (155, 0, 0)
BLUE = (0, 200, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('ZeroHour-Regular', 40)
WINNER_FONT = pygame.font.SysFont('ZeroHour-Regular', 100)

FPS = 60
VEL = 5
VEL2 = 7
RED_BULLET_VEL = 7
BLUE_BULLET_VEL = 10
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 90, 70

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'L spaceship png.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'W spaceship png.png'))
BLUE_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'purple galaxy.png')), (WIDTH, HEIGHT))

def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    blue_health_text = HEALTH_FONT.render("BLUE HP: " + str(blue_health), 1 ,BLUE)
    red_health_text = HEALTH_FONT.render("RED HP: " + str(red_health), 1 ,RED)
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width(), HEIGHT - blue_health_text.get_height()))
    WIN.blit(red_health_text, (10, 10))    


    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
    WIN.blit(BLUE_SPACESHIP_IMAGE, (blue.x, blue.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    pygame.display.update()

    


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0 : #goes left
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < WIDTH - SPACESHIP_WIDTH: #goes right
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0 : #goes up
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT//2-5 - SPACESHIP_HEIGHT: #goes down
        red.y += VEL

def blue_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL2 > 0: #goes left
        blue.x -= VEL2
    if keys_pressed[pygame.K_RIGHT] and blue.x + VEL2 < WIDTH - SPACESHIP_WIDTH: #goes right
        blue.x += VEL2
    if keys_pressed[pygame.K_UP] and blue.y - VEL2 > HEIGHT//2 + 5: #goes up
        blue.y -= VEL2
    if keys_pressed[pygame.K_DOWN] and blue.y + VEL2 < HEIGHT-SPACESHIP_HEIGHT: #goes down
        blue.y += VEL2

def handle_bullets(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.y += RED_BULLET_VEL      
        if blue.colliderect(bullet):     
            pygame.event.post(pygame.event.Event(BLUE_HIT))      
            red_bullets.remove(bullet)       
        elif bullet.y > HEIGHT:     
            red_bullets.remove(bullet)       


    for bullet in blue_bullets:
        bullet.y -= BLUE_BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.y < 0:
            blue_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PURPLE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    

def main():
    blue = pygame.Rect(100, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets = []
    red_bullets = []

    blue_health = 12
    red_health = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width // 2 - 5, red.y + red.height - 0, 10, 20)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width // 2 - 1.5, blue.y + blue.height - 70 , 5, 10)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if blue_health <= 0:
            winner_text = "RED WINS!"

        if red_health <= 0:
            winner_text = "BLUE WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break


                
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        blue_movement(keys_pressed, blue)

        handle_bullets(red_bullets, blue_bullets, red, blue)

        draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health)

    main()

if __name__ == "__main__":
    main()