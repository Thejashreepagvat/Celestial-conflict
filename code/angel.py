import pygame
from os.path import join
from random import randint,uniform

score=0

class Player(pygame.sprite.Sprite):
    def __init__(self,surf,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=surf.get_frect(center=(window_width/2,window_height/2))
        self.direction=pygame.math.Vector2()
        self.speed=300

        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown=400

        self.mask=pygame.mask.from_surface(self.image)

    def holy_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time-self.holy_shoot_time>=self.cooldown:
                self.can_shoot=True


    def update(self,dt):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y=int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction=self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys=pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Holy_light(resized_holy,self.rect.midtop,(all_sprites,holy_sprites))
            self.can_shoot=False
            self.holy_shoot_time=pygame.time.get_ticks()

        self.holy_time()
             
       

class Cloud(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups) 
        self.image=surf
        self.rect=self.image.get_frect(center=(randint(0,window_width),randint(0,window_height)))

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(center=(randint(0,window_width),randint(0,window_height)))

class Holy_light(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)  
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)
       

    def update(self,dt):
        self.rect.centery -= 400*dt
        if self.rect.bottom<0:
            self.kill()

class Monster(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image=surf
        self.rect= self.image.get_frect(center=pos)
        self.start_time=pygame.time.get_ticks()
        self.lifetime=3000
        self.direction=pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed=randint(300,400)
        

    def update(self,dt):
        self.rect.center+=self.direction*self.speed*dt
        if pygame.time.get_ticks()-self.start_time>=self.lifetime:
            self.kill()
         
def collisions():
    global running,score 

    collision_sprites=pygame.sprite.spritecollide(player,monster_sprites,True,pygame.sprite.collide_mask)
    if collision_sprites:
        running=False

    for holy in holy_sprites:
        collided_sprites=pygame.sprite.spritecollide(holy,monster_sprites,True)
        for _ in collided_sprites:
            holy_sound.play()
            holy_sound.set_volume(0.4)
            score+=1
        if collided_sprites:
            holy.kill()

    
def draw_score():
        text_surf=font.render(f"SOULS FREED: {score}",True,"#91caff")
        display_surface.blit(text_surf,(10,10))
    



    
#GENERAL SETUP
pygame.init()
window_width=1280
window_height=720
display_surface=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Salvation")
running=True
clock=pygame.time.Clock()

#Creating 
all_sprites=pygame.sprite.Group()
monster_sprites=pygame.sprite.Group()
holy_sprites=pygame.sprite.Group()
font=pygame.font.Font(None,40)

#sound
holy_sound=pygame.mixer.Sound(join("sound","holy.mp3"))
game_music=pygame.mixer.Sound(join("sound","game_music2.mp3"))
game_music.set_volume(0.5)
game_music.play(loops=-1)


#star import and creating instance
star_surf=pygame.image.load(join("images","star_angel.png"))
star_resized=pygame.transform.scale(star_surf,(15,20)).convert_alpha()
for i in range(20):
    Star(all_sprites,star_resized)

#cloud import and creating instance
cloud_surf=pygame.image.load(join("images","angel_cloud.png"))
cloud_resized=pygame.transform.scale(cloud_surf,(145,35)).convert_alpha()
for i in range(20):
    Cloud(all_sprites,cloud_resized)

#dark_blast import
holy_surf=pygame.image.load(join("images","holy_light.png"))
resized_holy=pygame.transform.scale(holy_surf,(35,40)).convert_alpha()

#player import
player_surf= pygame.image.load(join("images","angel.png"))
player_resized=pygame.transform.scale(player_surf,(120,110)).convert_alpha()

#ghost import
monster_surf=pygame.image.load(join("images","angel_monster.png"))
monster_resized=pygame.transform.scale(monster_surf,(75,90)).convert_alpha()

#creating an instance of player
player=Player(player_resized,all_sprites)

#making custom event for interval timer
monster_event=pygame.event.custom_type()
pygame.time.set_timer(monster_event,500)

#actual game loop
while running:
    dt=clock.tick() / 1000
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False  
        if event.type == monster_event: 
            x,y=randint(0,window_width),randint(-200,-100)
            Monster(monster_resized,(x,y),(all_sprites,monster_sprites))   

    #update
    all_sprites.update(dt)

    collisions()
    
    #drawing or showing on surface
    display_surface.fill("aliceblue")
    all_sprites.draw(display_surface)

    draw_score()


   
    


    pygame.display.update()
    



pygame.quit()


