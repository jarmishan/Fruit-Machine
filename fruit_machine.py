import random
import sys

import pygame

pygame.init()
HEIGHT, WIDTH = 800, 800 

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

slot = pygame.transform.scale(pygame.image.load("Fruit machine/assets/slot.png"), (60, 770)).convert_alpha()
slots_spinning = pygame.transform.scale(pygame.image.load("Fruit machine/assets/slots.png"), (192, 128)).convert_alpha()
slot_machine = pygame.transform.scale(pygame.image.load("Fruit machine/assets/slot_machine.png"), (272, 458)).convert_alpha()
coin = pygame.image.load("Fruit machine/assets/coin.png").convert_alpha()
bg = pygame.image.load("Fruit machine/assets/tempbg.png").convert_alpha()

fruits = {
    "cherry": pygame.image.load("Fruit machine/fruits/cherry.png").convert_alpha(),
    "grape": pygame.image.load("Fruit machine/fruits/grape.png").convert_alpha(),
    "lemon": pygame.image.load("Fruit machine/fruits/lemon.png").convert_alpha(),
    "melon": pygame.image.load("Fruit machine/fruits/melon.png").convert_alpha()
}

jackpot = pygame.mixer.Sound("Fruit machine/music/jackpot_payout.wav")
win = pygame.mixer.Sound("Fruit machine/music/win_payout.wav")
spinning = pygame.mixer.Sound("Fruit machine/music/spinning.wav")

fruit_coords = {
    -143: "cherry",
    -216: "grape",
    0: "lemon",
    -72: "melon",
}



class Coin:
    def __init__(self, x_vel, y_vel):
        self.x = 450
        self.y = 550
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.dist = 0

    
class Machine:
    def __init__(self):
        self.spinning = True
        self.fruit = random.choices(list(fruit_coords), k=3)
        self.coins = [Coin(0, 5)]
        self.spins = 0          

    def play_animation_win(self, jackpot):
        if jackpot:
            self.coins.append(Coin(round(random.uniform(-4, 4), 1), random.randint(7, 15)))
      
        screen.blit(bg,  (0, 0))
        screen.blit(slot_machine, (263, 171))

        for coin in self.coins:
            coin.dist += coin.y_vel
            coin.x += coin.x_vel
            coin.y += coin.y_vel

            if coin.dist > random.randint(300, 400):
                self.coins.remove(coin)

            screen.blit(pygame.image.load("Fruit machine/assets/coin.png").convert_alpha(), (coin.x, coin.y))

            screen.blit(fruits[self.f1], (306, 308))
            screen.blit(fruits[self.f2], (369, 308))
            screen.blit(fruits[self.f3], (434, 308))
        pygame.display.flip()
 
    def play_animation_spin(self):
        self.fruit1_y, self.fruit2_y, self.fruit3_y =  self.fruit[0], self.fruit[1], self.fruit[2]
        for _ in range(75):
            screen.blit(slots_spinning, (303, 308))
            
            self.fruit1_y += 5
            self.fruit2_y += 4
            self.fruit3_y += 3

            screen.blit(slot, (305, self.fruit1_y))
            screen.blit(slot, (370, self.fruit2_y))
            screen.blit(slot, (435, self.fruit3_y))

            screen.blit(bg,  (0, 0))
            screen.blit(slot_machine, (263, 171))
            pygame.display.flip()

    def check_win(self, f1, f2, f3):
        if f1 == f2 == f3:
            return "jackpot"
        elif f1 == f2 or f2 == f3 or f1 == f3:
            return "win"
        else:
            return "loss"

    def playsound(self):  
        if self.win_type == "jackpot":
            jackpot.play()
        elif self.win_type == "win":
            win.play()
    
    def reward(self):
        if self.win_type == "jackpot":
            self.play_animation_win(True)

        elif self.win_type == "win":
            self.play_animation_win(False)
    
    def spin(self):
        if self.spinning:
            if self.spins == 0:
                spinning.play()
            self.spins += 1
            self.play_animation_spin()
                      
        if self.spins > 20:
            spinning.stop()
            self.f1, self.f2, self.f3 = fruit_coords[self.fruit[0]], fruit_coords[self.fruit[1]], fruit_coords[self.fruit[2]]
            self.spinning = False
            self.spins = 0

        if not self.spinning:
            screen.blit(slots_spinning, (303, 308))
            screen.blit(fruits[self.f1], (306, 308))
            screen.blit(fruits[self.f2], (369, 308))
            screen.blit(fruits[self.f3], (434, 308))
            self.win_type = self.check_win(self.f1, self.f2, self.f3)
            self.reward()
            self.playsound()
        
    def update(self):
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed(5)[0]:
            jackpot.stop()
            win.stop()
            self.__init__()   
        self.spin()

machine = Machine()

while True:
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    machine.update()
    pygame.display.flip()
    clock.tick(60)