import pygame
import random
import constants as Constants


class Danger:
    def __init__(self, obj, player):
        self.obj = obj
        self.player = player


class Rocket(Danger):
    def __init__(self, obj, player):
        super().__init__(obj, player)

        self.warning_counter = 0

        self.spawn_time = 0
        self.spawn_interval = random.randint(60, 300)

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Constants.ROCKET_IMAGE.convert_alpha()
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)

 
    def draw(self):
        for rocket in self.obj.rockets:
            if rocket["warning"]:
                self.draw_warning(rocket)
            else:
                self.draw_rocket(rocket)

                if pygame.Rect.colliderect(self.sprite.rect, self.player.sprite.rect):
                    self.obj.game_over_menu.active = True

                if self.sprite.rect.x <= 0:
                    self.obj.rockets.remove(rocket)
                    del rocket


    def draw_warning(self, rocket):
        rocket_warning = pygame.draw.rect(self.obj.screen, "crimson", [rocket["x"], rocket["y"], 50, 50], 0, 5)
        text_surface = Constants.FONT_ROCKET_WARNING.render("!", True, "white")
        text_rect = text_surface.get_rect(center=rocket_warning.center)
        self.obj.screen.blit(text_surface, text_rect)

        if not self.obj.pause_menu.active:
            if rocket["y"] > self.player.sprite.rect.y:
                rocket["y"] -= 6
            else:
                rocket["y"] += 6

            self.warning_counter += 1
            if self.warning_counter >= 45:
                self.warning_counter = 0
                rocket["warning"] = False


    def draw_rocket(self, rocket):
        self.sprite.rect.x = rocket["x"]
        self.sprite.rect.y = rocket["y"]

        self.obj.screen.blit(self.sprite.image, self.sprite.rect)

        if not self.obj.pause_menu.active:
            rocket["x"] -= 15 + self.obj.game_speed


class Laser(Danger):
    def __init__(self, obj, player):
        super().__init__(obj, player)

        self.spawn_time = 0
        self.spawn_interval = random.randint(60, 300)


    def draw(self):
        for laser in self.obj.lasers:
            laser_rect = pygame.Rect(laser["x"], laser["y"], 15, laser["size"] + 30)
            pygame.draw.line(self.obj.screen, "yellow", (laser["x"], laser["y"]), (laser["x"], laser["y"] + laser["size"]), 12)
            pygame.draw.circle(self.obj.screen, "yellow", (laser["x"], laser["y"] + laser["size"]), 15)
            pygame.draw.circle(self.obj.screen, "yellow", (laser["x"], laser["y"]), 15)

            if not self.obj.pause_menu.active:
                laser["x"] -= 7 + self.obj.game_speed

            if pygame.Rect.colliderect(laser_rect, self.player.sprite.rect):
                self.obj.game_over_menu.active = True
                
            if laser["x"] <= 0:
                self.obj.lasers.remove(laser)
                del laser