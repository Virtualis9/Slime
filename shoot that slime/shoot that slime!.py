import pygame
import sys
import math
import random

pygame.init()

display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
hit_counter = 0
player_weapon = pygame.image.load("shotgun.png").convert_alpha()

turret_original = pygame.image.load("guard.png").convert_alpha()
x = 400
y = 300


# Player class
class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        self.health = 100  # player's health

    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0
        self.animation_count += 1


# This is the bullet from the gun
class PlayerBullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 25  # Adjust the bullet speed here
        self.angle = angle
        self.x_vel = math.cos(math.radians(self.angle)) * self.speed
        self.y_vel = -math.sin(math.radians(self.angle)) * self.speed

    def main(self, display):
        self.x += int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


class SlimeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = [
            pygame.image.load("slime_animation_0.png"),
            pygame.image.load("slime_animation_1.png"),
            pygame.image.load("slime_animation_2.png"),
            pygame.image.load("slime_animation_3.png")
        ]
        self.animation_count = 0
        self.reset_offset = 0
        self.is_hit = False

    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.is_hit:
            global hit_counter
            enemies.remove(self)
            hit_counter += 1
            spawn_new_slimes(self.x, self.y)

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-50, 50)
            self.offset_y = random.randrange(-50, 50)
            self.reset_offset = random.randrange(20, 50)
        else:
            self.reset_offset -= 0.01

        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 1

        display.blit(pygame.transform.scale(self.animation_images[self.animation_count // 4], (32, 30)), (self.x - display_scroll[0], self.y - display_scroll[1]))

    def check_collision(self, bullets):
        for bullet in bullets:
            if bullet.x > self.x - display_scroll[0] and bullet.x < self.x - display_scroll[0] + 32:
                if bullet.y > self.y - display_scroll[1] and bullet.y < self.y - display_scroll[1] + 32:
                    bullets.remove(bullet)
                    self.is_hit = True
                    spawn_new_slimes(self.x, self.y)
                    break


def spawn_new_slimes(x, y):
    global hit_counter
    hit_counter += 1
    new_slimes = [SlimeEnemy(x - 32, y), SlimeEnemy(x + 32, y)]
    enemies.extend(new_slimes)


# Player and Enemy start position
enemies = [SlimeEnemy(700, 700)]
player = Player(400, 300, 32, 32)

display_scroll = [0, 0]

player_bullets = []

font = pygame.font.SysFont(None, 24)

# My while loop for when the game is running
while True:
    display.fill((24, 164, 86))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # This is the button on the mouse when pressed releases a bullet
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                angle = math.degrees(math.atan2(mouse_y - player.y, mouse_x - player.x))
                player_bullets.append(PlayerBullet(player.x, player.y, angle))

    keys = pygame.key.get_pressed()

    # get mouse position
    pos = pygame.mouse.get_pos()

    # calculate turret angle
    x_dist = pos[0] - x
    y_dist = -(pos[1] - y)  # -ve because pygame y coordinates increase down the screen
    angle = math.degrees(math.atan2(y_dist, x_dist))

    # rotate turret
    turret = pygame.transform.rotate(turret_original, angle - -90)
    turret_rect = turret.get_rect(center=(x, y))

    # drawn rectangle to show the player is moving on the screen 255,255,255 is RGB for white
    pygame.draw.rect(
        display, (255, 255, 255), (500 - display_scroll[0], 500 - display_scroll[1], 32, 32)
    )

    # draw image
    display.blit(turret, turret_rect)

    # IF statements for key pressing moving character
    if keys[pygame.K_a]:
        display_scroll[0] -= 3

        player.moving_left = True

        for bullet in player_bullets:
            bullet.x -= 3

    if keys[pygame.K_d]:
        display_scroll[0] += 3

        player.moving_right = True

        for bullet in player_bullets:
            bullet.x += 0.5

    if keys[pygame.K_w]:
        display_scroll[1] -= 3
        for bullet in player_bullets:
            bullet.y -= 0.5

    if keys[pygame.K_s]:
        display_scroll[1] += 3
        for bullet in player_bullets:
            bullet.y += 0.5

    # Here are all my displays in the game, everything that should appear needs to be called from here.
    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)

    for enemy in enemies:
        enemy.main(display)
        enemy.check_collision(player_bullets)  # Check collision with player bullets

    hit_counter_text = font.render("Hits: " + str(hit_counter), True, (255, 255, 255))
    display.blit(hit_counter_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
