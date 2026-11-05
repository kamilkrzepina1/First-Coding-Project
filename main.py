
import pygame
import random
import math
import json
import os

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("POLSKA ODYSEJA KOSMICZNA")
clock = pygame.time.Clock()

# KOLORY
BLACK = (5, 5, 20)
WHITE = (255, 255, 255)
RED = (220, 20, 40)
YELLOW = (255, 230, 0)
GREEN = (0, 255, 100)
PURPLE = (150, 0, 220)
LIGHT_PURPLE = (210, 100, 255)
DARK_PURPLE = (65, 0, 100)
PINK = (255, 50, 180)
ORANGE = (255, 130, 20)
GOLD = (255, 210, 0)
BLUE = (30, 100, 255)
CYAN = (0, 220, 255)

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 25)
big_font = pygame.font.Font(None, 80)
title_font = pygame.font.Font(None, 75)

menu_title_font = pygame.font.Font(None, 65)
menu_subtitle_font = pygame.font.Font(None, 34)
menu_prompt_font = pygame.font.Font(None, 38)

RECORDS_FILE = "rekordy.json"

PLAYER_SPEED = 8

# BONUSY
MAX_LIVES = 5
BONUS_DROP_CHANCE = 0.20
BONUS_SPEED = 3

NORMAL_SHOOT_DELAY = 300
RAPID_SHOOT_DELAY = 110
RAPID_FIRE_DURATION = 6000

# SYSTEM POZIOMOW
KILLS_TO_BOSS = 10
LEVEL_TRANSITION_DURATION = 3000

LEVELS = [
    {"name": "ZIEMSKA ORBITA", "boss": "NISZCZYCIEL ORBITALNY"},
    {"name": "MARS", "boss": "MARSJANSKI KOLOS"},
    {"name": "PLANETA CIENI", "boss": "WIDMO GALAKTYKI"},
    {"name": "STACJA IMPERIUM", "boss": "GENERAL MECHANICUS"},
    {"name": "SERCE GALAKTYKI", "boss": "WLADCA WSZECHSWIATA"}
]


# ==================================================
# REKORDY
# ==================================================

def load_records():
    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, "r", encoding="utf-8") as file:
                records = json.load(file)

            if isinstance(records, list):
                return records

        except (json.JSONDecodeError, OSError):
            pass

    return []


def save_record(name, points):
    records = load_records()

    existing_record = None

    for record in records:
        if str(record.get("name", "")).strip().casefold() == name.strip().casefold():
            existing_record = record
            break

    if existing_record:
        if points > existing_record.get("score", 0):
            existing_record["score"] = points
    else:
        records.append({"name": name, "score": points})

    records.sort(
        key=lambda record: record.get("score", 0),
        reverse=True
    )

    records = records[:5]

    with open(RECORDS_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

    return records


records = load_records()


# ==================================================
# TLO KOSMICZNE
# ==================================================

stars = []

for i in range(120):
    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.uniform(0.3, 1.2),
        "size": random.choice([1, 1, 1, 2]),
        "color": random.choice([
            (130, 140, 180),
            (150, 160, 200),
            (100, 170, 190),
            (170, 130, 190)
        ])
    })


background = pygame.Surface((WIDTH, HEIGHT))

for y in range(HEIGHT):
    darkness = int(5 + y * 0.025)

    color = (3, 4 + darkness // 5, 15 + darkness)

    pygame.draw.line(background, color, (0, y), (WIDTH, y))


space_clouds = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

pygame.draw.ellipse(space_clouds, (30, 90, 180, 12), (-100, 60, 280, 180))
pygame.draw.ellipse(space_clouds, (20, 110, 160, 12), (620, 300, 260, 200))
pygame.draw.ellipse(space_clouds, (45, 65, 160, 10), (40, 480, 250, 150))

galaxy_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


def create_galaxy(x, y, size, rotation=0):
    pygame.draw.ellipse(
        galaxy_surface,
        (20, 90, 190, 13),
        (x - size, y - size // 2, size * 2, size)
    )

    pygame.draw.ellipse(
        galaxy_surface,
        (30, 140, 220, 12),
        (x - size * 0.7, y - size * 0.35,
         size * 1.4, size * 0.7)
    )

    for arm in range(2):
        points = []

        for step in range(90):
            angle = step * 0.10 + arm * math.pi + rotation
            distance = step * size / 90

            px = x + math.cos(angle) * distance
            py = y + math.sin(angle) * distance * 0.48

            points.append((int(px), int(py)))

        if len(points) > 1:
            pygame.draw.lines(
                galaxy_surface,
                (65, 150, 230, 45),
                False,
                points,
                2
            )

        for i in range(5, len(points), 12):
            px, py = points[i]
            pygame.draw.circle(
                galaxy_surface,
                (120, 195, 255, 85),
                (px, py),
                1
            )

    pygame.draw.circle(
        galaxy_surface,
        (100, 180, 240, 65),
        (x, y),
        max(3, size // 12)
    )

    pygame.draw.circle(
        galaxy_surface,
        (180, 220, 255, 90),
        (x, y),
        2
    )


create_galaxy(65, 155, 48, 0.3)
create_galaxy(735, 420, 55, 1.5)
create_galaxy(690, 85, 35, 0.8)
create_galaxy(125, 500, 30, 2.0)


# ==================================================
# NOWE TLA POSZCZEGOLNYCH POZIOMOW
# ==================================================

def draw_earth():
    x, y, radius = 1040, 390, 245

    pygame.draw.circle(screen, (5, 20, 55), (x, y), radius + 15)
    pygame.draw.circle(screen, (20, 75, 160), (x, y), radius)
    pygame.draw.circle(screen, (30, 125, 210), (x - 15, y - 15), radius - 12)

    # Kontynenty
    pygame.draw.ellipse(screen, (45, 145, 85), (880, 270, 115, 75))
    pygame.draw.ellipse(screen, (45, 145, 85), (1010, 330, 90, 125))
    pygame.draw.ellipse(screen, (45, 145, 85), (1100, 250, 95, 65))
    pygame.draw.ellipse(screen, (45, 145, 85), (1130, 410, 65, 90))
    pygame.draw.ellipse(screen, (45, 145, 85), (900, 465, 80, 45))

    pygame.draw.circle(screen, (80, 180, 255), (x, y), radius, 5)

    # Delikatny cien
    shadow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(shadow, (0, 0, 20, 85), (x + 80, y + 10), radius)
    screen.blit(shadow, (0, 0))


def draw_mars():
    x, y, radius = 1030, 390, 245

    pygame.draw.circle(screen, (70, 20, 10), (x, y), radius + 12)
    pygame.draw.circle(screen, (170, 65, 35), (x, y), radius)
    pygame.draw.circle(screen, (205, 90, 45), (x - 25, y - 25), radius - 15)

    # Kratery
    pygame.draw.ellipse(screen, (125, 45, 30), (900, 280, 85, 45))
    pygame.draw.ellipse(screen, (125, 45, 30), (1050, 330, 100, 60))
    pygame.draw.ellipse(screen, (125, 45, 30), (970, 460, 70, 40))

    pygame.draw.ellipse(screen, (230, 120, 65), (900, 275, 75, 35), 3)
    pygame.draw.ellipse(screen, (230, 120, 65), (1055, 325, 90, 50), 3)

    pygame.draw.circle(screen, (255, 130, 75), (x, y), radius, 5)


def draw_shadow_planet():
    x, y, radius = 1040, 390, 245

    pygame.draw.circle(screen, (35, 5, 65), (x, y), radius + 15)
    pygame.draw.circle(screen, (55, 15, 90), (x, y), radius)
    pygame.draw.circle(screen, (90, 25, 130), (x - 45, y - 30), radius - 25)

    pygame.draw.ellipse(screen, (35, 5, 55), (900, 290, 100, 55))
    pygame.draw.ellipse(screen, (35, 5, 55), (1050, 360, 90, 65))
    pygame.draw.ellipse(screen, (35, 5, 55), (960, 470, 75, 40))

    pygame.draw.circle(screen, (160, 60, 220), (x, y), radius, 5)


def draw_imperial_station():
    x, y = 1030, 380

    # Konstrukcja stacji
    pygame.draw.circle(screen, (45, 55, 80), (x, y), 175, 20)
    pygame.draw.circle(screen, (90, 105, 135), (x, y), 115, 35)
    pygame.draw.circle(screen, (25, 35, 65), (x, y), 65)

    pygame.draw.rect(screen, (65, 75, 105), (x - 230, y - 30, 460, 60))
    pygame.draw.rect(screen, (45, 55, 85), (x - 30, y - 230, 60, 460))

    # Czerwone swiatla
    for i in range(-2, 3):
        pygame.draw.circle(screen, RED, (x + i * 70, y - 30), 7)
        pygame.draw.circle(screen, RED, (x + 30, y + i * 70), 7)

    pygame.draw.circle(screen, (130, 150, 190), (x, y), 175, 4)


def draw_galaxy_core():
    x, y = 1030, 360

    pygame.draw.circle(screen, (60, 20, 110), (x, y), 250)
    pygame.draw.circle(screen, (100, 35, 170), (x, y), 210)
    pygame.draw.circle(screen, (150, 65, 210), (x, y), 155)
    pygame.draw.circle(screen, (230, 150, 255), (x, y), 90)
    pygame.draw.circle(screen, (255, 220, 255), (x, y), 35)

    for angle in range(0, 360, 30):
        radians = math.radians(angle)

        start_x = x + math.cos(radians) * 100
        start_y = y + math.sin(radians) * 100

        end_x = x + math.cos(radians) * 245
        end_y = y + math.sin(radians) * 245

        pygame.draw.line(
            screen,
            (150, 80, 230),
            (int(start_x), int(start_y)),
            (int(end_x), int(end_y)),
            3
        )


def draw_level_background():
    screen.blit(background, (0, 0))

    if current_level == 1:
        draw_earth()
        screen.blit(space_clouds, (0, 0))

    elif current_level == 2:
        draw_mars()

    elif current_level == 3:
        draw_shadow_planet()

    elif current_level == 4:
        draw_imperial_station()

    elif current_level == 5:
        draw_galaxy_core()

    else:
        screen.blit(space_clouds, (0, 0))
        screen.blit(galaxy_surface, (0, 0))

    # Gwiazdy
    for star in stars:
        pygame.draw.circle(
            screen,
            star["color"],
            (int(star["x"]), int(star["y"])),
            star["size"]
        )

        star["y"] += star["speed"]

        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)


def draw_background():
    draw_level_background()


# ==================================================
# EFEKTY
# ==================================================

explosions = []


def create_explosion(x, y, boss_explosion=False):
    particles = []

    if boss_explosion:
        colors = [PURPLE, LIGHT_PURPLE, PINK, WHITE]
        amount = 100
    else:
        colors = [RED, ORANGE, YELLOW, WHITE]
        amount = 35

    for i in range(amount):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 8 if boss_explosion else 6)

        particles.append({
            "x": x,
            "y": y,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "size": random.choice([4, 6, 8, 10]),
            "life": random.randint(15, 35),
            "color": random.choice(colors)
        })

    explosions.append(particles)


# ==================================================
# SYSTEM BONUSOW
# ==================================================

bonuses = []
shield_active = False
rapid_fire_until = 0


def drop_bonus(x, y):
    if random.random() < BONUS_DROP_CHANCE:
        bonus_type = random.choice(["shield", "life", "rapid"])

        bonuses.append({
            "rect": pygame.Rect(x - 13, y - 13, 26, 26),
            "type": bonus_type
        })


def draw_bonus(bonus):
    rect = bonus["rect"]
    center = rect.center

    if bonus["type"] == "shield":
        pygame.draw.circle(screen, (10, 50, 140), center, 16)
        pygame.draw.circle(screen, CYAN, center, 12, 3)
        pygame.draw.circle(screen, WHITE, center, 4)

    elif bonus["type"] == "life":
        pygame.draw.circle(screen, (0, 100, 30), center, 16)
        pygame.draw.circle(screen, GREEN, center, 12)

        pygame.draw.polygon(
            screen,
            RED,
            [
                (center[0], center[1] + 8),
                (center[0] - 9, center[1]),
                (center[0] - 8, center[1] - 5),
                (center[0] - 3, center[1] - 6),
                (center[0], center[1] - 2),
                (center[0] + 3, center[1] - 6),
                (center[0] + 8, center[1] - 5),
                (center[0] + 9, center[1])
            ]
        )

    elif bonus["type"] == "rapid":
        pygame.draw.circle(screen, (130, 90, 0), center, 16)
        pygame.draw.circle(screen, YELLOW, center, 12)

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (center[0] + 2, center[1] - 10),
                (center[0] - 6, center[1] + 1),
                (center[0] - 1, center[1] + 1),
                (center[0] - 3, center[1] + 10),
                (center[0] + 7, center[1] - 3),
                (center[0] + 2, center[1] - 3)
            ]
        )


def collect_bonus(bonus):
    global shield_active, lives, rapid_fire_until

    current_time = pygame.time.get_ticks()

    if bonus["type"] == "shield":
        shield_active = True

    elif bonus["type"] == "life":
        lives = min(MAX_LIVES, lives + 1)

    elif bonus["type"] == "rapid":
        rapid_fire_until = current_time + RAPID_FIRE_DURATION


def draw_hearts(amount):
    for i in range(MAX_LIVES):
        x = WIDTH // 2 - 50 + i * 25
        y = 27

        color = RED if i < amount else (65, 35, 45)

        pygame.draw.polygon(
            screen,
            color,
            [
                (x, y + 8),
                (x - 9, y),
                (x - 8, y - 7),
                (x - 2, y - 8),
                (x, y - 3),
                (x + 2, y - 8),
                (x + 8, y - 7),
                (x + 9, y)
            ]
        )


def damage_player():
    global lives, shield_active, game_over

    if shield_active:
        shield_active = False

        create_explosion(player.centerx, player.centery, False)
        return

    lives -= 1

    create_explosion(player.centerx, player.centery)

    if lives <= 0:
        lives = 0
        game_over = True


def draw_player_shield():
    if shield_active:
        pygame.draw.ellipse(
            screen,
            CYAN,
            (player.x - 10, player.y - 8, player.width + 20, player.height + 16),
            3
        )

        pygame.draw.ellipse(
            screen,
            (100, 190, 255),
            (player.x - 14, player.y - 12, player.width + 28, player.height + 24),
            1
        )


# ==================================================
# POCISKI PRZECIWNIKOW
# ==================================================

enemy_bullets = []

last_enemy_shot = 0
enemy_shoot_delay = 1100

last_boss_shot = 0

boss_shoot_delay = 1200
BOSS_HEALTH = 10
BOSS_SPEED = 2
BOSS_BULLET_SPEED = 4


def shoot_enemy_bullet(enemy, player):
    dx = player.centerx - enemy.centerx
    dy = player.centery - enemy.centery

    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        distance = 1

    speed = 4

    dx = dx / distance * speed
    dy = dy / distance * speed

    enemy_bullets.append({
        "x": enemy.centerx,
        "y": enemy.bottom,
        "dx": dx,
        "dy": dy,
        "speed": speed,
        "color": (255, 65, 65),
        "size": 9
    })


def shoot_boss_bullets(boss, player):
    dx = player.centerx - boss.centerx
    dy = player.centery - boss.centery

    base_angle = math.atan2(dy, dx)

    for offset in [-0.3, 0, 0.3]:
        angle = base_angle + offset
        speed = BOSS_BULLET_SPEED

        enemy_bullets.append({
            "x": boss.centerx,
            "y": boss.bottom,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "speed": speed,
            "color": PINK,
            "size": 11
        })


def draw_enemy_bullet(bullet):
    x = int(bullet["x"])
    y = int(bullet["y"])
    size = bullet["size"]
    color = bullet["color"]

    pygame.draw.circle(screen, (90, 15, 35), (x, y), size + 4)
    pygame.draw.circle(screen, color, (x, y), size)
    pygame.draw.circle(screen, WHITE, (x, y), max(2, size // 3))


# ==================================================
# PRZECIWNICY
# ==================================================

def draw_enemy(enemy):
    x = enemy.x
    y = enemy.y

    pygame.draw.rect(screen, (100, 0, 20), (x + 2, y + 15, 8, 16))
    pygame.draw.rect(screen, (100, 0, 20), (x + 30, y + 15, 8, 16))

    pygame.draw.rect(screen, RED, (x + 8, y + 5, 24, 28))
    pygame.draw.rect(screen, RED, (x + 13, y, 14, 38))

    pygame.draw.rect(screen, (255, 70, 80), (x + 14, y + 5, 5, 4))
    pygame.draw.rect(screen, (255, 70, 80), (x + 22, y + 5, 5, 4))

    pygame.draw.rect(screen, YELLOW, (x + 12, y + 12, 5, 5))
    pygame.draw.rect(screen, YELLOW, (x + 23, y + 12, 5, 5))

    pygame.draw.rect(screen, BLACK, (x + 14, y + 13, 2, 3))
    pygame.draw.rect(screen, BLACK, (x + 25, y + 13, 2, 3))

    pygame.draw.rect(screen, (100, 0, 20), (x + 16, y + 25, 8, 4))

    pygame.draw.rect(screen, RED, (x + 5, y + 32, 8, 6))
    pygame.draw.rect(screen, RED, (x + 27, y + 32, 8, 6))

    pygame.draw.rect(screen, ORANGE, (x + 7, y + 38, 5, 3))
    pygame.draw.rect(screen, ORANGE, (x + 28, y + 38, 5, 3))


# ==================================================
# BOSS
# ==================================================

def draw_boss(boss):
    x = boss.x
    y = boss.y

    pygame.draw.rect(screen, DARK_PURPLE, (x, y + 25, 35, 35))
    pygame.draw.rect(screen, DARK_PURPLE, (x + 165, y + 25, 35, 35))

    pygame.draw.rect(screen, PURPLE, (x + 10, y + 35, 25, 20))
    pygame.draw.rect(screen, PURPLE, (x + 165, y + 35, 25, 20))

    pygame.draw.rect(screen, DARK_PURPLE, (x + 35, y + 10, 130, 65))
    pygame.draw.rect(screen, PURPLE, (x + 45, y + 5, 110, 70))
    pygame.draw.rect(screen, PURPLE, (x + 60, y, 80, 80))

    pygame.draw.rect(screen, LIGHT_PURPLE, (x + 55, y + 10, 15, 10))
    pygame.draw.rect(screen, LIGHT_PURPLE, (x + 130, y + 10, 15, 10))
    pygame.draw.rect(screen, LIGHT_PURPLE, (x + 75, y + 5, 12, 8))
    pygame.draw.rect(screen, LIGHT_PURPLE, (x + 113, y + 5, 12, 8))

    pygame.draw.rect(screen, PINK, (x + 65, y + 28, 25, 20))
    pygame.draw.rect(screen, PINK, (x + 110, y + 28, 25, 20))

    pygame.draw.rect(screen, RED, (x + 72, y + 33, 12, 12))
    pygame.draw.rect(screen, RED, (x + 117, y + 33, 12, 12))

    pygame.draw.rect(screen, WHITE, (x + 75, y + 34, 5, 5))
    pygame.draw.rect(screen, WHITE, (x + 120, y + 34, 5, 5))

    pygame.draw.rect(screen, DARK_PURPLE, (x + 80, y + 55, 40, 12))
    pygame.draw.rect(screen, PINK, (x + 88, y + 58, 24, 4))

    pygame.draw.rect(screen, LIGHT_PURPLE, (x + 20, y + 15, 10, 10))
    pygame.draw.rect(screen, LIGHT_PURPLE, (x + 170, y + 15, 10, 10))


# ==================================================
# TABELA REKORDOW
# ==================================================

def draw_leaderboard(records, start_y):
    title = font.render("TOP 5 GRACZY", True, GOLD)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, start_y)))

    for i, record in enumerate(records[:5]):
        name = str(record.get("name", "Gracz"))[:15]
        points = record.get("score", 0)
        color = GOLD if i == 0 else WHITE

        text = small_font.render(
            f"{i + 1}. {name} - {points} pkt",
            True,
            color
        )

        screen.blit(
            text,
            text.get_rect(center=(WIDTH // 2, start_y + 32 + i * 27))
        )

    if not records:
        empty = small_font.render(
            "Brak rekordow. Zagraj jako pierwszy!",
            True,
            WHITE
        )

        screen.blit(
            empty,
            empty.get_rect(center=(WIDTH // 2, start_y + 45))
        )


# ==================================================
# POLSKI MYSLIWIEC "LOS"
# ==================================================

def draw_player(player):
    x = player.x
    y = player.y

    flame = random.randint(8, 16)

    pygame.draw.ellipse(screen, (20, 80, 180), (x + 5, y + 42, 13, flame + 5))
    pygame.draw.ellipse(screen, (20, 80, 180), (x + 30, y + 42, 13, flame + 5))

    pygame.draw.polygon(screen, ORANGE, [(x + 7, y + 43), (x + 17, y + 43), (x + 12, y + 43 + flame)])
    pygame.draw.polygon(screen, ORANGE, [(x + 31, y + 43), (x + 41, y + 43), (x + 36, y + 43 + flame)])

    pygame.draw.polygon(screen, CYAN, [(x + 10, y + 43), (x + 14, y + 43), (x + 12, y + 43 + flame - 3)])
    pygame.draw.polygon(screen, CYAN, [(x + 34, y + 43), (x + 38, y + 43), (x + 36, y + 43 + flame - 3)])

    pygame.draw.polygon(
        screen, (65, 70, 85),
        [
            (x + 24, y + 17), (x + 47, y + 34), (x + 43, y + 43),
            (x + 27, y + 37), (x + 24, y + 32), (x + 21, y + 37),
            (x + 5, y + 43), (x + 1, y + 34)
        ]
    )

    pygame.draw.polygon(screen, WHITE, [(x + 22, y + 19), (x + 4, y + 34), (x + 8, y + 38), (x + 23, y + 33)])
    pygame.draw.polygon(screen, WHITE, [(x + 26, y + 19), (x + 44, y + 34), (x + 40, y + 38), (x + 25, y + 33)])

    pygame.draw.polygon(screen, RED, [(x + 4, y + 34), (x + 1, y + 34), (x + 5, y + 42), (x + 11, y + 39)])
    pygame.draw.polygon(screen, RED, [(x + 44, y + 34), (x + 47, y + 34), (x + 43, y + 42), (x + 37, y + 39)])

    pygame.draw.rect(screen, RED, (x + 7, y + 34, 4, 4))
    pygame.draw.rect(screen, WHITE, (x + 11, y + 34, 4, 4))
    pygame.draw.rect(screen, WHITE, (x + 7, y + 38, 4, 3))
    pygame.draw.rect(screen, RED, (x + 11, y + 38, 4, 3))

    pygame.draw.rect(screen, RED, (x + 33, y + 34, 4, 4))
    pygame.draw.rect(screen, WHITE, (x + 37, y + 34, 4, 4))
    pygame.draw.rect(screen, WHITE, (x + 33, y + 38, 4, 3))
    pygame.draw.rect(screen, RED, (x + 37, y + 38, 4, 3))

    pygame.draw.rect(screen, (55, 65, 85), (x + 7, y + 39, 9, 8), border_radius=2)
    pygame.draw.rect(screen, (55, 65, 85), (x + 32, y + 39, 9, 8), border_radius=2)

    pygame.draw.rect(screen, CYAN, (x + 9, y + 42, 5, 3))
    pygame.draw.rect(screen, CYAN, (x + 34, y + 42, 5, 3))

    pygame.draw.polygon(
        screen, (65, 70, 85),
        [
            (x + 24, y), (x + 30, y + 12), (x + 34, y + 39),
            (x + 24, y + 50), (x + 14, y + 39), (x + 18, y + 12)
        ]
    )

    pygame.draw.polygon(
        screen, WHITE,
        [
            (x + 24, y + 2), (x + 29, y + 14), (x + 31, y + 37),
            (x + 24, y + 46), (x + 17, y + 37), (x + 19, y + 14)
        ]
    )

    pygame.draw.polygon(
        screen, RED,
        [
            (x + 24, y + 3), (x + 27, y + 14), (x + 26, y + 27),
            (x + 24, y + 31), (x + 22, y + 27), (x + 21, y + 14)
        ]
    )

    pygame.draw.ellipse(screen, (20, 50, 100), (x + 19, y + 10, 10, 17))
    pygame.draw.ellipse(screen, (40, 160, 220), (x + 20, y + 11, 8, 13))
    pygame.draw.line(screen, (190, 245, 255), (x + 22, y + 13), (x + 24, y + 11), 2)

    pygame.draw.circle(screen, RED, (x + 4, y + 35), 2)
    pygame.draw.circle(screen, RED, (x + 44, y + 35), 2)

    pygame.draw.polygon(screen, WHITE, [(x + 24, y), (x + 21, y + 9), (x + 24, y + 7), (x + 27, y + 9)])
    pygame.draw.line(screen, RED, (x + 24, y + 2), (x + 24, y + 6), 2)


# ==================================================
# DUZY MYSLIWIEC NA EKRANIE STARTOWYM
# ==================================================

def draw_title_ship(x, y):
    flame = 15 + int(math.sin(pygame.time.get_ticks() * 0.015) * 5)

    pygame.draw.ellipse(screen, (15, 65, 180), (x + 25, y + 105, 30, flame + 15))
    pygame.draw.ellipse(screen, (15, 65, 180), (x + 105, y + 105, 30, flame + 15))

    pygame.draw.polygon(screen, ORANGE, [(x + 32, y + 108), (x + 48, y + 108), (x + 40, y + 108 + flame)])
    pygame.draw.polygon(screen, ORANGE, [(x + 112, y + 108), (x + 128, y + 108), (x + 120, y + 108 + flame)])

    pygame.draw.polygon(screen, CYAN, [(x + 36, y + 108), (x + 44, y + 108), (x + 40, y + 108 + flame - 5)])
    pygame.draw.polygon(screen, CYAN, [(x + 116, y + 108), (x + 124, y + 108), (x + 120, y + 108 + flame - 5)])

    pygame.draw.polygon(
        screen, (55, 65, 85),
        [
            (x + 80, y + 35), (x + 155, y + 95), (x + 145, y + 115),
            (x + 95, y + 100), (x + 80, y + 80), (x + 65, y + 100),
            (x + 15, y + 115), (x + 5, y + 95)
        ]
    )

    pygame.draw.polygon(screen, WHITE, [(x + 75, y + 40), (x + 18, y + 94), (x + 28, y + 103), (x + 77, y + 82)])
    pygame.draw.polygon(screen, WHITE, [(x + 85, y + 40), (x + 142, y + 94), (x + 132, y + 103), (x + 83, y + 82)])

    pygame.draw.polygon(screen, RED, [(x + 18, y + 94), (x + 5, y + 95), (x + 15, y + 115), (x + 35, y + 105)])
    pygame.draw.polygon(screen, RED, [(x + 142, y + 94), (x + 155, y + 95), (x + 145, y + 115), (x + 125, y + 105)])

    for sx in [28, 125]:
        pygame.draw.rect(screen, RED, (x + sx, y + 94, 8, 8))
        pygame.draw.rect(screen, WHITE, (x + sx + 8, y + 94, 8, 8))
        pygame.draw.rect(screen, WHITE, (x + sx, y + 102, 8, 7))
        pygame.draw.rect(screen, RED, (x + sx + 8, y + 102, 8, 7))

    pygame.draw.polygon(
        screen, (55, 65, 85),
        [
            (x + 80, y + 2), (x + 99, y + 35), (x + 105, y + 100),
            (x + 80, y + 125), (x + 55, y + 100), (x + 61, y + 35)
        ]
    )

    pygame.draw.polygon(
        screen, WHITE,
        [
            (x + 80, y + 7), (x + 94, y + 38), (x + 97, y + 96),
            (x + 80, y + 115), (x + 63, y + 96), (x + 66, y + 38)
        ]
    )

    pygame.draw.polygon(
        screen, RED,
        [
            (x + 80, y + 8), (x + 88, y + 38), (x + 85, y + 72),
            (x + 80, y + 82), (x + 75, y + 72), (x + 72, y + 38)
        ]
    )

    pygame.draw.ellipse(screen, (10, 35, 85), (x + 65, y + 30, 30, 42))
    pygame.draw.ellipse(screen, (35, 155, 220), (x + 69, y + 33, 22, 34))
    pygame.draw.line(screen, (190, 245, 255), (x + 75, y + 39), (x + 82, y + 34), 3)

    pygame.draw.circle(screen, RED, (x + 17, y + 98), 4)
    pygame.draw.circle(screen, RED, (x + 143, y + 98), 4)


# ==================================================
# FALUJACA POLSKA FLAGA
# ==================================================

def draw_polish_flag(x, y, current_time):
    pygame.draw.line(screen, (175, 185, 205), (x, y - 5), (x, y + 125), 5)
    pygame.draw.circle(screen, GOLD, (x, y - 8), 6)

    flag_width = 145
    flag_height = 82
    segments = 29

    for i in range(segments):
        t1 = i / segments
        t2 = (i + 1) / segments

        wave1 = math.sin(current_time * 0.005 + t1 * 7) * 7 * t1
        wave2 = math.sin(current_time * 0.005 + t2 * 7) * 7 * t2

        x1 = x + 4 + flag_width * t1
        x2 = x + 4 + flag_width * t2

        top1 = y + wave1
        top2 = y + wave2

        middle1 = y + flag_height / 2 + wave1
        middle2 = y + flag_height / 2 + wave2

        bottom1 = y + flag_height + wave1
        bottom2 = y + flag_height + wave2

        pygame.draw.polygon(
            screen, WHITE,
            [(int(x1), int(top1)), (int(x2), int(top2)),
             (int(x2), int(middle2)), (int(x1), int(middle1))]
        )

        pygame.draw.polygon(
            screen, RED,
            [(int(x1), int(middle1)), (int(x2), int(middle2)),
             (int(x2), int(bottom2)), (int(x1), int(bottom1))]
        )

        shade = int(15 + 15 * abs(math.sin(current_time * 0.005 + t1 * 7)))

        pygame.draw.line(
            screen,
            (max(0, 220 - shade), max(0, 220 - shade), max(0, 220 - shade)),
            (int(x1), int(top1)),
            (int(x1), int(middle1)),
            1
        )


# ==================================================
# EKRAN STARTOWY
# ==================================================

def draw_start_screen():
    draw_background()

    current_time = pygame.time.get_ticks()

    title = menu_title_font.render("POLSKA ODYSEJA", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 42))

    shadow = menu_title_font.render("POLSKA ODYSEJA", True, RED)

    screen.blit(shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title, title_rect)

    subtitle = menu_subtitle_font.render("KOSMICZNA", True, GOLD)
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 91)))

    pygame.draw.line(screen, WHITE, (250, 42), (390, 42), 4)
    pygame.draw.line(screen, RED, (250, 51), (390, 51), 4)

    pygame.draw.line(screen, WHITE, (890, 42), (1030, 42), 4)
    pygame.draw.line(screen, RED, (890, 51), (1030, 51), 4)

    ship_label = small_font.render("MYSLIWIEC L-OS", True, CYAN)
    screen.blit(ship_label, ship_label.get_rect(center=(WIDTH // 2, 135)))

    draw_title_ship(477, 150)
    draw_polish_flag(650, 175, current_time)

    instruction = font.render("WPISZ SWOJ NICK:", True, WHITE)
    screen.blit(instruction, instruction.get_rect(center=(WIDTH // 2, 310)))

    name_box = pygame.Rect(WIDTH // 2 - 210, 330, 420, 48)

    pygame.draw.rect(screen, (5, 10, 35), name_box, border_radius=8)
    pygame.draw.rect(screen, BLUE, name_box, 3, border_radius=8)

    cursor = "_" if (current_time // 500) % 2 == 0 else ""
    name_text = font.render(player_name + cursor, True, YELLOW)
    screen.blit(name_text, name_text.get_rect(center=name_box.center))

    if (current_time // 500) % 2 == 0:
        start_text = menu_prompt_font.render("NACISNIJ ENTER, ABY GRAC", True, GOLD)
        screen.blit(start_text, start_text.get_rect(center=(WIDTH // 2, 405)))

    controls = small_font.render(
        "RUCH: WASD / STRZALKI     STRZELANIE: SPACJA",
        True,
        CYAN
    )

    screen.blit(controls, controls.get_rect(center=(WIDTH // 2, 445)))

    pygame.draw.line(screen, GOLD, (WIDTH // 2 - 170, 465), (WIDTH // 2 + 170, 465), 2)

    draw_leaderboard(records, 480)


# ==================================================
# ZMIENNE GRY
# ==================================================

player_name = ""
game_started = False

player = pygame.Rect(WIDTH // 2 - 24, HEIGHT - 100, 48, 56)

enemies = []
bullets = []

last_shot = 0
shoot_delay = NORMAL_SHOOT_DELAY

score = 0
lives = 3

boss = None
boss_health = BOSS_HEALTH
boss_max_health = BOSS_HEALTH
boss_direction = 1
boss_active = False

game_over = False
campaign_complete = False
record_saved = False

current_level = 1
kills_in_level = 0

level_transition = False
level_transition_until = 0

restart_button = pygame.Rect(WIDTH // 2 - 150, 515, 300, 55)


def create_enemies():
    return [
        pygame.Rect(
            random.randint(0, WIDTH - 40),
            random.randint(-500, -50),
            40,
            40
        )
        for i in range(5)
    ]


def reset_level():
    global enemies, bullets, enemy_bullets, bonuses
    global boss, boss_health, boss_direction, boss_active
    global kills_in_level, last_enemy_shot, last_boss_shot

    enemies = create_enemies()
    bullets = []
    enemy_bullets = []
    bonuses = []

    boss = None
    boss_health = BOSS_HEALTH
    boss_direction = 1
    boss_active = False

    kills_in_level = 0

    current_time = pygame.time.get_ticks()
    last_enemy_shot = current_time
    last_boss_shot = current_time


def reset_game():
    global player
    global explosions
    global last_shot, score, lives
    global game_over, campaign_complete, record_saved
    global shield_active, rapid_fire_until
    global current_level, level_transition, level_transition_until

    player = pygame.Rect(WIDTH // 2 - 24, HEIGHT - 100, 48, 56)

    score = 0
    lives = 3

    shield_active = False
    rapid_fire_until = 0

    current_level = 1
    level_transition = False
    level_transition_until = 0

    game_over = False
    campaign_complete = False
    record_saved = False

    explosions = []

    last_shot = pygame.time.get_ticks()

    reset_level()


def start_next_level():
    global current_level, level_transition

    current_level += 1
    level_transition = False

    reset_level()


def defeat_boss():
    global boss_active, boss, score
    global level_transition, level_transition_until
    global campaign_complete, enemy_bullets

    if boss is not None:
        create_explosion(boss.centerx, boss.centery, True)

    boss_active = False
    boss = None

    score += 100
    enemy_bullets = []

    if current_level >= len(LEVELS):
        campaign_complete = True
    else:
        level_transition = True
        level_transition_until = pygame.time.get_ticks() + LEVEL_TRANSITION_DURATION


# ==================================================
# GLOWNA PETLA
# ==================================================

running = True

while running:
    clock.tick(60)

    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Wpisywanie nicku
        if not game_started and event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                if player_name.strip() != "":
                    player_name = player_name.strip()
                    game_started = True
                    reset_game()

            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]

            elif len(player_name) < 15 and event.unicode.isprintable():
                if event.unicode not in "\r\n\t":
                    player_name += event.unicode

        # Restart po przegranej lub ukonczeniu kampanii
        if game_over or campaign_complete:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restart_button.collidepoint(event.pos):
                        reset_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

    # EKRAN STARTOWY
    if not game_started:
        draw_start_screen()
        pygame.display.flip()
        continue

    # AUTOMATYCZNE PRZEJSCIE NA NASTEPNY POZIOM
    if level_transition and current_time >= level_transition_until:
        start_next_level()

    # AKTUALIZACJA GRY
    if not game_over and not campaign_complete and not level_transition:

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # RUCH STATKU
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= PLAYER_SPEED

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += PLAYER_SPEED

        player.clamp_ip(screen.get_rect())

        # STRZELANIE GRACZA
        current_shoot_delay = (
            RAPID_SHOOT_DELAY
            if current_time < rapid_fire_until
            else NORMAL_SHOOT_DELAY
        )

        if keys[pygame.K_SPACE]:
            if current_time - last_shot > current_shoot_delay:
                bullets.append(
                    pygame.Rect(player.centerx - 3, player.top, 6, 15)
                )
                last_shot = current_time

        # POCISKI GRACZA
        for bullet in bullets[:]:
            bullet.y -= 8

            if bullet.bottom < 0:
                bullets.remove(bullet)

        # POJAWIENIE SIE BOSSA
        if kills_in_level >= KILLS_TO_BOSS and not boss_active:
            boss = pygame.Rect(WIDTH // 2 - 100, 50, 200, 80)

            boss_health = boss_max_health
            boss_active = True
            enemy_bullets = []

        # ZWYKLI PRZECIWNICY
        if not boss_active:

            for enemy in enemies[:]:
                enemy.y += 2

                if enemy.top > HEIGHT:
                    enemy.y = random.randint(-200, -50)
                    enemy.x = random.randint(0, WIDTH - 40)

                if enemy.colliderect(player):
                    damage_player()
                    enemies.remove(enemy)

                    if not game_over:
                        enemies.append(
                            pygame.Rect(random.randint(0, WIDTH - 40), -50, 40, 40)
                        )

                    continue

                for bullet in bullets[:]:
                    if enemy.colliderect(bullet):
                        create_explosion(enemy.centerx, enemy.centery)

                        score += 10
                        kills_in_level += 1

                        drop_bonus(enemy.centerx, enemy.centery)

                        enemies.remove(enemy)
                        bullets.remove(bullet)

                        if kills_in_level < KILLS_TO_BOSS:
                            enemies.append(
                                pygame.Rect(random.randint(0, WIDTH - 40), -50, 40, 40)
                            )

                        break

            # PRZECIWNICY STRZELAJA
            current_time = pygame.time.get_ticks()

            if (
                enemies
                and kills_in_level < KILLS_TO_BOSS
                and current_time - last_enemy_shot > enemy_shoot_delay
            ):
                chosen_enemy = random.choice(enemies)
                shoot_enemy_bullet(chosen_enemy, player)
                last_enemy_shot = current_time

        # BOSS
        if boss_active and boss:
            boss.x += BOSS_SPEED * boss_direction

            if boss.right >= WIDTH or boss.left <= 0:
                boss_direction *= -1

            current_time = pygame.time.get_ticks()

            if current_time - last_boss_shot > boss_shoot_delay:
                shoot_boss_bullets(boss, player)
                last_boss_shot = current_time

            for bullet in bullets[:]:
                if boss.colliderect(bullet):
                    boss_health -= 1
                    bullets.remove(bullet)

                    if boss_health <= 0:
                        defeat_boss()

                    break

            if boss_active and boss and boss.colliderect(player):
                damage_player()

                boss.x = WIDTH // 2 - 100
                boss.y = 50

        # BONUSY
        for bonus in bonuses[:]:
            bonus["rect"].y += BONUS_SPEED

            if bonus["rect"].top > HEIGHT:
                bonuses.remove(bonus)
                continue

            if bonus["rect"].colliderect(player):
                collect_bonus(bonus)
                bonuses.remove(bonus)

        # RUCH POCISKOW PRZECIWNIKOW
        for bullet in enemy_bullets[:]:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]

            bullet_rect = pygame.Rect(
                int(bullet["x"] - bullet["size"]),
                int(bullet["y"] - bullet["size"]),
                bullet["size"] * 2,
                bullet["size"] * 2
            )

            if bullet_rect.colliderect(player):
                enemy_bullets.remove(bullet)
                damage_player()
                continue

            if (
                bullet["x"] < -30
                or bullet["x"] > WIDTH + 30
                or bullet["y"] < -30
                or bullet["y"] > HEIGHT + 30
            ):
                enemy_bullets.remove(bullet)

    # ZAPIS REKORDU
    if (game_over or campaign_complete) and not record_saved:
        records = save_record(player_name, score)
        record_saved = True

    # RYSOWANIE GRY
    draw_background()

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    for bullet in enemy_bullets:
        draw_enemy_bullet(bullet)

    if not boss_active:
        for enemy in enemies:
            draw_enemy(enemy)

    # RYSOWANIE BONUSOW
    for bonus in bonuses:
        draw_bonus(bonus)

    # BOSS I PASEK ZDROWIA
    if boss_active and boss:
        draw_boss(boss)

        boss_bar_width = 300
        boss_bar_x = WIDTH // 2 - boss_bar_width // 2

        pygame.draw.rect(screen, RED, (boss_bar_x, 15, boss_bar_width, 15))

        health_width = int(boss_bar_width * boss_health / boss_max_health)

        pygame.draw.rect(screen, GREEN, (boss_bar_x, 15, health_width, 15))

        boss_text = font.render("BOSS!", True, LIGHT_PURPLE)
        screen.blit(boss_text, boss_text.get_rect(center=(WIDTH // 2, 105)))

        boss_name_text = small_font.render(
            LEVELS[current_level - 1]["boss"],
            True,
            WHITE
        )

        screen.blit(
            boss_name_text,
            boss_name_text.get_rect(center=(WIDTH // 2, 130))
        )

    # EKSPLOZJE
    for explosion in explosions[:]:
        for particle in explosion[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["life"] -= 1

            if particle["life"] > 0:
                size = particle["size"]

                pixel_x = int(particle["x"] // 4) * 4
                pixel_y = int(particle["y"] // 4) * 4

                pygame.draw.rect(
                    screen,
                    particle["color"],
                    (pixel_x, pixel_y, size, size)
                )

            else:
                explosion.remove(particle)

        if len(explosion) == 0:
            explosions.remove(explosion)

    # STATEK GRACZA
    if not game_over and not campaign_complete:
        draw_player_shield()
        draw_player(player)

    # INFORMACJE O GRZE
    name_label = font.render(f"GRACZ: {player_name}", True, LIGHT_PURPLE)
    score_text = font.render(f"WYNIK: {score}", True, WHITE)

    screen.blit(name_label, (20, 20))
    screen.blit(score_text, (20, 55))

    # AKTUALNY POZIOM
    level_text = small_font.render(
        f"POZIOM {current_level}/5: {LEVELS[current_level - 1]['name']}",
        True,
        GOLD
    )

    screen.blit(level_text, level_text.get_rect(topright=(WIDTH - 20, 20)))

    # POSTEP DO BOSSA
    if not boss_active and not level_transition and not campaign_complete:
        progress_text = small_font.render(
            f"POKONANI WROGOWIE: {kills_in_level}/{KILLS_TO_BOSS}",
            True,
            CYAN
        )

        screen.blit(progress_text, progress_text.get_rect(topright=(WIDTH - 20, 50)))

    draw_hearts(lives)

    # AKTYWNE BONUSY
    current_time = pygame.time.get_ticks()

    if shield_active:
        shield_text = small_font.render("TARCZA AKTYWNA", True, CYAN)
        screen.blit(shield_text, (20, 95))

    if current_time < rapid_fire_until:
        remaining = (rapid_fire_until - current_time + 999) // 1000

        rapid_text = small_font.render(
            f"SZYBKIE STRZELANIE: {remaining}s",
            True,
            YELLOW
        )

        screen.blit(rapid_text, (20, 125))

    # GAME OVER
    if game_over:
        game_over_text = big_font.render("GAME OVER", True, RED)

        final_score = font.render(
            f"{player_name}: {score} punktow",
            True,
            WHITE
        )

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, 105)))
        screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, 165)))

        draw_leaderboard(records, 225)

        mouse_pos = pygame.mouse.get_pos()
        button_color = GREEN if restart_button.collidepoint(mouse_pos) else (0, 150, 70)

        pygame.draw.rect(screen, button_color, restart_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, restart_button, 3, border_radius=12)

        restart_text = font.render("ZAGRAJ PONOWNIE", True, WHITE)
        screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))

        keyboard_text = small_font.render(
            "LUB NACISNIJ R NA KLAWIATURZE",
            True,
            LIGHT_PURPLE
        )

        screen.blit(keyboard_text, keyboard_text.get_rect(center=(WIDTH // 2, 585)))

    # PRZEJSCIE NA KOLEJNY POZIOM
    if level_transition:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 210))
        screen.blit(overlay, (0, 0))

        defeated_text = big_font.render("BOSS POKONANY!", True, GOLD)
        screen.blit(defeated_text, defeated_text.get_rect(center=(WIDTH // 2, 250)))

        next_level_text = font.render(
            f"PRZYGOTUJ SIE NA: {LEVELS[current_level]['name']}",
            True,
            WHITE
        )

        screen.blit(
            next_level_text,
            next_level_text.get_rect(center=(WIDTH // 2, 330))
        )

        countdown = max(
            1,
            (level_transition_until - current_time + 999) // 1000
        )

        countdown_text = small_font.render(
            f"Nastepny poziom za {countdown}...",
            True,
            CYAN
        )

        screen.blit(
            countdown_text,
            countdown_text.get_rect(center=(WIDTH // 2, 390))
        )

    # UKONCZENIE KAMPANII
    if campaign_complete:
        victory_text = big_font.render("KAMPANIA UKONCZONA!", True, GOLD)

        screen.blit(
            victory_text,
            victory_text.get_rect(center=(WIDTH // 2, 100))
        )

        subtitle = font.render("URATOWALES GALAKTYKE!", True, LIGHT_PURPLE)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 165)))

        final_score = font.render(
            f"{player_name}: {score} punktow",
            True,
            WHITE
        )

        screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, 220)))

        draw_leaderboard(records, 285)

        mouse_pos = pygame.mouse.get_pos()
        button_color = GREEN if restart_button.collidepoint(mouse_pos) else (0, 150, 70)

        pygame.draw.rect(screen, button_color, restart_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, restart_button, 3, border_radius=12)

        restart_text = font.render("ZAGRAJ PONOWNIE", True, WHITE)
        screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))

        keyboard_text = small_font.render(
            "LUB NACISNIJ R NA KLAWIATURZE",
            True,
            LIGHT_PURPLE
        )

        screen.blit(keyboard_text, keyboard_text.get_rect(center=(WIDTH // 2, 585)))

    pygame.display.flip()

pygame.quit()
