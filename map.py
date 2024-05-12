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
        coins_text = Constants.FONT_MAIN.render(f"Coins: {self.obj.collected_coins}", True, (255, 255, 255))
        self.screen.blit(coins_text, (10, 10))

        distance_text = Constants.FONT_MAIN.render(f"Distance: {self.obj.distance}", True, (255, 255, 255))
        self.screen.blit(distance_text, (10, 50))

        best_distance_text = Constants.FONT_MAIN.render(f"Best Distance: {self.obj.best_distance}", True, (255, 255, 255))
        self.screen.blit(best_distance_text, (10, 90))