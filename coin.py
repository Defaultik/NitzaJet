import pygame
import constants as Constants

class Coin:
    def __init__(self, obj, player, x, y):
        self.obj = obj
        self.player = player

        self.image = pygame.transform.scale(Constants.COIN_IMAGE, (50, 50)).convert_alpha()  # Scale the coin image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collision detection

        self.rect.x = x
        self.rect.y = y


    def draw(self):
        self.obj.screen.blit(self.image, self.rect)


    def update(self):
        self.rect.x -= 15 + self.obj.game_speed

        if self.rect.colliderect(self.player.rect):
            self.obj.coins.remove(self)
            self.obj.question_menu.active = True