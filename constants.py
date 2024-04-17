import pygame, random

pygame.init()

# GAME SETTINGS
WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h

FPS = 45
INIT_GAME_SPEED = 2


# BACKGROUND
BACKGROUND_IMAGES = [
        pygame.image.load("assets/images/backgrounds/1.jpg"),
        pygame.image.load("assets/images/backgrounds/2.jpg"),
        pygame.image.load("assets/images/backgrounds/3.jpg"),
        pygame.image.load("assets/images/backgrounds/4.jpg"),
        pygame.image.load("assets/images/backgrounds/5.jpg")
]

BACKGROUND_IMAGES = [
        pygame.transform.scale(BACKGROUND_IMAGES[0], (WIDTH, HEIGHT)),
        pygame.transform.scale(BACKGROUND_IMAGES[1], (WIDTH, HEIGHT)),
        pygame.transform.scale(BACKGROUND_IMAGES[2], (WIDTH, HEIGHT)),
        pygame.transform.scale(BACKGROUND_IMAGES[3], (WIDTH, HEIGHT)),
        pygame.transform.scale(BACKGROUND_IMAGES[4], (WIDTH, HEIGHT))
]

BACKGROUND_IMAGE = BACKGROUND_IMAGES[random.randint(0, 4)]


# QUESTIONS
QUESTIONS = [
    "Tuple is a data type",
    "Pygame is not a standart Python library"
]

RANDOM_QUESTION = QUESTIONS[random.randint(0, 1)]


# PLAYER
PLAYER_MOVE_1 = pygame.image.load("assets/images/player/move_1.png")
PLAYER_MOVE_1 = pygame.transform.scale(PLAYER_MOVE_1, (125, 125))

PLAYER_MOVE_2 = pygame.image.load("assets/images/player/move_2.png")
PLAYER_MOVE_2 = pygame.transform.scale(PLAYER_MOVE_2, (125, 125))

PLAYER_FLY = pygame.image.load("assets/images/player/fly.png")
PLAYER_FLY = pygame.transform.scale(PLAYER_FLY, (125, 125))

PLAYER_FLY_STOP = pygame.image.load("assets/images/player/fly_stop.png")
PLAYER_FLY_STOP = pygame.transform.scale(pygame.image.load("assets/images/player/fly_stop.png"), (125, 125))

PLAYER_DEATH = pygame.image.load("assets/images/player/death.png")
PLAYER_DEATH = pygame.transform.scale(PLAYER_DEATH, (125, 125))


# ROCKET
ROCKET_IMAGE = pygame.image.load("assets/images/rocket.png")
ROCKET_IMAGE = pygame.transform.scale(ROCKET_IMAGE, (130, 100))
ROCKET_IMAGE = pygame.transform.rotate(ROCKET_IMAGE, 90)

ROCKET_EXPLOSION_IMAGE = pygame.image.load("assets/images/explosion/2.png")
ROCKET_EXPLOSION_IMAGE = pygame.transform.scale(ROCKET_EXPLOSION_IMAGE, (250, 250))


# MAP
FLOOR_IMAGE = pygame.image.load("assets/images/floor.png")
FLOOR_IMAGE = pygame.transform.scale(FLOOR_IMAGE, (FLOOR_IMAGE.get_width(), 80))
ROOF_IMAGE = pygame.transform.flip(FLOOR_IMAGE, 0, 1)


# SOUNDS
SOUND_MUSIC = "assets/sounds/music.mp3"

SOUND_ROCKET_LAUNCH = "assets/sounds/rocket/launch.mp3"
SOUND_ROCKET_FLY = "assets/sounds/rocket/fly.mp3"
SOUND_ROCKET_EXPLOSION = "assets/sounds/rocket/explosion.wav"

SOUND_UI_QUIT = "assets/sounds/ui/quit.ogg"


# FONTS
FONT_LOGO = pygame.font.Font("assets/fonts/BlackHanSans-Regular.ttf", 65)
FONT_MAIN = pygame.font.Font("freesansbold.ttf", 22)
FONT_ROCKET_WARNING = pygame.font.Font("freesansbold.ttf", 35)