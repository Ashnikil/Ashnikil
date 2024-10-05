import pygame, random ,os


class Image(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        image.set_colorkey((255, 255, 255))
        self.image=image
        self.rect=self.image.get_rect(topleft=(x,y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.running = True
        self.clock = pygame.time.Clock()
        self.key_search=""
        self.save_name_search=""
        #self.images_group.sprites()[1].rect.x+=1
        self.images_group=pygame.sprite.Group()
        self.mousewhere=pygame.mouse.get_pos()
        self.old_mousewhere=pygame.mouse.get_pos()
        self.mousedown=False
        self.which_item=0
        self.shifty=False
        self.saving=False
        self.first_save=False
        self.first_box=False
        self.edge_click=False
        self.border_size=2
        pygame.font.init()
        self.namefont=pygame.font.SysFont(None,self.width//20)
        self.item_list=[]
        self.image_list=[]

    def savename(self):
        if self.saving==False:
            img=self.namefont.render(self.key_search,False,"blue")

        elif self.saving==True:
            img = self.namefont.render(f"saving as:{self.save_name_search}", False, "blue")
        self.screen.blit(img,img.get_rect(bottomleft=(0,self.height)))

    def dragdrop(self):
        self.mousewhere=pygame.mouse.get_pos()
        if self.mousedown:
            if self.edge_click:
                for b,i in enumerate(self.images_group):
                    if b==self.which_item:
                        try:
                            img = vars(self)[str(self.image_list[self.which_item])]
                            img = pygame.transform.scale(img, (pygame.mouse.get_pos()[0]-i.rect.x,pygame.mouse.get_pos()[1]-i.rect.y))
                            self.image_list.append(self.image_list[self.which_item])
                            self.image_list.pop(self.which_item)
                            self.item_list.append(list(img.get_size()))
                            self.item_list.pop(self.which_item)
                            i.kill()
                            self.images_group.add((Image(img,i.rect.x,i.rect.y)))
                        except:
                            pass

            else:
                x,y=map(lambda i, j: i - j, self.mousewhere,self.old_mousewhere)
                self.images_group.sprites()[self.which_item].rect.x += x
                self.images_group.sprites()[self.which_item].rect.y += y
                self.item_list[self.which_item][0]+=x
                self.item_list[self.which_item][1]+=y
        self.old_mousewhere=pygame.mouse.get_pos()


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type==pygame.KEYDOWN:




                    if self.shifty==True:
                        if pygame.key.name(event.key)=="s":
                            if self.saving==False:
                                self.shifty=False
                                self.first_save=True
                                self.save_name_search=""
                            elif self.saving==True:
                                self.sub=self.screen.subsurface(pygame.Rect(((self.width / 4)+1, (self.height / 4)+1, (self.width / 2)-2, (self.height / 2)-2)))
                                pygame.image.save(self.sub,f"images/{self.save_name_search}.png")
                                self.shifty=False
                                self.first_box=True


                        else:
                            self.shifty=False

                    if self.saving==True:
                        if pygame.key.name(event.key)=="ctrl":
                            self.shifty=True
                        elif pygame.key.name(event.key)=="backspace":
                            self.save_name_search=self.save_name_search[:len(self.save_name_search)-1]
                        elif pygame.key.name(event.key)=="escape":
                            self.first_box=True
                            self.save_name_search=""
                        elif pygame.key.name(event.key) == "return":
                            self.sub = self.screen.subsurface(pygame.Rect(((self.width / 4) + 1, (self.height / 4) + 1,(self.width / 2) - 2,(self.height / 2) - 2)))
                            pygame.image.save(self.sub, f"images/{self.save_name_search}.png")
                            self.shifty = False
                            self.first_box = True
                        elif len(pygame.key.name(event.key))!=1:
                            pass
                        else:
                            self.save_name_search=self.save_name_search+str(pygame.key.name(event.key))



                    elif self.saving==False:
                        if pygame.key.name(event.key)=="return":
                            if self.key_search=="clear" or self.key_search=="deletespaceall":
                                for i in self.images_group:
                                    i.kill()
                            self.key_search="_".join(self.key_search.split())
                            # try:
                            #     print(1/0)
                            #     img=exec('f"self.{self.key_search}_image"')
                            # except:
                            #     exec(f"self.{self.key_search}_image"'=pygame.image.load(f"images/{self.key_search}.png")')
                            #     img=(exec('f"self.{self.key_search}_image"'))
                            # exec('self.images_group.add(Image(img.convert_alpha(), 0, 0))')
                            # exec('self.item_list.append(list(img.get_size()))')
                            try:
                                img=vars(self)[str(self.key_search) + "_image"]
                                self.images_group.add(Image(img.convert_alpha(), 0, 0))
                                self.item_list.append(list(img.get_size()))
                                self.image_list.append(str(self.key_search) + "_image")
                            except:
                                try:
                                    exec("self." + str(self.key_search) + "_image=pygame.image.load('images/"+str(self.key_search)+".png')") #converting alpha later
                                    self.image_list.append(str(self.key_search)+ "_image")
                                    img = vars(self)[str(self.key_search) + "_image"]
                                    self.images_group.add(Image(img.convert_alpha(), 0, 0))
                                    self.item_list.append(list(img.get_size()))
                                except:
                                    pass


                            self.key_search=""
                        elif pygame.key.name(event.key)=="backspace":
                            self.key_search=self.key_search[:len(self.key_search)-1]
                        elif pygame.key.name(event.key)=="space":
                            self.key_search=self.key_search+" "
                        elif len(pygame.key.name(event.key))!=1:
                            pass
                        else:
                            self.key_search = self.key_search + str(pygame.key.name(event.key))



                    if self.first_save==True:
                        self.first_save=False
                        self.saving=True
                    if self.first_box==True:
                        self.first_box=False
                        self.saving=False
                        self.key_search = ""













                if event.type==pygame.MOUSEBUTTONDOWN:
                    for b,i in enumerate(self.images_group):
                        if i.rect.collidepoint(self.mousewhere):
                            self.mousedown=True

                            if self.mousewhere[0]<=i.rect.x+self.border_size or self.mousewhere[0]>=((i.rect.x+self.item_list[b][0])-self.border_size) or (self.mousewhere[1]<=i.rect.y+self.border_size) or (self.mousewhere[1]>=(i.rect.y+self.item_list[b][1])-self.border_size):
                                self.edge_click=True


                            self.which_item=b
                elif event.type==pygame.MOUSEBUTTONUP:
                    self.mousedown=False
                    self.edge_click=False












            self.clock.tick(60)  # 60 fps
            self.screen.fill("white")
            pygame.draw.rect(self.screen,"black",(self.width/4,self.height/4,self.width/2,self.height/2))
            pygame.draw.rect(self.screen, "white", ((self.width / 4)+1, (self.height / 4)+1, (self.width / 2)-2, (self.height / 2)-2))
            self.dragdrop()
            self.images_group.draw(self.screen)
            if pygame.key.get_mods() == 64:
                self.shifty=True
            else:
                self.shifty=False
            self.savename()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
