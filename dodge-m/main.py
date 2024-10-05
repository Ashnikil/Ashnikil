import pygame, random , math

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 10

class Dodge(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed=5
        self.direction=[random.choice([-1,1])*self.speed,random.choice([-1,1])*self.speed]
        #self.count=10 #maybe max num of dodges?



class Images(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.running = True
        pygame.font.init()
        self.phase=[self.main,self.game,self.score,self.shop]
        self.fonts()
        self.images()
        self.groups()
        self.start_time=0
        self.phase_on=0
        self.speed=5
        self.health=10
        self.score=0
        self.money=0
        self.max_health=10
        self.clock = pygame.time.Clock()


    def fonts(self):
        self.fps_on_screen_font = pygame.font.SysFont(None, int(self.width / 60))
        self.health_font = pygame.font.SysFont(None,int(self.width/30))
        self.score_font = pygame.font.SysFont(None,int(self.width/30))
        self.shop_font = pygame.font.SysFont(None, int(self.width / 30))
        self.shop_item_font = pygame.font.SysFont(None, int(self.width / 30))

    def images(self):
        self.mc_image=pygame.image.load("mc.png")
        self.mc_image=pygame.transform.scale(self.mc_image,(self.width/19.2,self.height/10.8))

        self.dodgem_image=pygame.image.load("dodgem_image.png")
        self.dodgem_image=pygame.transform.scale(self.dodgem_image,(self.width/1.236714975845410628019323671,self.height/3.1034482758620689655172))

        self.background_image = pygame.image.load("background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.play_image = pygame.image.load("play_image.png")
        self.play_image = pygame.transform.scale(self.play_image, (self.width / (3*3.84), self.height / (3*2.16)))

        self.dodge_me_image = pygame.image.load("dodge_me_image.png")
        self.dodge_me_image = pygame.transform.scale(self.dodge_me_image, (self.width/19.2,self.height/10.8))

        self.shop_image = pygame.image.load("shop_image.png")
        self.shop_image = pygame.transform.scale(self.shop_image, (self.width / (3 * 3.84), self.height / (3 * 2.16)))

        self.exit_image = pygame.image.load("exit_image.png")
        self.exit_image = pygame.transform.scale(self.exit_image, (self.width / (3 * 3.84), self.height / (3 * 2.16)))

    def groups(self):
        self.cursor_sprite = pygame.sprite.Sprite()
        self.cursor_sprite.image = pygame.Surface([1, 1])
        self.cursor_sprite.rect = self.cursor_sprite.image.get_rect(topleft=(pygame.mouse.get_pos()))

        self.player_group = pygame.sprite.Group()
        self.player_group.add(Player(self.mc_image, self.width / 2, self.height / 2))

        self.start_group=pygame.sprite.Group()
        self.start_group.add(Images(self.play_image, self.width / 2, self.height / 2))
        self.start_group.add(Images(self.shop_image, self.width / 2, (self.height / 2)+self.play_image.get_size()[1]))
        self.start_group.add(Images(self.exit_image, self.width / 2, (self.height / 2)+(2*self.play_image.get_size()[1])))

        self.dodge_group=pygame.sprite.Group()
        self.dodge_group.add(Dodge(self.dodge_me_image,0,0))

        self.background_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.shop_item_surface = pygame.Surface((self.width, self.height/7.2), pygame.SRCALPHA)

        self.shop_item_surface.fill("black")

        shop_text_image = self.shop_item_font.render("increase health",True,"gold")
        self.shop_item_surface.blit(shop_text_image,shop_text_image.get_rect(midleft=(0,self.shop_item_surface.get_size()[1]/2)))

        shop_text_image2 = self.shop_item_font.render("cost: 10 money",True,"gold")
        self.shop_item_surface.blit(shop_text_image2,shop_text_image2.get_rect(midright=(self.width,self.shop_item_surface.get_size()[1]/2)))
        pygame.draw.line(self.shop_item_surface,"gold",(self.width/2,0),(self.width/2,self.shop_item_surface.get_size()[1]),width=1)



    def add_new_dodge(self):
        # self.dodge_group.add(Dodge(self.dodge_me_image, random.randint(0,self.width-self.dodge_me_image.get_size()[0]), random.randint(0,self.height-self.dodge_me_image.get_size()[1])))

        if random.randint(1,2)==1:
            self.dodge_group.add(Dodge(self.dodge_me_image,random.choice([0,self.width]),random.randint(0,self.height-self.dodge_me_image.get_size()[1])))
        else:
            self.dodge_group.add(Dodge(self.dodge_me_image, random.randint(0,self.width-self.dodge_me_image.get_size()[0]),random.choice([0,self.height])))





    def dodge_move(self):
        for i in self.dodge_group:
            i.rect.x+=i.direction[0]
            i.rect.y+=i.direction[1]
            if i.rect.x>=(self.width-i.image.get_size()[0]):
                i.rect.x=(self.width-i.image.get_size()[0])
                # i.direction[0]=-i.speed
                i.direction[0]=-random.randint(1,i.speed-1)
                # i.direction[1]=((random.choice([-1,1]))*(math.sqrt((i.speed**2)-(i.direction[0]**2))))
                i.direction[1]=((i.direction[1]/abs(i.direction[1]))*(math.sqrt((i.speed**2)-(i.direction[0]**2))))
            elif i.rect.x<=0:
                i.rect.x=0
                # i.direction[0]=i.speed
                i.direction[0]=random.randint(1,i.speed-1)
                # i.direction[1]=((random.choice([-1,1]))*(math.sqrt((i.speed**2)-(i.direction[0]**2))))
                i.direction[1]=((i.direction[1]/abs(i.direction[1]))*(math.sqrt((i.speed**2)-(i.direction[0]**2))))
            if i.rect.y>=(self.height-i.image.get_size()[1]):
                i.rect.y=(self.height-i.image.get_size()[1])
                # i.direction[1]=-i.speed
                i.direction[1]=-random.randint(1,i.speed-1)
                # i.direction[0]=((random.choice([-1,1]))*(math.sqrt((i.speed**2)-(i.direction[1]**2))))
                i.direction[0]=((i.direction[0]/abs(i.direction[0]))*(math.sqrt((i.speed**2)-(i.direction[1]**2))))
            if i.rect.y<=0:
                i.rect.y=0
                # i.direction[1]=i.speed
                i.direction[1]=random.randint(1,i.speed-1)
                # i.direction[0]=((random.choice([-1,1]))*(math.sqrt((i.speed**2)-(i.direction[1]**2))))
                i.direction[0]=((i.direction[0]/abs(i.direction[0]))*(math.sqrt((i.speed**2)-(i.direction[1]**2))))


    def game(self):
        self.screen.fill("black")
        self.movement()
        self.dodge_move()
        self.player_group.draw(self.screen)
        self.dodge_group.draw(self.screen)


        if (self.pygame_time-self.start_time)>=1000:
            self.start_time=self.pygame_time
            self.add_new_dodge()

        for i in self.dodge_group:
            if i.rect.collideobjects(self.player_group.sprites()):
                i.kill()
                self.health-=1

        health_image = self.health_font.render(f"{self.health}/{self.max_health}", True, "gold")
        self.screen.blit(health_image, health_image.get_rect(topleft=(0,0)))
        if self.health<=0:
            self.died()


    def score(self):
        score_image = self.score_font.render(f"{self.score}", True, "gold")
        self.screen.blit(score_image, score_image.get_rect(center=(self.width/2,self.height/2)))
        click_to_restart = self.score_font.render(f"click anywhere to restart", True, "gold")
        self.screen.blit(click_to_restart, click_to_restart.get_rect(center=(self.width / 2, (self.height / 2)+score_image.get_size()[1])))

    def died(self):
        self.background_surface.fill((155,155,155,155))
        self.screen.blit(self.background_surface,(0,0))
        self.phase_on=2
        self.health=self.max_health
        self.score=len(self.dodge_group)+1
        self.money+=self.score
        for i in self.dodge_group:
            i.kill()
        for i in self.player_group:
            i.kill()
        self.player_group.add(Player(self.mc_image, self.width / 2, self.height / 2))



    def movement(self):
        keys=pygame.key.get_pressed()
        #make speed vector...fied? idk dude , #fixthis
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (((keys[pygame.K_s] or keys[pygame.K_DOWN])==False)):
            for i in self.player_group:
                i.rect.y-=self.speed
                if i.rect.y<=0:
                    i.rect.y=0
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and ((keys[pygame.K_w] or keys[pygame.K_UP]) == False):
            for i in self.player_group:
                i.rect.y+=self.speed
                if i.rect.y>=self.height-i.image.get_size()[1]:
                    i.rect.y=self.height-i.image.get_size()[1]
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) == False):
            for i in self.player_group:
                i.rect.x-=self.speed
                if i.rect.x<=0:
                    i.rect.x=0
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and ((keys[pygame.K_a] or keys[pygame.K_LEFT]) == False):
            for i in self.player_group:
                i.rect.x+=self.speed
                if i.rect.x>=self.width-i.image.get_size()[0]:
                    i.rect.x=self.width-i.image.get_size()[0]


    def shop(self):
        self.screen.fill("blue")
        money_image=self.shop_font.render(f"money: {self.money}",True,"gold")
        self.screen.blit(money_image,money_image.get_rect(topleft=(0,0)))
        self.screen.blit(self.shop_item_surface,(0,self.height/10.8))






    def main(self):
        self.screen.blit(self.background_image,(0,0))
        self.screen.blit(self.dodgem_image,((self.width-self.dodgem_image.get_size()[0])/2,0))
        self.start_group.draw(self.screen)

    def run(self):
        while self.running:
            self.clock.tick(60)  # 60 fps
            self.pygame_time=pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor_sprite.rect = self.cursor_sprite.image.get_rect(topleft=(pygame.mouse.get_pos()))
                    if event.button==1:
                        if self.phase_on==0:
                            if pygame.sprite.spritecollide(self.cursor_sprite,self.start_group,False):
                                for i,j in enumerate(self.start_group):
                                    if j.rect.colliderect(self.cursor_sprite):
                                        if i==0:
                                            self.phase_on=1
                                            self.health=self.max_health
                                            self.start_time=self.pygame_time
                                        elif i==1:
                                            self.phase_on=3
                                        elif i==2:
                                            self.running=False
                        elif self.phase_on==2:
                            self.phase_on=0
                        elif self.phase_on==3:
                            if pygame.rect.Rect(self.shop_item_surface.get_rect(topleft=(0, self.height / 10.8))).collidepoint(pygame.mouse.get_pos()):
                                if self.money>=10:
                                    self.max_health+=10
                                    self.money-=10
                elif event.type == pygame.KEYDOWN:
                    if self.phase_on==3:
                        if event.key==pygame.K_ESCAPE:
                            self.phase_on=0
            self.phase[self.phase_on]()
            fps_img_test = self.fps_on_screen_font.render(f"{self.clock.get_fps():.2f}", True, "gold")
            self.screen.blit(fps_img_test, fps_img_test.get_rect(bottomright=(self.width, self.height)))
            pygame.display.update()



if __name__ == "__main__":
    game = Game()
    game.run()
