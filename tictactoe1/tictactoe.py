import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, count, x, y):
        super().__init__()
        if not count:
            self.image = pygame.image.load("blue.png")
        else:
            self.image = pygame.image.load("white.png")
        self.rect = self.image.get_rect(topleft=(x, y))


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((300, 300))
        self.width, self.height = pygame.display.get_surface().get_size()
        self.running = True
        self.clock = pygame.time.Clock()
        self.box_group = pygame.sprite.Group()
        self.counter = 0
        self.array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.temp=False

    def collision(self, x, y):
        if self.counter % 2 == 0:
            self.image = pygame.image.load("cross.png")
        else:
            self.image = pygame.image.load("circle.png")
        self.counter += 1
        self.screen.blit(self.image, (x, y))

    def screenput(self):
        for a in range(3):
            for b in range(3):
                count = (a + b) % 2
                x = (a * 100)
                y = (b * 100)
                self.box_group.add(Box(count, x, y))

    def mouseput(self):
        lclick, mclick, rclick = pygame.mouse.get_pressed()
        mousepos = pygame.mouse.get_pos()
        if lclick:
            self.temp=True
        if lclick==False and self.temp==True:
            if self.box_group:
                for i in self.box_group:
                    if i.rect.collidepoint(*mousepos):
                        self.temp=False
                        x = i.rect.x
                        y = i.rect.y
                        self.collision(x, y)
                        a = ((x / 100) * 3) + (y / 100)
                        if self.counter % 2 == 0:
                            self.array[int(a)] = 1
                        else:
                            self.array[int(a)] = 2
                        i.kill()

    def checkwin(self):
        if (self.array[0] == 1 and self.array[1] == 1 and self.array[2] == 1) or (
                self.array[3] == 1 and self.array[4] == 1 and self.array[5] == 1) or (
                self.array[6] == 1 and self.array[7] == 1 and self.array[8] == 1) or (
                self.array[0] == 1 and self.array[3] == 1 and self.array[6] == 1) or (
                self.array[1] == 1 and self.array[4] == 1 and self.array[7] == 1) or (
                self.array[2] == 1 and self.array[5] == 1 and self.array[8] == 1) or (
                self.array[0] == 1 and self.array[4] == 1 and self.array[8] == 1) or (
                self.array[2] == 1 and self.array[4] == 1 and self.array[6] == 1):
            print("circle win")
            self.array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in self.box_group:
                i.kill()
            self.screenput()

        if (self.array[0] == 2 and self.array[1] == 2 and self.array[2] == 2) or (
                self.array[3] == 2 and self.array[4] == 2 and self.array[5] == 2) or (
                self.array[6] == 2 and self.array[7] == 2 and self.array[8] == 2) or (
                self.array[0] == 2 and self.array[3] == 2 and self.array[6] == 2) or (
                self.array[1] == 2 and self.array[4] == 2 and self.array[7] == 2) or (
                self.array[2] == 2 and self.array[5] == 2 and self.array[8] == 2) or (
                self.array[0] == 2 and self.array[4] == 2 and self.array[8] == 2) or (
                self.array[2] == 2 and self.array[4] == 2 and self.array[6] == 2):
            print("cross win")
            self.array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in self.box_group:
                i.kill()
            self.screenput()
        if 0 not in self.array:
            print("draw")
            self.array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in self.box_group:
                i.kill()
            self.screenput()

    def start(self):
        self.image = pygame.image.load("1p2p.png")
        self.screen.blit(self.image, (0, 0))
        pygame.display.update()

    def ai(self):
        if self.counter == 1:
            pygame.mouse.set_pos(250, 250)
            if self.box_group:
                for i in self.box_group:
                    if i.rect.collidepoint(250, 250):
                        self.collision(i.rect.x, i.rect.y)
                        i.kill()
    def run(self):
        # self.start()
        self.screenput()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.box_group.draw(self.screen)
            self.clock.tick(60)  # 60 fps
            self.mouseput()
            self.checkwin()
            pygame.display.update()




if __name__ == "__main__":
    game = Game()
    game.run()



















