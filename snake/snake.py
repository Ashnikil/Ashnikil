import pygame, random,math

class Apple(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        self.image=pygame.image.load("apple.png") #146 130
        self.imagex,self.imagey=width / (8.76712*3), height /(5.538*3)
        self.image = pygame.transform.scale(self.image, (self.imagex,self.imagey))
        self.rect=self.image.get_rect(topleft=(random.randint(0,(width-int(self.imagex))),random.randint(0,(height-int(self.imagey)))))


class Box2(pygame.sprite.Sprite):
    def __init__(self,x,y,rot,width,height):
        super().__init__()
        self.image=pygame.image.load("snake_body.png")
        self.image=pygame.transform.scale(self.image,(width/25.6,height/14.4))
        self.image=pygame.transform.rotate(self.image,rot)
        self.wherex,self.wherey=x,y
        self.rect=self.image.get_rect(topleft=(self.wherex,self.wherey))



class Box(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__()
        self.image=pygame.image.load("snake_head.png").convert_alpha()
        self.imagex,self.imagey=width/18.8235,height/10.588
        self.image=pygame.transform.scale(self.image,(self.imagex,self.imagey))
        self.image=pygame.transform.rotate(self.image,180)
        self.wherex,self.wherey=x,y
        self.rect=self.image.get_rect(topleft=(self.wherex,self.wherey))
        self.image_og = self.image.copy()
        self.angle = 0

    def turn(self):
        self.image=pygame.transform.rotate(self.image_og,self.angle)
        self.rect = self.image.get_rect(center=(self.wherex,self.wherey))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.running = True
        self.clock = pygame.time.Clock()
        self.location=[]
        self.tick=0
        self.box_group2=pygame.sprite.Group()
        for i in range(2):
            self.box_group2.add(Box2(-100,-100,0,self.width,self.height))
        self.lag=10
        self.move_xy = 5
        self.turn_rate = 5
        self.max_apples=1
        self.apples_on_screen=self.max_apples
        self.apple_group=pygame.sprite.Group()
        for i in range(self.apples_on_screen):
            self.apple=Apple(self.width,self.height)
            self.apple_group.add(self.apple)
        self.directionfacing="down"
        self.dead=False

        try:
            with open("note.txt","r") as f:
                x=str(f.read().splitlines()[0])
                self.wherebox=(x[:x.index(",")],x[x.index(",")+1:])
                self.box = Box(int(self.wherebox[0]),int(self.wherebox[1]),self.width,self.height)

        except:
            f=open("note.txt","w")
            f.write("100,100")
            f.close()
            self.box=Box(100,100,self.width,self.height)
            self.wherebox = 100, 100
        self.box_group=pygame.sprite.Group()
        self.box_group.add(self.box)

    def turning(self):
        self.keys=pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.box.angle+=self.turn_rate
            self.box.turn()
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.box.angle-=self.turn_rate
            self.box.turn()
        self.box.wherex+=(self.move_xy*(math.sin((self.box.angle%360)*math.pi/180)))
        self.box.wherey+=(self.move_xy * (math.cos((self.box.angle % 360) * math.pi / 180)))
        self.box.turn()

    def locate(self):
        if self.box_group:
            for i in self.box_group:
                self.location.append((i.rect.x,i.rect.y))
        if self.box_group2:
            for a,b in enumerate(self.box_group2):
                if self.tick>=(a+1)*self.lag:
                        b.rect.x = self.location[self.tick-(self.lag*(a+1))][0]
                        b.rect.y=self.location[self.tick-(self.lag*(a+1))][1]

    def appleput(self):
        if self.apples_on_screen < self.max_apples:
            self.apple_group.add(Apple(self.width,self.height))
            self.apples_on_screen+=1
            if self.directionfacing=="down":
                self.box_group2.add(Box2(-100,-100,0,self.width,self.height))
            elif self.directionfacing=="right":
                self.box_group2.add(Box2(-100, -100, 90,self.width,self.height))
            elif self.directionfacing=="up":
                self.box_group2.add(Box2(-100, -100, 180,self.width,self.height))
            elif self.directionfacing=="left":
                self.box_group2.add(Box2(-100, -100, 270,self.width,self.height))

    def rotg2(self):
        if (self.box.angle%360>0 and self.box.angle%360<45) or (self.box.angle>(360-45) and self.box.angle<360):
            if self.directionfacing!="down":
                if self.box_group2:
                    for i in self.box_group2:
                        self.box_group2.add(Box2(i.rect.x,i.rect.y,0,self.width,self.height))
                        i.kill()
            self.directionfacing = "down"
        elif (self.box.angle%360>45 and self.box.angle%360<(90+45)):
            if self.directionfacing!="right":
                if self.box_group2:
                    for i in self.box_group2:
                        self.box_group2.add(Box2(i.rect.x,i.rect.y,90,self.width,self.height))
                        i.kill()
            self.directionfacing = "right"
        elif (self.box.angle%360>(90+45) and self.box.angle%360<(180+45)):
            if self.directionfacing!="up":
                if self.box_group2:
                    for i in self.box_group2:
                        self.box_group2.add(Box2(i.rect.x,i.rect.y,180,self.width,self.height))
                        i.kill()
            self.directionfacing = "up"
        elif (self.box.angle%360>(180+45) and self.box.angle%360<(270+45)):
            if self.directionfacing!="left":
                if self.box_group2:
                    for i in self.box_group2:
                        self.box_group2.add(Box2(i.rect.x,i.rect.y,270,self.width,self.height))
                        i.kill()
            self.directionfacing = "left"

    def applecol(self):
        if self.apple_group:
            if self.box_group:
                for a in self.apple_group:
                    for b in self.box_group:
                        if a.rect.colliderect(b):
                            a.kill()
                            self.apples_on_screen-=1


    def gameover(self):
        if self.box_group:
            for i in self.box_group:
                i.kill()
        if self.box_group2:
            for i in self.box_group:
                i.kill()
        if self.apple_group:
            for i in self.box_group:
                i.kill()
        self.dead=True



    def overlapbad(self):
        if self.box_group:
            if self.box_group2:
                for a in self.box_group:
                    for c, b in enumerate(self.box_group2):
                        if c != 0 and c != 1 and c!=2 and c!=3:
                            if a.rect.colliderect(b):
                                self.gameover()
    def dont_leave_screen(self):
        if self.box_group:
            for i in self.box_group:
                if i.rect.x<=0 or i.rect.x>=(self.width-self.box.imagex):
                    self.gameover()
                if i.rect.y<=0 or i.rect.y>=(self.height-self.box.imagey):
                    self.gameover()
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(60)  # 60 fps
            self.screen.fill("white")
            if self.dead==False:
                self.locate()
                self.tick+=1
                self.apple_group.draw(self.screen)
                self.box_group2.draw(self.screen)
                self.box_group.draw(self.screen)
                self.turning()
                self.appleput()
                self.rotg2()
                self.applecol()
                self.overlapbad()
                self.dont_leave_screen()
            else:
                self.running=False
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
