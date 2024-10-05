import pygame, random

class Colour(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect(topleft=(x,y))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.running = True
        self.clock = pygame.time.Clock()
        self.board_group=pygame.sprite.Group()
        self.colour_list=["blue","brown","dark_green","gold","light_green","pink","purple","red"]
        for i in self.colour_list:
            exec('self.'+i+'_image=pygame.image.load("'+i+'.png")')
        self.tile_amount=[10,10]
        self.board()


    def board(self):
        # self.colour_image=pygame.transform.scale(self.blue_image, (self.width // self.tile_amount[0], self.height // self.tile_amount[1]))
        for a in range(self.tile_amount[0]):
            for b in range(self.tile_amount[1]):
                exec('self.colour_image = pygame.transform.scale(self.'+self.colour_list[(a+b)%(len(self.colour_list)-1)]+'_image, (self.width / self.tile_amount[0], self.height / self.tile_amount[1]))')
                self.board_group.add(Colour(self.colour_image,a*self.colour_image.get_size()[0],b*self.colour_image.get_size()[1]))


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(60)  # 60 fps
            self.screen.fill("white")
            self.board_group.draw(self.screen)
            if pygame.mouse.get_pressed()[0]==True:
                for i in self.board_group:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        i.kill()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
