import pygame, random
import constants as Constants


class Coin:
    def __init__(self, obj):
        self.obj = obj
        self.player = self.obj.player

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Constants.COIN_IMAGE.convert_alpha() 

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = Constants.WIDTH
        self.sprite.rect.y = random.randint(80, Constants.HEIGHT - 80)

        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)  # Create a mask for collision detection


    def draw(self):
        for coin in self.obj.coins:
            self.obj.screen.blit(self.sprite.image, self.sprite.rect)

            self.sprite.rect.x -= 15 + self.obj.game_speed

            if pygame.Rect.colliderect(self.sprite.rect, self.player.sprite.rect):
                self.obj.coins.remove(coin)
                self.obj.question_menu.active = True

            if self.sprite.rect.x <= (0 - self.sprite.mask.get_size()[0]):
                self.obj.coins.remove(coin)
                del rocket