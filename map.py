import constants as Constants


class Map:
    def __init__(self, obj):
        self.obj = obj
        self.screen = self.obj.screen


    def draw(self):
        self.screen.blit(Constants.BACKGROUND_IMAGE, (0, 0))

        for x in range(0, Constants.WIDTH, Constants.FLOOR_IMAGE.get_width()):
            self.roof = self.screen.blit(Constants.ROOF_IMAGE, (x, 0))
            self.floor = self.screen.blit(Constants.FLOOR_IMAGE, (x, Constants.HEIGHT - Constants.FLOOR_IMAGE.get_height()))

        # Display distance and collected coins in the top-left corner
        coin_image = self.screen.blit(Constants.COIN_IMAGE, (10, 10))
        coins_text = Constants.FONT_MAIN.render(str(self.obj.collected_coins), True, (255, 255, 255))
        coins_text_pos = self.screen.blit(coins_text, (coin_image.x + 45, coin_image.y * 2))

        distance_text = Constants.FONT_MAIN.render(str(self.obj.distance) + "m", True, (255, 255, 255))
        distance_text_pos = self.screen.blit(distance_text, (Constants.WIDTH / 2.1, 15))