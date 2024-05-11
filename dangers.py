import pygame
import random
import constants as Constants


class Danger:
    def __init__(self, obj):
        self.obj = obj
        self.player = self.obj.player


class Rocket(Danger):
    def __init__(self, obj):
        super().__init__(obj)

        self.warning = True
        self.warning_counter = 0

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Constants.ROCKET_IMAGE.convert_alpha()

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = Constants.WIDTH - 60
        self.sprite.rect.y =  Constants.HEIGHT / 2

        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)


    def draw(self):
        for rocket in self.obj.rockets:
            if self.warning:
                self.draw_warning()
            else:
                self.draw_rocket(rocket)

                if pygame.Rect.colliderect(self.sprite.rect, self.player.sprite.rect):
                    self.obj.game_over_menu.active = True
                    self.sprite.image = Constants.ROCKET_EXPLOSION_IMAGE
                    self.sprite.rect = self.player.sprite.rect


    def draw_warning(self):
        rocket_warning = pygame.draw.rect(self.obj.screen, "crimson", [self.sprite.rect.x, self.sprite.rect.y, 50, 50], 0, 5)
        text_surface = Constants.FONT_ROCKET_WARNING.render("!", True, "white")
        text_rect = text_surface.get_rect(center=rocket_warning.center)
        self.obj.screen.blit(text_surface, text_rect)

        if (not self.obj.pause_menu.active) and (not self.obj.game_over_menu.active) and (not self.obj.main_menu.active) and (not self.obj.question_menu.active):
            if self.sprite.rect.y > self.player.sprite.rect.y:
                self.sprite.rect.y -= 6
            else:
                self.sprite.rect.y += 6

            self.warning_counter += 1
            if self.warning_counter >= 45:
                self.warning_counter = 0
                self.warning = False


    def draw_rocket(self, rocket):
        self.obj.screen.blit(self.sprite.image, self.sprite.rect)

        if (not self.obj.pause_menu.active) and (not self.obj.game_over_menu.active) and (not self.obj.main_menu.active) and (not self.obj.question_menu.active):
            self.sprite.rect.x -= 15 + self.obj.game_speed

        if self.sprite.rect.x <= (0 - self.sprite.mask.get_size()[0]):
            self.obj.rockets.remove(rocket)
            del rocket


class Laser(Danger):
    def __init__(self, obj):
        super().__init__(obj)


    def draw(self):
        for laser in self.obj.lasers:
            laser_rect = pygame.Rect(laser["x"], laser["y"], 15, laser["size"] + 30)
            pygame.draw.line(self.obj.screen, "yellow", (laser["x"], laser["y"]), (laser["x"], laser["y"] + laser["size"]), 12)
            pygame.draw.circle(self.obj.screen, "yellow", (laser["x"], laser["y"] + laser["size"]), 15)
            pygame.draw.circle(self.obj.screen, "yellow", (laser["x"], laser["y"]), 15)

            if (not self.obj.pause_menu.active) and (not self.obj.game_over_menu.active) and (not self.obj.main_menu.active) and (not self.obj.question_menu.active):
                laser["x"] -= 7 + self.obj.game_speed

            if pygame.Rect.colliderect(laser_rect, self.player.sprite.rect):
                self.obj.game_over_menu.active = True
                
            if laser["x"] <= 0:
                self.obj.lasers.remove(laser)
                del laser