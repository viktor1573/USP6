import pygame
import math
import random
import sqlite3

conn=sqlite3.connect("lifever.db")
logged=False
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("lifever")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Sessions" (
    "user_id" INTEGER,
    "session_id" INTEGER PRIMARY KEY AUTOINCREMENT
)
""")
conn.commit()

WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

''''buffs'''
health=0
speed=0
fit=0
range=0
size=0

d_square_size = 50
d_square_speed = 3
d_square_x = SCREEN_WIDTH // 2
d_square_y = SCREEN_HEIGHT // 2
d_player_health = 100
d_player_gold = 0
d_player_xp = 0
d_xp_required = 10
d_gold_rate = 5
''''stats'''
square_size = d_square_size
square_speed = d_square_speed
square_x = d_square_x
square_y = d_square_y
player_health = d_player_health
player_gold = d_player_gold
player_xp = d_player_xp
xp_required = d_xp_required
gold_rate = d_gold_rate

bullet_speed = 10
bullets = []
bullet_damage = 20
bullet_size = 5
reload_rate = 2000
last_shot = 0
gunner = []
gunner.append(1)

enemies = []
types = ['tanker','dasher','sniper']
enemy_spawn_rate = 5000
prev_spawn_rate = 0
last_enemy = 0
enemy_health = 40

tanker_size = 30
tanker_speed = 2
tanker_damage = 40

dasher_size = 30
dasher_speed = 200
dasher_teleport_time = 2000
dasher_damage = 30

sniper_size = 50
sniper_bullet_speed = 5
sniper_damage = 50
sniper_bullet_reload_rate = 3000
sniper_bullets = []

boss_size = 60
boss_laser_damage = 1
boss_laser_duration = 5000
boss_laser_cooldown = 5000
boss_health = 100
boss_count = 0
max_bosses = 5

gold_drops = []
d_IH = 5
d_IRR = 12
d_IBD = 8
d_IS = 12
d_DS = 15
d_AB = 40
d_IGD = 20
d_IBS = 15

c_IH = d_IH
c_IRR = d_IRR
c_IBD =d_IBD
c_IS = d_IS
c_DS = d_IBS
c_AB = d_AB
c_IGD = d_IGD
c_IBS = d_IBS

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
FPS = 60
xp = 1
background = pygame.image.load("5-dots.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def submit_score():
    global player_xp, player_gold

    cursor.execute("SELECT user_id FROM Sessions ORDER BY session_id DESC LIMIT 1")
    user_id = cursor.fetchone()[0]
    cursor.execute("UPDATE Users SET score = ? WHERE id = ?", (player_xp, user_id))
    conn.commit()
    leaderboard()
def leaderboard():
    window = pygame.Surface((400, 300))
    window.fill(WHITE)
    pygame.draw.rect(window, PURPLE, (0, 0, 400, 300), 5)

    cursor.execute("SELECT username, score FROM Users ORDER BY score DESC LIMIT 5")
    leaderboard = cursor.fetchall()

    y_offset = 50
    for idx, (username, score) in enumerate(leaderboard):
        positions = font.render(f"{idx + 1}. {username}: {score}", True, PURPLE)
        window.blit(positions, (50, y_offset))
        y_offset += 50

    screen.blit(window, (200, 150))
    pygame.display.flip()

    choose = True
    while choose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    choose = False
def register_login():
    global logged, health,speed,fit,range,size

    window = pygame.Surface((400, 300))
    window.fill(WHITE)
    pygame.draw.rect(window, PURPLE, (0, 0, 400, 300), 5)

    prompt_text = font.render("Enter Username:", True, PURPLE)
    window.blit(prompt_text, (50, 50))
    pygame.display.flip()

    username = ""
    entering = True
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username:
                        entering = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        window.fill(WHITE)
        pygame.draw.rect(window, PURPLE, (0, 0, 400, 300), 5)
        window.blit(prompt_text, (50, 50))
        username_text = font.render(username, True, PURPLE)
        window.blit(username_text, (50, 100))
        screen.blit(window, (200, 150))
        pygame.display.flip()

    cursor.execute("SELECT id FROM Users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        logged = True
        cursor.execute("INSERT INTO Sessions (user_id) VALUES (?)", (user_id,))
        conn.commit()
    else:
        build_id=random.randint(1,5)
        skin_id=random.randint(1,5)
        cursor.execute("INSERT INTO Users (username, score, build_id, skin_id) VALUES (?, 0, ?, ?)",
                       (username, build_id,skin_id))
        user_id = cursor.lastrowid
        logged = True
        cursor.execute("INSERT INTO Sessions (user_id) VALUES (?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT buff_id FROM Builds WHERE id=?", (build_id,))
        build_buff_id = cursor.fetchone()[0]
        cursor.execute("SELECT buff_id FROM Skins WHERE id=?", (skin_id,))
        skin_buff_id = cursor.fetchone()[0]

        cursor.execute("SELECT stat FROM Buffs WHERE id IN (?, ?)", (build_buff_id, skin_buff_id))
        buffs = cursor.fetchall()
        for buff in buffs:
            buff_types = buff[0].split()
            for buff_type in buff_types:
                if buff_type == 'health':
                    health = 0.0005
                elif buff_type == 'speed':
                    speed = 0.0002
                elif buff_type == 'bullet':
                    fit = 0.0003
                elif buff_type == 'range':
                    range = 0.0003
                elif buff_type == 'size':
                    size = 0.0001
def game_over():
    global player_gold, player_health, reload_rate, bullet_damage, bullet_speed, bullet_size, square_speed, square_size, upgrades, c_DS, c_IH, c_IS, c_IGD, c_AB, c_IRR, c_IBD, c_IBS, logged

    window = pygame.Surface((400, 300))
    window.fill(WHITE)
    pygame.draw.rect(window, PURPLE, (0, 0, 400, 300), 5)

    upgrade_text = font.render("Game Over", True, PURPLE)
    window.blit(upgrade_text, (120, 130))
    record_text = font.render("Press K to Submit Score", True, PURPLE)
    window.blit(record_text, (80, 160))

    screen.blit(window, (200, 150))
    pygame.display.flip()
    waiting_for_choice = True
    while waiting_for_choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    choice = 1
                    waiting_for_choice = False
    if choice == 1:
        if logged:
            submit_score()
        else:
            register_login()
    game_restart()
def game_restart():
    global c_IH,c_IRR,c_IBD,c_IS,c_DS,c_AB,c_IGD,c_IBS,\
        square_size,square_speed,square_x,square_y,player_health,player_gold,player_xp,xp_required,gold_rate,enemy_spawn_rate,screen,background
    c_IH = d_IH
    c_IRR = d_IRR
    c_IBD = d_IBD
    c_IS = d_IS
    c_DS = d_IBS
    c_AB = d_AB
    c_IGD = d_IGD
    c_IBS = d_IBS

    square_size = d_square_size
    square_speed = d_square_speed
    square_x = d_square_x
    square_y = d_square_y
    player_health = d_player_health
    player_gold = d_player_gold
    player_xp = d_player_xp
    xp_required = d_xp_required
    gold_rate = d_gold_rate
    enemy_spawn_rate=5000

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("lifever")
    background = pygame.image.load("5-dots.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def upgrade_window():
    global player_gold, player_health, reload_rate, bullet_damage, bullet_speed, bullet_size, square_speed, square_size, upgrades, c_DS, c_IH, c_IS, c_IGD, c_AB, c_IRR, c_IBD, c_IBS
    upgrades = [
        (f"Increase Health: ${c_IH}", "player_health", c_IH),
        (f"Increase Reload Rate: ${c_IRR}", "reload_rate", c_IRR),
        (f"Increase Bullet Damage: ${c_IBD}", "bullet_damage", c_IBD),
        (f"Increase Speed: ${c_IS}", "square_speed", c_IS),
        (f"Decrease Size: ${c_DS}", "square_size", c_DS),
        (f"Add Bullet 15 Degrees: ${c_AB}", "extra_bullet", c_AB),
        (f"Increase Gold Drop: ${c_IGD}", "gold_multiplier", c_IGD),
        (f"Increase Bullet Size: ${c_IBS}", "bullet_size", c_IBS)
    ]

    upgrade_choices = random.sample(upgrades, 3)

    window = pygame.Surface((400, 300))
    window.fill(WHITE)
    pygame.draw.rect(window, PURPLE, (0, 0, 400, 300), 5)

    for upg, (text, _, _) in enumerate(upgrade_choices):
        upgrade_text = font.render(f"{upg + 1}. {text}", True, PURPLE)
        window.blit(upgrade_text, (50, 50 + upg * 80))

    screen.blit(window, (200, 150))
    pygame.display.flip()

    choose = True
    while choose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if player_gold < upgrade_choices[0][2]:
                        choose = False
                        choice = "none"
                        break
                    choice = upgrade_choices[0][1]
                    player_gold -= upgrade_choices[0][2]
                    choose = False
                elif event.key == pygame.K_2:
                    if player_gold < upgrade_choices[1][2]:
                        choose = False
                        choice = "none"
                        break
                    choice = upgrade_choices[1][1]
                    player_gold -= upgrade_choices[1][2]
                    choose = False
                elif event.key == pygame.K_3:
                    if player_gold < upgrade_choices[2][2]:
                        choose = False
                        choice = "none"
                        break
                    choice = upgrade_choices[2][1]
                    player_gold -= upgrade_choices[2][2]
                    choose = False

    if choice == "player_health":
        player_health += 100
        c_IH = round(c_IH * 1.2)
    elif choice == "reload_rate":
        reload_rate = max(500, reload_rate - 200)
        c_IRR = round(c_IRR * 1.5)
    elif choice == "bullet_damage":
        bullet_damage += 15
        c_IBD = round(c_IBD * 1.7)
    elif choice == "bullet_size":
        bullet_size += 2
        c_IBS = round(c_IBS * 2)
    elif choice == "bullet_speed":
        bullet_speed += 1
        c_IBS = round(c_IBS * 2)
    elif choice == "square_speed":
        square_speed += 1
        c_IS = round(c_IS * 1.4)
    elif choice == "square_size":
        square_size -= 5
        c_DS = round(c_DS * 2.2)
    elif choice == "extra_bullet":
        if len(gunner) == 1:
            gunner.append(-15)
        else:
            gunner.append(15)
        c_AB = round(c_AB * 3)
    elif choice == "gold_multiplier":
        global gold_rate
        gold_rate += 2
        c_IGD = round(c_IGD * 2.5)
    else:
        pass

running = True
while running:
    player_xp += xp
    player_health+=health
    square_speed+=speed
    bullet_damage+=fit
    bullet_speed+=range
    bullet_size+=size
    if player_xp == 10000:
        types.append('boss')
    if player_xp == 14000:
        types.pop(3)
    enemy_spawn_rate -= enemy_spawn_rate / 60000
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0] and current_time - last_shot > reload_rate:
        last_shot = current_time
        for shot in gunner:
            angle = math.atan2(mouse_y - square_y, mouse_x - square_x) + math.radians(shot)
            shot_dx = bullet_speed * math.cos(angle)
            shot_dy = bullet_speed * math.sin(angle)
            bullets.append([square_x, square_y, shot_dx, shot_dy])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        square_x -= square_speed
    if keys[pygame.K_d]:
        square_x += square_speed
    if keys[pygame.K_w]:
        square_y -= square_speed
    if keys[pygame.K_s]:
        square_y += square_speed
    if keys[pygame.K_x]:
        upgrade_window()

    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= SCREEN_WIDTH and 0 <= bullet[1] <= SCREEN_HEIGHT]

    if current_time - last_enemy > enemy_spawn_rate:
        last_enemy = current_time
        enemy_type = random.choice(types)
        spawn_side = random.choice(['top', 'bottom', 'left', 'right'])

        if spawn_side == 'top':
            enemy_x = random.randint(0, SCREEN_WIDTH)
            enemy_y = 0
        elif spawn_side == 'bottom':
            enemy_x = random.randint(0, SCREEN_WIDTH)
            enemy_y = SCREEN_HEIGHT
        elif spawn_side == 'left':
            enemy_x = 0
            enemy_y = random.randint(0, SCREEN_HEIGHT)
        else:
            enemy_x = SCREEN_WIDTH
            enemy_y = random.randint(0, SCREEN_HEIGHT)

        if enemy_type == 'tanker':
            enemies.append({
                'type': 'tanker',
                'x': enemy_x,
                'y': enemy_y,
                'health': enemy_health
            })
        elif enemy_type == 'dasher':
            enemies.append({
                'type': 'dasher',
                'x': enemy_x,
                'y': enemy_y,
                'health': enemy_health,
                'last_teleport': current_time
            })

        elif enemy_type == 'sniper':
            enemies.append({
                'type': 'sniper',
                'x': enemy_x,
                'y': enemy_y,
                'health': enemy_health,
                'last_shot': current_time
            })
        elif enemy_type == 'boss':
            enemies.append({
                'type': 'boss',
                'x': enemy_x,
                'y': enemy_y,
                'health': boss_health,
                'last_shot': current_time,
                'laser_start': None
            })

    new_enemies = []
    for enemy in enemies:
        if enemy['type'] == 'tanker':
            angle = math.atan2(square_y - enemy['y'], square_x - enemy['x'])
            enemy['x'] += tanker_speed * math.cos(angle)
            enemy['y'] += tanker_speed * math.sin(angle)

            if abs(enemy['x'] - square_x) < square_size and abs(enemy['y'] - square_y) < square_size:
                player_health -= tanker_damage
                if player_health<1:
                    game_over()
                continue

        elif enemy['type'] == 'dasher':
            if current_time - enemy['last_teleport'] > dasher_teleport_time:
                enemy['last_teleport'] = current_time
                angle = math.atan2(square_y - enemy['y'], square_x - enemy['x'])
                enemy['x'] += dasher_speed * math.cos(angle)
                enemy['y'] += dasher_speed * math.sin(angle)

                if abs(enemy['x'] - square_x) < square_size and abs(enemy['y'] - square_y) < square_size:
                    player_health -= dasher_damage
                    if player_health < 1:
                        game_over()
                    continue

        elif enemy['type'] == 'sniper':
            if current_time - enemy['last_shot'] > sniper_bullet_reload_rate:
                enemy['last_shot'] = current_time
                angle = math.atan2(square_y - enemy['y'], square_x - enemy['x'])
                bullet_dx = sniper_bullet_speed * math.cos(angle)
                bullet_dy = sniper_bullet_speed * math.sin(angle)
                sniper_bullets.append([enemy['x'], enemy['y'], bullet_dx, bullet_dy])


        elif enemy['type'] == 'boss':

            if current_time - enemy['last_shot'] > boss_laser_cooldown:
                enemy['laser_start'] = current_time
                if spawn_side == 'top' or spawn_side == 'bottom':
                    if abs(square_x - enemy['x']) < boss_size:
                        player_health -= boss_laser_damage
                else:
                    if abs(square_y - enemy['y']) < boss_size:
                        player_health -= boss_laser_damage
            if player_health<1:
                game_over()

        enemy_alive = True
        for bullet in bullets:
            if abs(bullet[0] - enemy['x']) < square_size and abs(bullet[1] - enemy['y']) < square_size:
                enemy['health'] -= bullet_damage
                bullets.remove(bullet)
                if enemy['health'] <= 0:
                    enemy_alive = False
                    gold_drops.append((enemy['x'], enemy['y']))
                    break

        if enemy_alive:
            new_enemies.append(enemy)
    enemies = new_enemies

    new_sniper_bullets = []
    for bullet in sniper_bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

        if abs(bullet[0] - square_x) < square_size and abs(bullet[1] - square_y) < square_size / 2:
            player_health -= sniper_damage
            if player_health < 1:
                game_over()
            pygame.draw.rect(screen, RED, (draw_square_x, draw_square_y, square_size, square_size))
        else:
            new_sniper_bullets.append(bullet)
    sniper_bullets = new_sniper_bullets

    new_gold_drops = []
    for gold in gold_drops:
        if abs(gold[0] - square_x) < square_size and abs(gold[1] - square_y) < square_size:
            player_gold += random.randint(1, gold_rate)
        else:
            new_gold_drops.append(gold)
    gold_drops = new_gold_drops

    screen.blit(background, (0, 0))
    draw_square_x = square_x
    draw_square_y = square_y
    pygame.draw.rect(screen, PURPLE, (draw_square_x, draw_square_y, square_size, square_size))

    for bullet in bullets:
        draw_bullet_x = bullet[0]
        draw_bullet_y = bullet[1]
        pygame.draw.circle(screen, RED, (int(draw_bullet_x), int(draw_bullet_y)), bullet_size)

    for bullet in sniper_bullets:
        draw_bullet_x = bullet[0]
        draw_bullet_y = bullet[1]
        pygame.draw.circle(screen, GREEN, (int(draw_bullet_x), int(draw_bullet_y)), 15)

    for enemy in enemies:
        draw_enemy_x = enemy['x']
        draw_enemy_y = enemy['y']
        if enemy['type'] == 'tanker':
            pygame.draw.rect(screen, YELLOW, (draw_enemy_x, draw_enemy_y, tanker_size, tanker_size))
        elif enemy['type'] == 'dasher':
            pygame.draw.polygon(screen, BLUE, [
                (draw_enemy_x, draw_enemy_y - dasher_size // 2),
                (draw_enemy_x - dasher_size // 2, draw_enemy_y + dasher_size // 2),
                (draw_enemy_x + dasher_size // 2, draw_enemy_y + dasher_size // 2)
            ])
        elif enemy['type'] == 'sniper':
            pygame.draw.circle(screen, RED, (int(draw_enemy_x), int(draw_enemy_y)), sniper_size)
        elif enemy['type'] == 'boss':
            pygame.draw.rect(screen, BLUE, (draw_enemy_x, draw_enemy_y, boss_size, boss_size))

    for gold in gold_drops:
        draw_gold_x = gold[0]
        draw_gold_y = gold[1]
        pygame.draw.circle(screen, YELLOW, (int(draw_gold_x), int(draw_gold_y)), 5)

    health_text = font.render(f"Health: {round(player_health)}", True, PURPLE)
    screen.blit(health_text, (10, 10))
    gold_text = font.render(f"Gold: {player_gold}", True, PURPLE)
    screen.blit(gold_text, (10, 50))
    xp_text = font.render(f"XP: {round(player_xp / 100)}", True, PURPLE)
    screen.blit(xp_text, (10, 90))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
