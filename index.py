import pygame as pg
from pygame.locals import (K_LEFT, K_RIGHT, K_SPACE)
import math as m
import random

# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 500
VINDU_HOYDE = 700
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

font = pg.font.SysFont("Arial", 24) # Med pygame så henter jeg font for å kunne skrive tekst i spillet

pg.display.set_caption("Øving til prøve")


class Ball:
    def __init__(self, x, y, radius, farge, vinduobjekt, fart):
        self.x = x
        self.y = y
        self.radius = radius
        self.farge = farge
        self.vinduobjekt = vinduobjekt
        self.fart = fart

    def tegn(self):
        pg.draw.circle(self.vinduobjekt, self.farge, (self.x, self.y), self.radius)


class Hinder(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, fart):
        super().__init__(x, y, radius, farge, vindusobjekt, fart)
        self.hp = 100
        self.move_counter = 0
        self.move_threshold = 400  # Ved å gjøre dette tallet større øker man mellomrommet for Hinder til å velge ny retning

    def flytt(self):
        # Sjekker om hinderet er utenfor høyre/venstre kant
        if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vinduobjekt.get_width()):
            self.fart = -self.fart

        # Flytter hinderet
        self.x += self.fart

        self.move_counter += 1

        if self.move_counter >= self.move_threshold: # For hver "frame" blir move_counter plusset med 1, så move_counter vil nærme seg nermere move_thresholden. Når den blir lik så kan Hinder endre retning igjen, men det er tilfeldig.
            self.move_counter = 0
            tall = random.randint(0, 100)
            if tall <= 50:
                self.fart = abs(self.fart)
            else:
                self.fart = -abs(self.fart)

    def slutt(self):
        self.fart = 0 # Stopper hinder fra å bevege seg
        self.farge = (0, 255, 46)




class Spiller(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, fart):
        super().__init__(x, y, radius, farge, vindusobjekt, fart)
        self.pellets = []  # Det kommer til å være mange pellets i spillet på en gang, så ved å putte det i en liste, så kan jeg fjerne og legge til lettere
        self.shoot_pressed = False  # Denne variabelen blir brukt slik at brukeren ikke kan holde inne knappen
        self.pellet_max = 30
        self.pellet_counter = 0

        self.pellet_skrift = (255,255,255)

    def flytt(self, taster):
        if taster[K_LEFT]:
            self.x -= self.fart
        if taster[K_RIGHT]:
            self.x += self.fart

        if taster[K_SPACE] and not self.shoot_pressed:  # Hvis space er trukket inn og shoot_pressed ikke er True
            self.shoot_pressed = True
            self.shoot() # Funksjon osm lager en pellet variabel og legger det til i en pellet liste
        elif not taster[K_SPACE]: # Hvis brukeren ikke trykker inn, så gir den brukeren muligheten til å skyte
            self.shoot_pressed = False

    def shoot(self):
        tall = random.randint(0,100)
        if (self.pellet_max - self.pellet_counter) == 0:
            self.pellet_skrift = (255,0,0)
        else:
            if tall > 0 and tall < 10:
                pellet = Pellet(self.x, self.y, 10, (255, 255, 0 ), vindu, 0.5, True)
                self.pellets.append(pellet)
                self.pellet_counter += 1
                self.radius -= 0.5
            else:
                pellet = Pellet(self.x, self.y, 5, (255, 255, 255), vindu, 0.5, False)
                self.pellets.append(pellet)
                self.pellet_counter += 1
                self.radius -= 0.5


    def update_pellets(self): # Denne funksjonen går igjennom alle pelletsa som er på skjermen og oppdaterer dem alle sammen. Metoden blir kjørt i hoved loop.
        for pellet in self.pellets: # Går igjennom alle pelletsa som er i skjermen nå, beveger, tegner og skjekker om er utenfor y = 0
            pellet.move()
            pellet.draw()
            if pellet.y <= 0:  # skjekker om pelleten treffer toppen av skjermen
                self.pellets.remove(pellet)
                print("Pellet borte")


class Pellet(Ball):
    def __init__(self, x, y, radius, farge, vinduobjekt, fart, dobbel):
        super().__init__(x, y, radius, farge, vinduobjekt, fart)
        self.dobbel = dobbel

    def move(self):
        self.y -= self.fart  # Pelleten skal bare oppover

    def draw(self):
        pg.draw.circle(self.vinduobjekt, self.farge, (self.x, self.y), self.radius)

    def avstand(self, annenBall):
        """Metode for å finne avstanden til en annen ball"""
        xAvstand2 = (self.x - annenBall.x) ** 2  # x-avstand i andre
        yAvstand2 = (self.y - annenBall.y) ** 2  # y-avstand i andre

        sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

        radiuser = self.radius + annenBall.radius

        avstand = sentrumsavstand - radiuser

        return avstand





hinder = Hinder(100, 100, 50, (255, 40, 50), vindu, 0.23)
spiller = Spiller(250, 600, 20, (200, 0, 100), vindu, 0.146)

# Gjenta helt til brukeren lukker vinduet
fortsett = True
dood = False
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    # Henter en ordbok med status for alle tastatur-taster
    trykkede_taster = pg.key.get_pressed()

    # Farger bakgrunnen lyseblå
    vindu.fill((135, 206, 235))

    spiller.tegn()
    spiller.flytt(trykkede_taster)
    spiller.update_pellets() # Skjekker og oppdaterer pelletsa på skjermen (Siden pelletsa blir dannet innenfor spiller klassen, så skal den ikke blir definert som spiller og hindring.)

    for pellet in spiller.pellets: # Går igjennom alle pellets i spillet akkurat nå
        if pellet.avstand(hinder) < 20 and hinder.hp != 0: # hvis de pelleten som blir skjekket nå har en avstand på mindre enn 20 (og hvis hindring ikke allerede er dø):
            if pellet.dobbel == False: # Egen variabel som hvis er sann gir dobbel skade til Hinder (hvis du treffer)
                spiller.pellets.remove(pellet)
                hinder.hp -= 5
                print(hinder.hp)
            else:
                spiller.pellets.remove(pellet)
                hinder.hp -= 10
                print(hinder.hp)


    hinder.tegn()
    hinder.flytt()

    if hinder.hp <= 0 and dood == False:
        print("kundi")
        hinder.slutt()
        dood = True

    hindring_hp = font.render(f"HP: {str(hinder.hp)}", True, (15, 15, 15))
    antall_pellets = font.render(f"{str((spiller.pellet_max - spiller.pellet_counter))}", True, spiller.pellet_skrift) #spiller.pellet_skrift vil endre farge når spiller er tom for skudd

    vindu.blit(hindring_hp, (0,0))
    vindu.blit(antall_pellets, (spiller.x-11, spiller.y-12))

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()
