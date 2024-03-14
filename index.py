import pygame as pg
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
import math as m
import random
import time

# Initialiserer/starter pygame
pg.init()

clock = pg.time.Clock()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 500
VINDU_HOYDE = 700
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

font = pg.font.SysFont("Arial", 24) # Med pygame så henter jeg font for å kunne skrive tekst i spillet

pg.display.set_caption("Space Invaders")

class Ball:
    def __init__(self, x, y, radius, farge, vinduobjekt, fart):
        self.x = x
        self.y = y
        self.radius = radius
        self.farge = farge
        self.vinduobjekt = vinduobjekt
        self.fart = fart
        self.dood = False

    def tegn(self):
        pg.draw.circle(self.vinduobjekt, self.farge, (self.x, self.y), self.radius)

class Hinder(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, fart, sprite):
        super().__init__(x, y, radius, farge, vindusobjekt, fart)
        self.hp = 10
        self.move_counter = 0
        self.move_threshold = 400 # Ved å gjøre dette tallet større øker man mellomrommet for Hinder til å velge ny retning
        self.sakteFart = 0.01
        if random.randint(0,100) <= 20: # Hvis det tilfeldige tallet er mindre enn tallet så... (20% sjanse)
            self.ekstraSkudd = True # Ekstra skudd blir gitt til spilleren
        else:
            self.ekstraSkudd = False # Spilleren får ikke ekstra skudd
        
        self.sprite = sprite

    def flytt(self):
        # Sjekker om hinderet er utenfor høyre/venstre kant
        if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vinduobjekt.get_width()):
            self.fart = -self.fart

        # Flytter hinderet
        self.x += self.fart
        self.y += self.sakteFart

        self.move_counter += 1

        if self.move_counter >= self.move_threshold: # For hver "frame" blir move_counter plusset med 1, så move_counter vil nærme seg nermere move_thresholden. Når den blir lik så kan Hinder endre retning igjen, men det er tilfeldig.
            self.move_counter = 0
            tall = random.randint(0, 100)
            if tall <= 50:
                self.fart = abs(self.fart)
            else:
                self.fart = -abs(self.fart)

    def slutt(self):
        self.fart = 0 # Stopper hinder fra å bevege seg side til side
        self.sakteFart = 0 # Stopper hinder fra å bevege seg ned mot spilleren
        self.farge = (0, 255, 46) # Gjør hinderet grønn
        if self.hp < 0:
            self.hp = 0

    def avstand(self, annenBall):
        xAvstand2 = (self.x - annenBall.x) ** 2 # x-avstand i andre
        yAvstand2 = (self.y - annenBall.y) ** 2 # y-avstand i andre

        sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

        radiuser = self.radius + annenBall.radius

        avstand = sentrumsavstand - radiuser

        return avstand

    def tegn(self): # For å tegne bilde isteden for ball
        self.vinduobjekt.blit(self.sprite, (self.x - self.radius, self.y - self.radius))


class Boss(Ball): # Egen klasse for BOSS i spillet
    def __init__(self, x, y, radius, farge, vindusobjekt, fart):
        super().__init__(x, y, radius, farge, vindusobjekt, fart)
        self.hp = 200 * ((level/10)/2) # Mer hp enn de vanlige hinderene (øker for hvert level)
        self.move_counter = 0
        self.move_threshold = 400 # Ved å gjøre dette tallet større øker man mellomrommet for Hinder til å velge ny retning
        self.sakteFart = 0.01
        if random.randint(0,100) <= 50: # Hvis det tilfeldige tallet er mindre enn tallet så... (50% sjanse)
            self.ekstraSkudd = True # Ekstra skudd blir gitt til spilleren
        else:
            self.ekstraSkudd = False # Spilleren får ikke ekstra skudd
    def flytt(self):
        # Sjekker om hinderet er utenfor høyre/venstre kant
        if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vinduobjekt.get_width()):
            self.fart = -self.fart

        # Flytter hinderet
        self.x += self.fart
        self.y += self.sakteFart

        self.move_counter += 1

        if self.move_counter >= self.move_threshold: # For hver "frame" blir move_counter plusset med 1, så move_counter vil nærme seg nermere move_thresholden. Når den blir lik så kan Hinder endre retning igjen, men det er tilfeldig.
            self.move_counter = 0
            tall = random.randint(0, 100)
            if tall <= 50:
                self.fart = abs(self.fart)
            else:
                self.fart = -abs(self.fart)

    def slutt(self):
        self.fart = 0 # Stopper hinder fra å bevege seg side til side
        self.sakteFart = 0 # Stopper hinder fra å bevege seg ned mot spilleren
        self.farge = (0, 255, 46) # Gjør hinderet grønn
        if self.hp < 0:
            self.hp = 0

    def avstand(self, annenBall):
        xAvstand2 = (self.x - annenBall.x) ** 2 # x-avstand i andre
        yAvstand2 = (self.y - annenBall.y) ** 2 # y-avstand i andre

        sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

        radiuser = self.radius + annenBall.radius

        avstand = sentrumsavstand - radiuser

        return avstand
    
    def tegn(self):
        pg.draw.circle(self.vinduobjekt, self.farge, (self.x, self.y), self.radius)
        boss_hp = font.render(f"{str(self.hp)}", True, (0,0,0))

        vindu.blit(boss_hp, (hinder.x - 15, hinder.y - 12))





class Spiller(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, fart):
        super().__init__(x, y, radius, farge, vindusobjekt, fart)
        self.pellets = [] # Det kommer til å være mange pellets i spillet på en gang, så ved å putte det i en liste, så kan jeg fjerne og legge til lettere
        self.shoot_pressed = False # Denne variabelen blir brukt slik at brukeren ikke kan holde inne knappen
        self.pellet_max = 100
        self.pellet_counter = 0
        self.pellet_skrift = (255, 255, 255)

    # Bevegelse
    def flytt(self, taster):
        if taster[K_LEFT]:
            if self.x <= 0: # Skjekker om spiller er på venstre side av skjermen, hvis sant: ikke gå videre den veien
                self.x = self.x
            else:
                self.x -= self.fart
        if taster[K_RIGHT]:
            if self.x >= VINDU_BREDDE:
                self.x = self.x
            else:
                self.x += self.fart
        # Tregere enn å gå side til side
        if taster[K_UP]: 
            if self.y <= 0:
                self.y = self.y
            else:
                self.y -= self.fart / 1.3
        if taster[K_DOWN]:
            if self.y >= VINDU_HOYDE:
                self.y = self.y
            else:
                self.y += self.fart / 1.3

        if taster[K_SPACE] and not self.shoot_pressed: # Hvis space er trukket inn og shoot_pressed ikke er True
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
            else:
                pellet = Pellet(self.x, self.y, 5, (255, 255, 255), vindu, 0.5, False)
                self.pellets.append(pellet)
                self.pellet_counter += 1

    def update_pellets(self): # Denne funksjonen går igjennom alle pelletsa som er på skjermen og oppdaterer dem alle sammen. Metoden blir kjørt i hoved loop.
        for pellet in self.pellets: # Går igjennom alle pelletsa som er i skjermen nå, beveger, tegner og skjekker om er utenfor y = 0
            pellet.move()
            pellet.draw()
            if pellet.y <= 0: # skjekker om pelleten treffer toppen av skjermen
                self.pellets.remove(pellet)
                print("Pellet borte")
    
    def tegn(self): # For å tegne bilde isteden for ball
        self.vinduobjekt.blit(spiller_sprite, (self.x-self.radius-10, self.y - self.radius)) #trengte -10 for at det skulle være mer eksakt


class Pellet(Ball):
    def __init__(self, x, y, radius, farge, vinduobjekt, fart, dobbel):
        super().__init__(x, y, radius, farge, vinduobjekt, fart)
        self.dobbel = dobbel

    def move(self):
        self.y -= self.fart # Pelleten skal bare oppover

    def draw(self):
        pg.draw.circle(self.vinduobjekt, self.farge, (self.x, self.y), self.radius)

    def avstand(self, annenBall):
        """Metode for å finne avstanden til en annen ball"""
        xAvstand2 = (self.x - annenBall.x) ** 2 # x-avstand i andre
        yAvstand2 = (self.y - annenBall.y) ** 2 # y-avstand i andre

        sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

        radiuser = self.radius + annenBall.radius

        avstand = sentrumsavstand - radiuser

        return avstand
    
class PowerUp(Ball): # En klasse for PowerUp ballen som kommer
    def __init__(self, x, y, radius, farge, vinduobjekt, fart):
        super().__init__(x, y, radius, farge, vinduobjekt, fart)

    def flytt(self):
        self.y += self.fart

    def avstand(self, annenBall):
        """Metode for å finne avstanden til en annen ball"""
        xAvstand2 = (self.x - annenBall.x) ** 2 # x-avstand i andre
        yAvstand2 = (self.y - annenBall.y) ** 2 # y-avstand i andre

        sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

        radiuser = self.radius + annenBall.radius

        avstand = sentrumsavstand - radiuser

        return avstand

class Stjerne(Ball): # Skal kun bli brukt for bakgrunn
    def __init__(self, x, y, radius, farge, vindusobjekt, fart):
        super().__init__(x, y, radius, farge, vindusobjekt, fart)


def title_screen():
    stjerner = [] # Liste over stjeren som kommer til å være i bakgrunnen.
    for i in range(0, 140):
        # Stjernen blir laget med klassen og har en tilfeldig posisjon og en tilfelfig radius mellom 5 og 10.
        # Sjernen plassert i listen stjerner
        stjerner.append(Stjerne(random.randint(0, VINDU_BREDDE), random.randint(0, VINDU_HOYDE), random.randint(5, 10), (100, 100, 0), vindu, 0))

    # Gradvis øk fontstørrelsen til original størrelse
    start_font = 1
    while start_font < 64: # Endre 64 til ønsket størrelse på tittelteksten
        start_font += 1
        tittel_font = pg.font.Font(None, start_font)
        tittel_tekst = tittel_font.render("Space Invaders", True, (255, 255, 255))
        tittel_tekst_posisjon = tittel_tekst.get_rect(center=(VINDU_BREDDE // 2, VINDU_HOYDE // 2 - 50))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        # Tegner bakgrunnen
        vindu.fill((0, 0, 0)) # Bakgrunn for title-screen vil være verdien inni
        for stjerne in stjerner: # Her så skjekker man alle cellene i spillet
            stjerne.tegn() # tegner alle cellene

        # Tegner tittelteksten
        vindu.blit(tittel_tekst, tittel_tekst_posisjon)

        pg.display.flip()
        time.sleep(0.01) # Slik at tittelen bruker lengre tid på å bli ferdig

    # Lag play-knapp
    play_font = pg.font.Font(None, 32)
    play_tekst = play_font.render("Play", True, (255, 255, 255))
    play_tekst_posisjon = play_tekst.get_rect(center=(VINDU_BREDDE // 2, VINDU_HOYDE // 2 + 50))

    color_timer = 0 # Variabel som blir brukt for knappen sin farge
    lys_farge = True # Brukes også som variabel for knappen sin farge
    boks_farge = (0, 123, 0) # Knappen sin farge
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if play_tekst_posisjon.collidepoint(mouse_x, mouse_y):
                    return
            
        # Denne if-statmenten gjør slik at hvert sekund fargen på knappen endres
        if time.time() - color_timer > 1:
            if lys_farge == True: # lys_farge starter som True, og gjør derfor knappen mørk
                boks_farge = (0,79,0)
                lys_farge = False # Endrer til False slik at knappen blir lys neste gang
            else:
                boks_farge = (0, 153, 0)
                lys_farge = True
            color_timer = time.time()

        # Tegner tittelteksten
        vindu.blit(tittel_tekst, tittel_tekst_posisjon)

        # Tegner knappen
        pg.draw.rect(vindu, boks_farge, (VINDU_BREDDE // 2 - 50, VINDU_HOYDE // 2 + 30, 100, 40))
        vindu.blit(play_tekst, play_tekst_posisjon)
        pg.display.flip()

# Funksjon som er game over skjermen
def game_over_screen():
    game_over_font = pg.font.SysFont(None, 64)
    restart_button = pg.Rect(VINDU_BREDDE / 2 - 100, VINDU_HOYDE / 2, 200, 50) # Dette er posisjonen og størrelse på knappene
    quit_button = pg.Rect(VINDU_BREDDE / 2 - 100, VINDU_HOYDE / 2 + 100, 200, 50)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    return "restart"
                elif quit_button.collidepoint(mouse_pos):
                    pg.quit()
                    quit()

        # Bakgrunn
        vindu.fill((30, 30, 30))

        # Tegner "GAME OVER"
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(VINDU_BREDDE / 2, 200))
        vindu.blit(game_over_text, game_over_text_rect)

        # Tegner restart knappen
        pg.draw.rect(vindu, (0, 150, 0), restart_button)
        restart_text = game_over_font.render("Restart", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        vindu.blit(restart_text, restart_text_rect)

        # Tegner quit knappen
        pg.draw.rect(vindu, (150, 0, 0), quit_button)
        quit_text = game_over_font.render("Quit", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        vindu.blit(quit_text, quit_text_rect)

        pg.display.flip()



# Start tittel skjerm
title_screen()

# Laster ned alle sprites
spiller_sprite_original = pg.image.load("Assets/SpillerSkip.png")
spiller_sprite = pg.transform.scale(spiller_sprite_original, (60,60))
hinder_sprite_original = pg.image.load("Assets/HinderSkip.png")
hinder_sprite = pg.transform.scale(hinder_sprite_original, (60,60))
hinderDMG_sprite_original = pg.image.load("Assets/HinderSkipDMG.png")
hinderDMG_sprite = pg.transform.scale(hinderDMG_sprite_original, (60,60)) 


hinder_mengde = 3 # Denne variabelen blir brukt senere slik at når en ny level starter

hinder_liste = [] # Liste for å samle alle hindere
for i in range(0, hinder_mengde): # hinder mengde på starten av spillet (første "wave")
    x = random.randint(50, VINDU_BREDDE - 50)
    y = random.randint(50, 150)
    farge = (255, 0, 0)
    hinder = Hinder(x, y, 20, farge, vindu, 0.23, hinder_sprite)
    hinder_liste.append(hinder)


def generer_ny_bolge(bølge_level):

    hinder_liste = []
    for i in range(0, hinder_mengde * bølge_level): # 10 hinder på starten
        x = random.randint(50, VINDU_BREDDE - 50)
        y = random.randint(50, 150)
        farge = (255, 0, 0)
        hinder = Hinder(x, y, 20, farge, vindu, 0.23, hinder_sprite)
        hinder_liste.append(hinder)
    
    return hinder_liste # Returnerer den nye bølgen med fiender


spiller = Spiller(250, 600, 20, (200, 0, 100), vindu, 0.146) # Variabel for spiller karakteren

avstand_mellom_spiller_og_hinder_bool = False
alle_dood2 = False


level = 1  # Når spilleren vinner en bølge med fiender, så skal denne økes med 1

game_over = False
tom_for_pellets = False

ekstra_pellet_ball = []

# Dette er hovedløkken til spillet
while not game_over:

    clock.tick(2500)

    # Skjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True

    # Henter en ordbok med status for alle tastatur-taster
    trykkede_taster = pg.key.get_pressed()

    # Farger bakgrunnen lyseblå
    vindu.fill((135, 206, 235))

    # Tekst som skal vise hvilket level brukeren er på
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    vindu.blit(level_text, (10, 10))  

    spiller.tegn()
    spiller.flytt(trykkede_taster)
    spiller.update_pellets() # Skjekker og oppdaterer pelletsa på skjermen (Siden pelletsa blir dannet innenfor spiller klassen, så skal den ikke blir definert som spiller og hindring.)

    for hinder in hinder_liste: # Går igjennom alle hinderene i spillet
        for pellet in spiller.pellets: # Går igjennom alle pellets i spillet akkurat nå
            if pellet.avstand(hinder) < 20 and hinder.hp != 0: # hvis de pelleten som blir skjekket nå har en avstand på mindre enn 20 (og hvis hindring ikke allerede er dø):
                if pellet.dobbel == False: # Egen variabel som hvis er sann gir dobbel skade til Hinder (hvis du treffer)
                    spiller.pellets.remove(pellet)
                    hinder.hp -= 5
                    hinder.sprite = hinderDMG_sprite # Skal endre bilde til hinder
                    print(hinder.sprite)
                    print(hinder.hp)
                else:
                    spiller.pellets.remove(pellet)
                    hinder.hp -= 10
                    print(hinder.hp)

    for hinder in hinder_liste: # Gjør alle kode delene som må kjøres for alle hinderene
        hinder.tegn() # tegner hinderet
        hinder.flytt() # Flytter hinderet

        if hinder.hp <= 0 and hinder.dood == False: # Når hinderet har 0 hp, vil den dø
            hinder.slutt()
            if hinder.ekstraSkudd == True: # Inne i alle hindere så er den en variabel som sier om den har ekstra skudd eller ikke
                print("EKSTRA SKUDD")
                PowerUp_ball = PowerUp(hinder.x, hinder.y, 15, (100,100,255), vindu, 0.10) # Lager en PowerUp-ball for skuddene
                ekstra_pellet_ball.append(PowerUp_ball)
                #spiller.pellet_counter -= 10
            hinder.dood = True 

        if hinder.avstand(spiller) < 15 and avstand_mellom_spiller_og_hinder_bool == False: # Når spiller og hinder kolliderer kjører koden under
            avstand_mellom_spiller_og_hinder_bool = True

        if hinder.y >= VINDU_HOYDE: # Hvis hinderet treffer enden av bakken så taper spilleren
            avstand_mellom_spiller_og_hinder_bool = True
    

    for P_U in ekstra_pellet_ball: # Går igjennom alle powerUps i spillet akkurat da
        # Tegner og flytter
        P_U.tegn()
        P_U.flytt()

        if P_U.avstand(spiller) < 15: # Når spiller og powerUp-ball kolliderer kjører koden under
            spiller.pellet_counter -= 10
            ekstra_pellet_ball.remove(P_U)
        
        if P_U.y >= VINDU_HOYDE: # Fjerner powerUp-ballen når den treffer bunden av skjermen
            ekstra_pellet_ball.remove(P_U)
            print(f"PowerUp borte, {ekstra_pellet_ball}")


    
    alle_dood = all(hinder.dood for hinder in hinder_liste) # All skjekker 
    if alle_dood == True:
        hinder_liste = [] # Fjerner alle de dø 
        print("ALLE ER DØ")
        level = level + 1 # Øker level med 1, siden spilleren drepte alle hinderene 
        if level % 10 == 0: # Skjekker om levelet er 10, 20, 30, osv. Det gjør den ved å dele på 10, hvis resten er på 0, så er det et helt tall delt på 10. Hvis dette er sant, er det en BOSS
            hinder_liste = [] # Tømmer alle hinderene
            hinder_liste.append(Boss(100, 50, 65, (255, 200, 0), vindu, 0.23)) # Legger inn en BOSS i hinder listen, slik kan koden forsette som den er skrevet uten egen kode for BOSS-en
            
            # Tekst som sier at det er boss
            boss_font = pg.font.SysFont(None, 84) 
            boss_text = boss_font.render(f"Boss {level/10}", True, (255, 0, 0))

            # Tekst som sier hvilket level
            ny_level_font = pg.font.SysFont(None, 64)
            ny_level_text = ny_level_font.render(f"Level {level}", True, (255, 100, 0))

            # Skriver det inn og posisjon
            vindu.blit(boss_text, (VINDU_BREDDE // 2 - 100, 150))
            vindu.blit(ny_level_text, (VINDU_BREDDE // 2 - 100, 200))

            pg.display.flip()

            time.sleep(1.2) # Gir spilleren en pause før neste level starter
            # Plasserer spilleren tilbake til hvor den først startet
            spiller.x = 250
            spiller.y = 600
        else: # Ellers en ny bølge av fiender
            hinder_liste = generer_ny_bolge(level) # Den nye hinder_listen med den nye bølgen

            ny_level_font = pg.font.SysFont(None, 64)
            ny_level_text = ny_level_font.render(f"Level {level}", True, (255, 0, 0))
            vindu.blit(ny_level_text, (VINDU_BREDDE // 2 - 100, 150))

            pg.display.flip()

            time.sleep(1.2)
            spiller.x = 250
            spiller.y = 600


    antall_pellets = font.render(f"{str((spiller.pellet_max - spiller.pellet_counter))}", True, spiller.pellet_skrift) # spiller.pellet_skrift vil endre farge når spiller er tom for skudd

    vindu.blit(antall_pellets, (spiller.x - 11, spiller.y - 12))

    if spiller.pellet_max - spiller.pellet_counter == 0: # Skjekker om skuddene til spilleren er 0
        tom_for_pellets = True # HVis det er sant, så er tom_for_pellets SANN

    if avstand_mellom_spiller_og_hinder_bool or tom_for_pellets: # Hvis avstand_mellom_spiller_og_hinder_bool eller tom_for_pellets er True, så betyr det at hinder og spiller kolliderte, eller at spiller er tom for skudd.
        valg = game_over_screen() # Game over skjermen kommer og spilleren får valget om å restarte eller avslutte
        if valg == "restart":
            # Her må alle verdier bli restarta
            hinder_liste = [] # Nye hindere
            ekstra_pellet_ball = [] # Tømmer alle powerUps

            for i in range(0, hinder_mengde): # så mange hindere som skal være for level 1 
                x = random.randint(50, VINDU_BREDDE - 50)
                y = random.randint(50, 150)
                farge = (255, 0, 0)
                hinder = Hinder(x, y, 20, farge, vindu, 0.23, hinder_sprite)
                hinder_liste.append(hinder)

            spiller = Spiller(250, 600, 20, (200, 0, 100), vindu, 0.146) # Spiller starter på nytt

            avstand_mellom_spiller_og_hinder_bool = False # Kollisjon variabel resetta
            tom_for_pellets = False # Tom for skudd variabel resetta

            level = 1 # Går tilbake til level 1
        elif valg == "quit":
            game_over = True # Går ut av hovedløkken

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()
