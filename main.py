import pygame, io
from PIL import Image, ImageFilter
import random


def main():
    pygame.init()
    Game().run()


class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("NitzaJet")

        self.fonts_init()
        self.images_init()

        # MAIN
        self.fps = 60
        self.game_speed = 2

        # PLAYER
        self.player_counter = 0
        self.player_x = 280

        self.player_init_y = self.HEIGHT / 1.22
        self.player_y = self.player_init_y
        self.player_y_velocity = 0

        self.player_gravity = 2
        self.player_jet_force = -15

        self.player_on_ground = True


        # ROCKET
        self.rockets = []  # List to store rockets
        self.rocket_spawn_time = 0
        self.rocket_spawn_interval = random.randint(60, 300)  # Time until first rocket appears
        self.rocket_warning_counter = 0 

        # LASER
        self.lasers = []
        self.laser_spawn_time = 0
        self.laser_spawn_interval = random.randint(60, 300)  # Time until first laser appears

        # STATEMENTS
        self.main_menu = True
        self.pause_menu = False
        self.restart = False
        self.game_over = False


    def fonts_init(self):
        self.font_logo = pygame.font.Font("assets/fonts/BlackHanSans-Regular.ttf", 65)
        self.font_main = pygame.font.Font("freesansbold.ttf", 22)
        self.font_rocket_warning = pygame.font.Font("freesansbold.ttf", 35)


    def images_init(self):
        self.bg_image = "assets/images/backgrounds/1.jpg"

        self.game_image = pygame.image.load(self.bg_image)
        self.game_image = pygame.transform.scale(self.game_image, (self.WIDTH, self.HEIGHT))

        # Blur background image
        byte_stream = io.BytesIO()
        self.pause_image = Image.open(self.bg_image)
        self.pause_image = self.pause_image.resize((self.WIDTH, self.HEIGHT))
        self.pause_image = self.pause_image.filter(ImageFilter.GaussianBlur(7))
        self.pause_image.save(byte_stream, format="JPEG")
        byte_stream.seek(0)
        self.pause_image = pygame.image.load(byte_stream)

        # Load floor and roof images
        self.floor_image = pygame.image.load("assets/images/floor.png")
        self.floor_image = pygame.transform.scale(self.floor_image, (self.floor_image.get_size()[0], 80))
        self.roof_image = pygame.transform.flip(self.floor_image, 0, 1)

        self.player_image_move_1 = pygame.image.load("assets/images/player/move_1.png")
        self.player_image_move_1 = pygame.transform.scale(self.player_image_move_1, (125, 125))

        self.player_image_move_2 = pygame.image.load("assets/images/player/move_2.png")
        self.player_image_move_2 = pygame.transform.scale(self.player_image_move_2, (125, 125))

        self.player_image_fly = pygame.image.load("assets/images/player/fly.png")
        self.player_image_fly = pygame.transform.scale(self.player_image_fly, (125, 125))

        self.player_image_fly_stop = pygame.image.load("assets/images/player/fly_stop.png")
        self.player_image_fly_stop = pygame.transform.scale(self.player_image_fly_stop, (125, 125))

        self.player_image_death = pygame.image.load("assets/images/player/death.png")
        self.player_image_death = pygame.transform.scale(self.player_image_fly_stop, (125, 125))

        self.rocket_image = pygame.image.load("assets/images/rocket.png")
        self.rocket_image = pygame.transform.scale(self.rocket_image, (130, 100))
        self.rocket_image = pygame.transform.rotate(self.rocket_image, 90)

    
    # LASER BARRIER
    def draw_laser(self):
        for laser in self.lasers:
            pygame.draw.line(self.screen, "yellow", (laser["x"], laser["y"]), (laser["x"], laser["y"] + laser["size"]), 12)
            pygame.draw.circle(self.screen, "yellow", (laser["x"], laser["y"] + laser["size"]), 15)
            pygame.draw.circle(self.screen, "yellow", (laser["x"], laser["y"]), 15)

            laser["x"] -= 7 + self.game_speed

            # Check collision with player
            if laser["x"] < self.player_x + self.player_image_move_1.get_width() and \
                    laser["x"] + self.rocket_image.get_width() > self.player_x and \
                    laser["y"] < self.player_y + self.player_image_move_1.get_height() and \
                    laser["y"] + self.rocket_image.get_height() > self.player_y:
                
                self.game_over = True
                
            if laser["x"] <= 0:
                self.lasers.remove(laser)
                del laser


    # ROCKET (Aleksey)
    # Method to generate rocket warning
    def draw_rocket(self):
        for rocket in self.rockets:
            if rocket["warning"]:
                rocket_warning = pygame.draw.rect(self.screen, "crimson", [rocket["x"], rocket["y"], 50, 50], 0, 5)
                text_surface = self.font_rocket_warning.render("!", True, "white")
                text_rect = text_surface.get_rect(center=rocket_warning.center)
                self.screen.blit(text_surface, text_rect)

                if rocket["y"] > self.player_y:
                    rocket["y"] -= 5
                else:
                    rocket["y"] += 5

                self.rocket_warning_counter += 1
                if self.rocket_warning_counter >= 60:
                    self.rocket_warning_counter = 0
                    rocket["warning"] = False
            else:
                rocket_warning = self.screen.blit(self.rocket_image, (rocket["x"], rocket["y"]))
                rocket["x"] -= 20 + self.game_speed

            # Check collision with player
            if rocket["x"] < self.player_x + self.player_image_move_1.get_width() and \
                    rocket["x"] + self.rocket_image.get_width() > self.player_x and \
                    rocket["y"] < self.player_y + self.player_image_move_1.get_height() and \
                    rocket["y"] + self.rocket_image.get_height() > self.player_y:
                
                self.game_over = True

            if rocket["x"] <= 0:
                self.rockets.remove(rocket)
                del rocket


    # PLAYER
    def draw_player(self):
        if not self.game_over:
            if self.player_counter < 10:
                self.player_counter += 1
            else:
                self.player_counter = 0

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.player_y_velocity = self.player_jet_force
            else:
                self.player_y_velocity += self.player_gravity

            # Update player"s y position
            self.player_y += self.player_y_velocity

            # Ensure player stays within screen boundaries
            if self.player_y < 54:  # roof
                self.player_y = 54
                self.player_y_velocity = 0
            elif self.player_y > self.floor_surf.y - 80:  # floor
                self.player_y = self.floor_surf.y - 80
                self.player_y_velocity = 0

            # Check if player is on the ground
            if self.player_y < self.floor_surf.y - 80:
                self.on_ground = False
            else:
                self.on_ground = True

            if pygame.key.get_pressed()[pygame.K_SPACE] and not self.on_ground:
                player = self.screen.blit(self.player_image_fly, (self.player_x, self.player_y))
            elif not self.on_ground:
                player = self.screen.blit(self.player_image_fly_stop, (self.player_x, self.player_y))
            elif self.on_ground:
                if self.player_counter < 5:
                    player = self.screen.blit(self.player_image_move_1, (self.player_x, self.player_y))
                else:
                    player = self.screen.blit(self.player_image_move_2, (self.player_x, self.player_y))
        else:
            player = self.screen.blit(self.player_image_death, (self.player_x, self.player_y))

        return player


    # GAME
    # Method to draw game map
    def draw_map(self):
        self.screen.blit(self.game_image, (0, 0))

        # Draw roof and floor
        for x in range(0, self.WIDTH, self.roof_image.get_size()[0]):
            self.roof_surf = self.screen.blit(self.roof_image, (x, 0))
            self.floor_surf = self.screen.blit(self.floor_image, (x, self.HEIGHT / 1.1))


    # Method to draw main menu
    def draw_main_menu(self):
        # Draw main menu interface
        self.screen.blit(self.pause_image, (0, 0))
        pygame.draw.rect(self.surface, (10, 10, 10, 120), [0, 0, self.WIDTH, self.HEIGHT])

        # Render and position text and buttons
        text_surface = self.font_logo.render("NITZAJET", True, "white")
        text_rect = text_surface.get_rect(center=(self.WIDTH / 2.05, self.HEIGHT / 3))
        self.surface.blit(text_surface, text_rect)

        start_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, text_rect.y + 80, 270, 45], 0, 100)
        text_surface = self.font_main.render("Play", True, "black")
        text_rect = text_surface.get_rect(center=start_btn.center)
        self.surface.blit(text_surface, text_rect)

        quit_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, start_btn.y + 60, 270, 45], 0, 100)
        text_surface = self.font_main.render("Quit", True, "black")
        text_rect = text_surface.get_rect(center=quit_btn.center)
        self.surface.blit(text_surface, text_rect)

        self.screen.blit(self.surface, (0, 0))

        return start_btn, quit_btn


    # Method to draw pause menu
    def draw_pause_menu(self):
        # Draw pause menu interface
        self.screen.blit(self.pause_image, (0, 0))
        pygame.draw.rect(self.surface, (10, 10, 10, 120), [0, 0, self.WIDTH, self.HEIGHT])

        text_surface = self.font_logo.render("Pause Menu", True, "white")
        text_rect = text_surface.get_rect(center=(self.WIDTH / 2.05, self.HEIGHT / 3))
        self.surface.blit(text_surface, text_rect)

        play_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, text_rect.y + 80, 270, 45], 0, 100)
        text_surface = self.font_main.render("Play", True, "black")
        text_rect = text_surface.get_rect(center=play_btn.center)
        self.surface.blit(text_surface, text_rect)

        restart_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, play_btn.y + 60, 270, 45], 0, 100)
        text_surface = self.font_main.render("Restart", True, "black")
        text_rect = text_surface.get_rect(center=restart_btn.center)
        self.surface.blit(text_surface, text_rect)

        quit_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, restart_btn.y + 60, 270, 45], 0, 100)
        text_surface = self.font_main.render("Quit", True, "black")
        text_rect = text_surface.get_rect(center=quit_btn.center)
        self.surface.blit(text_surface, text_rect)

        self.screen.blit(self.surface, (0, 0))

        return play_btn, restart_btn, quit_btn
    

    # Method to draw restart menu
    def draw_game_over_menu(self):
        # Draw main menu interface
        pygame.draw.rect(self.surface, (10, 10, 10, 200), [0, 0, self.WIDTH, self.HEIGHT])

        # Render and position text and buttons
        text_surface = self.font_logo.render("Game Over", True, "white")
        text_rect = text_surface.get_rect(center=(self.WIDTH / 2.05, self.HEIGHT / 3))
        self.surface.blit(text_surface, text_rect)

        restart_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, text_rect.y + 80, 270, 45], 0, 100)
        text_surface = self.font_main.render("Restart", True, "black")
        text_rect = text_surface.get_rect(center=restart_btn.center)
        self.surface.blit(text_surface, text_rect)

        quit_btn = pygame.draw.rect(self.surface, "white", [self.WIDTH / 2.5, restart_btn.y + 60, 270, 45], 0, 100)
        text_surface = self.font_main.render("Quit", True, "black")
        text_rect = text_surface.get_rect(center=quit_btn.center)
        self.surface.blit(text_surface, text_rect)

        self.screen.blit(self.surface, (0, 0))

        return restart_btn, quit_btn
    

    def run(self):
        quit = False
        clock = pygame.time.Clock()

        while not quit:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.game_over and not self.main_menu:
                        if self.pause_menu:
                            self.pause_menu = False
                        else:
                            self.pause_menu = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu:
                        if btn_start.collidepoint(event.pos):
                            self.main_menu = False
                        elif btn_quit.collidepoint(event.pos):
                            quit = True

                    elif self.pause_menu:
                        if btn_play.collidepoint(event.pos):
                            self.pause_menu = False
                        elif btn_restart.collidepoint(event.pos):
                            self.pause_menu = False
                            self.restart = True
                        elif btn_quit.collidepoint(event.pos):
                            quit = True

                    elif self.game_over:
                        if btn_restart.collidepoint(event.pos):
                            self.restart = True
                        elif btn_quit.collidepoint(event.pos):
                            quit = True

            if not self.game_over:
                if self.rocket_spawn_time >= self.rocket_spawn_interval:
                    self.rockets.append({"x": self.WIDTH - 60, "y": self.HEIGHT / 2, "warning": True})
                    self.rocket_spawn_time = 0
                    self.rocket_spawn_interval = random.randint(60, 300)  # Generate new time
                else:
                    self.rocket_spawn_time += 1

                if self.laser_spawn_time >= self.laser_spawn_interval:
                    self.lasers.append({"x": self.WIDTH, "y": random.randint(80, self.HEIGHT - 80), "size": random.randint(90, 120)})
                    self.laser_spawn_time = 0
                    self.laser_spawn_interval = random.randint(160, 550)  # Generate new time
                else:
                    self.laser_spawn_time += 1

            if self.restart:
                self.restart = False
                self.game_over = False
                self.game_speed = 2

                self.player_y = self.player_init_y

                self.rockets.clear()
                self.lasers.clear()

            if self.main_menu:
                btn_start, btn_quit = self.draw_main_menu()

            elif self.pause_menu:
                self.draw_map()
                self.draw_rocket()
                self.draw_player()
                self.draw_laser()

                btn_play, btn_restart, btn_quit = self.draw_pause_menu()

            elif self.game_over:
                self.draw_map()
                self.draw_rocket()
                self.draw_player()
                self.draw_laser()

                btn_restart, btn_quit = self.draw_game_over_menu()

            else:
                self.draw_map()
                self.draw_rocket()
                self.player = self.draw_player()
                self.draw_laser()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    main()

