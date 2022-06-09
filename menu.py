class Menu(object):
    def __init__(self, config):
        self.leftIndent = config['screen_width']/4 - 100
        self.topIndent = config['screen_height']/4 - 100
    
    def render(self, screen, game_font):
        game_font.render_to(screen, (self.leftIndent, self.topIndent), "Menu", (255, 255, 255))
        game_font.render_to(screen, (self.leftIndent, self.topIndent + 50), "Instructions", (255, 255, 255))
        game_font.render_to(screen, (self.leftIndent + 50, self.topIndent + 100), "Press 'enter' to start!", (255, 255, 255))
        game_font.render_to(screen, (self.leftIndent + 50, self.topIndent + 150), "arrows keys to move", (255, 255, 255))
        game_font.render_to(screen, (self.leftIndent + 50, self.topIndent + 200), "capture 80 percent of the total area to win", (255, 255, 255))
        game_font.render_to(screen, (self.leftIndent + 50, self.topIndent + 250), "Game over if you lose 3 lives", (255, 255, 255))
