import constants as Constants


class Map:
    def __init__(self, screen):
        self.screen = screen


    def draw(self):
        self.screen.blit(Constants.BACKGROUND_IMAGE, (0, 0))

        for x in range(0, Constants.WIDTH, Constants.FLOOR_IMAGE.get_width()):
            self.roof = self.screen.blit(Constants.ROOF_IMAGE, (x, 0))
            self.floor = self.screen.blit(Constants.FLOOR_IMAGE, (x, Constants.HEIGHT / 1.1))