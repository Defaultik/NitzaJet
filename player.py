import pygame
import constants as Constants

class Player:
    def __init__(self, game):
        self.game = game

        self.motion_counter = 0

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Constants.PLAYER_MOVE_1.convert_alpha()
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)

        self.sprite.rect.x = 350
        self.sprite.rect.y = Constants.HEIGHT / 1.1 - Constants.FLOOR_IMAGE.get_height()
        self.y_velocity = 0

        self.jet_force = -15
        self.gravity = 2


    def draw(self):
        if not self.game.game_over_menu.active:
            if not self.game.pause_menu.active:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.y_velocity = self.jet_force
                else:
                    self.y_velocity += self.gravity
                
                self.sprite.rect.y += self.y_velocity

                if self.sprite.rect.y < (53):  # roof
                    self.sprite.rect.y = 53
                    self.y_velocity = 0
                    
                elif self.sprite.rect.y > (Constants.HEIGHT / 1.1 - Constants.FLOOR_IMAGE.get_height()):  # floor
                    self.sprite.rect.y = Constants.HEIGHT / 1.1 - Constants.FLOOR_IMAGE.get_height()
                    self.y_velocity = 0

                if self.sprite.rect.y < (Constants.HEIGHT / 1.1 - 81):
                    self.on_ground = False
                else:
                    self.on_ground = True

                if pygame.key.get_pressed()[pygame.K_SPACE] and not self.on_ground:
                    self.sprite.image = Constants.PLAYER_FLY.convert_alpha()
                elif not self.on_ground:
                    self.sprite.image = Constants.PLAYER_FLY_STOP.convert_alpha()
                elif self.on_ground:
                    if self.motion_counter < 10:
                        self.motion_counter += 1
                    else:
                        self.motion_counter = 0

                    if self.motion_counter < 5:
                        self.sprite.image = Constants.PLAYER_MOVE_1.convert_alpha()
                    else:
                        self.sprite.image = Constants.PLAYER_MOVE_2.convert_alpha()
        else:
            self.sprite.image = Constants.PLAYER_DEATH.convert_alpha()
        
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.game.screen.blit(self.sprite.image, self.sprite.rect)