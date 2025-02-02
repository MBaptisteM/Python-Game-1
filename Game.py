import pyxel
from random import randint
import math




# Constantes

class Tuiles:
    MUR = (1, 13)

    PLAINE = (5, 12)
    SABLE  = (14, 12)
    NEIGE  = (11, 12)
    ROCHE  = (2, 18)


    SPAWN_PLAINE = (2, 4)
    SPAWN_SABLE  = (3, 4)
    SPAWN_NEIGE  = (0, 4)
    SPAWN_ROCHE  = (1, 4)


    SPAWN_JOUEUR = (6, 13)


    ARBRE_PLAINE = (2, 12)
    ARBRE_SABLE  = (13, 12)
    ARBRE_NEIGE  = (8, 12)
    ARBRE_ROCHE  = (1, 11)


    COFFRE = (14, 0)
    COFFRE_OUVERT = (15, 0)
    PICS = (0, 19)



class Direction:
    NORD  = 'N'
    EST   = 'E'
    SUD   = 'S'
    OUEST = 'O'



class Sprite:

    HEROS = {
        Direction.NORD  : [(24, 0), (32, 0)],
        Direction.EST   : [(40, 0), (48, 0)],
        Direction.SUD   : [(8, 0), (16, 0)],
        Direction.OUEST : [(16, 128), (8, 128)]
    }

    EPEE = {
        Direction.NORD : [(0, 160), (8, 160), (16, 160)],
        Direction.EST  : [(56, 0), (64, 0), (72, 0)]
    }

    SQUELETTE = {
        Direction.NORD  : [(80, 8), (88, 8)],
        Direction.EST   : [(96, 8), (104, 8)],
        Direction.SUD   : [(64, 8), (72, 8)],
        Direction.OUEST : [(0, 136), (8, 136)]
    }

    CHAUVE_SOURIS = [(0, 144), (8, 144)]

    MAGE = {
        Direction.NORD  : (0, 16),
        Direction.EST   : (40, 16),
        Direction.SUD   : (0, 16),
        Direction.OUEST : (8, 16)
    }

    PROJECTILE = (50, 34)



COULEUR_TRANSPARENTE = 1



# Listes dynamiques

ennemis = []
projectiles = []
explosions = []





def get_tuile(tx, ty):
    #assert dans_tableau(tx, ty)
    return pyxel.tilemaps[0].pget(tx, ty)




def dans_tableau(tx, ty):
    return 1 <= tx < pyxel.tilemaps[0].width - 1 and 1 <= ty < pyxel.tilemaps[0].height - 1




def est_solide(tx, ty):
    return get_tuile(tx, ty) in (Tuiles.MUR, Tuiles.ARBRE_PLAINE, Tuiles.ARBRE_SABLE, Tuiles.ARBRE_NEIGE, Tuiles.ARBRE_ROCHE)




def generation_terrain():
    for x in range(256):

        for y in range(256):

            n = pyxel.noise(
                x / 40,
                y / 40,
                0
            )


            if n > 0.4:

                if not randint(0, 6):
                    col = Tuiles.SPAWN_NEIGE

                else:
                    col = Tuiles.NEIGE


            elif n > 0:

                if not randint(0, 6):
                    col = Tuiles.SPAWN_ROCHE

                else:
                    col = Tuiles.ROCHE


            elif n > -0.4:

                if not randint(0, 6):
                    col = Tuiles.SPAWN_PLAINE

                else:
                    col = Tuiles.PLAINE


            else:

                if not randint(0, 6):
                    col = Tuiles.SPAWN_SABLE

                else:
                    col = Tuiles.SABLE


            pyxel.tilemaps[0].pset(x, y, col)


        # Murs tout autour de la map
        pyxel.tilemaps[0].pset(x, 0, Tuiles.MUR)
        pyxel.tilemaps[0].pset(0, x, Tuiles.MUR)
        pyxel.tilemaps[0].pset(x, 255, Tuiles.MUR)
        pyxel.tilemaps[0].pset(255, x, Tuiles.MUR)


    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            x = joueur.x // 8
            y = joueur.y // 8

            if dans_tableau(x + a, y + b):
                pyxel.tilemaps[0].pset(x + a, y + b, Tuiles.SPAWN_JOUEUR)

            if dans_tableau(x + b, y + a):
                pyxel.tilemaps[0].pset(x + b, y + a, Tuiles.SPAWN_JOUEUR)




def contenu():
    for xi in range(18):
        for yi in range(18):

            x = xi + (joueur.x - 60) // 8
            y = yi + (joueur.y - 60) // 8


            tuile = get_tuile(x, y)

            if tuile == Tuiles.SPAWN_NEIGE:

                if not randint(0, 60):
                    pyxel.tilemaps[0].pset(x, y, Tuiles.COFFRE)

                    for a in (-1, 0, 1):
                        for b in (-1, 1):
                            if dans_tableau(x + a, y + b):
                                pyxel.tilemaps[0].pset(x + a, y + b, Tuiles.NEIGE)

                            if dans_tableau(x + b, y + a):
                                pyxel.tilemaps[0].pset(x + b, y + a, Tuiles.NEIGE)

                else:
                    pyxel.tilemaps[0].pset(x, y, Tuiles.ARBRE_NEIGE)


            if tuile == Tuiles.SPAWN_ROCHE:

                if not randint(0, 20):
                    ennemis.append(ChauveSouris(x*8, y*8))
                    pyxel.tilemaps[0].pset(x, y, Tuiles.ROCHE)

                elif not randint(0, 1):
                    pyxel.tilemaps[0].pset(x, y, Tuiles.PICS)

                else:
                    pyxel.tilemaps[0].pset(x, y, Tuiles.ARBRE_ROCHE)


            if tuile == Tuiles.SPAWN_PLAINE:

                if not randint(0, 20):
                    ennemis.append(Mage(x*8, y*8))
                    pyxel.tilemaps[0].pset(x, y, Tuiles.PLAINE)

                else:
                    pyxel.tilemaps[0].pset(x, y, Tuiles.ARBRE_PLAINE)


            if tuile == Tuiles.SPAWN_SABLE:

                if not randint(0, 20):
                    ennemis.append(Squelette(x*8, y*8))
                    pyxel.tilemaps[0].pset(x, y, Tuiles.SABLE)

                else:
                    pyxel.tilemaps[0].pset(x, y, Tuiles.ARBRE_SABLE)




def collision(x, y):

    x1 = int(x // 8)
    y1 = int(y // 8)
    x2 = int((x + 7) // 8)
    y2 = int((y + 7) // 8)
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if est_solide(xi, yi):
                return True
    return False




def deplacer(x, y, dx, dy):

    # Applique les déplacements à x et y en vérifiant
    # les collisions avec les murs/obstacles (collision(x, y))


    for _ in range(pyxel.ceil(abs(dx))):
        pas = max(-1, min(1, dx))
        if collision(x + pas, y):
            break
        x += pas
        dx -= pas

    for _ in range(pyxel.ceil(abs(dy))):
        pas = max(-1, min(1, dy))
        if collision(x, y + pas):
            break
        y += pas
        dy -= pas


    return x, y




def en_mouvement(dx, dy):
    return abs(dx) or abs(dy)




def collision_j(x, y):
    x1 = int(x//8)
    y1 = int(y//8)
    x2 = int((x+7)//8)
    y2 = int((y+7)//8)

    for xi in range(x1, x2+1):
        for yi in range(y1, y2+1):
            tuile = get_tuile(xi, yi)

            if tuile == Tuiles.PICS:
                joueur.vivant = False

            elif tuile == Tuiles.COFFRE:
                pyxel.tilemaps[0].pset(xi, yi, Tuiles.COFFRE_OUVERT)
                joueur.points += 10
                if joueur.vies < 5 and joueur.vivant: joueur.vies += 1




def explosion(expl):
    expl[2] +=1
    if expl[2] == 12:
        explosions.remove(expl)
    else:
        pyxel.circb(expl[0]+4, expl[1]+4, 2*(expl[2]//4), 8+expl[2]%3)




def touche(ennemi):
    touche=False
    if joueur.combat > 0:
        if joueur.direction_attaque==Direction.EST or joueur.direction_attaque==Direction.OUEST:
            if joueur.attaque_x<=ennemi.x<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=ennemi.y<=joueur.attaque_y+joueur.taille_att_y:
                touche=True
            elif joueur.attaque_x<=ennemi.x<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=ennemi.y+ennemi.taille<=joueur.attaque_y+joueur.taille_att_y:
                touche=True
            elif joueur.attaque_x<=ennemi.x+ennemi.taille<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=ennemi.y<=joueur.attaque_y+joueur.taille_att_y:
                touche=True
            elif joueur.attaque_x<=ennemi.x+ennemi.taille<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=ennemi.y+ennemi.taille<=joueur.attaque_y+joueur.taille_att_y:
                touche=True

        else:
            if joueur.attaque_y<=ennemi.y<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=ennemi.x<=joueur.attaque_x+joueur.taille_att_y:
                touche=True
            elif joueur.attaque_y<=ennemi.y+ennemi.taille<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=ennemi.x<=joueur.attaque_x+joueur.taille_att_y:
                touche=True
            elif joueur.attaque_y<=ennemi.y+ennemi.taille<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=ennemi.x+ennemi.taille<=joueur.attaque_x+joueur.taille_att_y:
                touche=True
            elif joueur.attaque_y<=ennemi.y<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=ennemi.x+ennemi.taille<=joueur.attaque_x+joueur.taille_att_y:
                touche=True

    if touche:
        explosions.append([ennemi.x, ennemi.y, 0])
        ennemis.remove(ennemi)
        joueur.points += 1

    if ennemi.x - joueur.taille_x <= joueur.x <= ennemi.x + joueur.taille_x and ennemi.y - joueur.taille_y <= joueur.y <= ennemi.y + joueur.taille_y:
        if joueur.inv <= 0:
            explosions.append([joueur.x, joueur.y, 0])
            ennemi.immobilise = ennemi.duree_immobilisation
            joueur.vies -= 1
            joueur.inv = joueur.inv_frames
            if joueur.vies <= 0:
                joueur.vivant = False




def direction(ennemi):
    if ennemi.immobilise<=0:
        a=joueur.x-ennemi.x
        b=joueur.y-ennemi.y
        if abs(a)>abs(b):
            if a>0:
                ennemi.direction=Direction.EST
                ennemi.dx=1
            else:
                ennemi.direction=Direction.OUEST
                ennemi.dx=-1
        else:
            if b>0:
                ennemi.direction=Direction.NORD
                ennemi.dy=1
            else:
                ennemi.direction=Direction.SUD
                ennemi.dy=-1
    else:
        ennemi.immobilise-=1





class Joueur:
    def __init__(self):
        # position initiale du personnage
        self.x = randint(1, 255) * 8
        self.y = randint(1, 255) * 8

        self.dx = 0
        self.dy = 0


        ###Définition de toutes les caractéristiques du héro ici###

        self.taille_x = 8
        self.taille_y = 8


        #direction dans laquelle le joueur regarde (d=droite,g=gauche,h=haut,b=bas)
        self.direction=Direction.EST

        #la taille des attaiques (x et y correspondent à une attaque en dessous ou haut dessus et sont inversés sur les cotés)
        self.taille_att_x=11
        self.taille_att_y=14

        #nombre de vies restantes
        self.vies=3

        #vitesse en nombre de pixels
        self.vitesse_abs= 1
        #vitesse qui peut changer en fonction de si on est invincible
        self.vitesse=self.vitesse_abs

        #nombre de frames durant une attaque
        self.frame_attaque=15

        #nombre de frames d'attente entre deux attques (doit toujours être négatif)
        self.attente=-10

        #gestion des attaques (si je suis en train d'attaquer ou d'attendre)
        self.combat=self.attente

        self.direction_attaque=self.direction

        #nombre de frames restantes avant que le héro puisse se faire toucher (début de salle ou héro touché)
        self.inv=0
        #nombre de frames lors d'un période d'invincibilité, cette derniere doit etre divisible par la période d'apparition du bouclier (8 par défault)
        self.inv_frames=40

        self.bouclier=True

        self.points=0

        self.vivant=True

        self.attaque_x=0
        self.attaque_y=0


    def update(self):

        if self.bouclier:
            self.vitesse=1
        else:
            self.vitesse=self.vitesse_abs

        self.dx=0
        self.dy=0

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            self.dx = -1 * self.vitesse
            self.direction = Direction.OUEST

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.dx = 1 * self.vitesse
            self.direction = Direction.EST

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z) :
            self.dy = -1 * self.vitesse
            self.direction = Direction.NORD

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.dy = 1 * self.vitesse
            self.direction = Direction.SUD

        if abs(self.dx)>0 and abs(self.dy)>0:
            self.dx=(self.dx/abs(self.dx)*(self.vitesse//2))+(1*self.dx/abs(self.dx))
            self.dy=(self.dy/abs(self.dy)*(self.vitesse//2))+(1*self.dy/abs(self.dy))

        self.x, self.y = deplacer(self.x, self.y, self.dx, self.dy)


        collision_j(self.x, self.y)



        # ATTAQUE

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.combat==self.attente and self.inv==0:
                self.combat=self.frame_attaque

        if self.inv>0:
            if self.inv%8==0:
                if self.bouclier:
                    self.bouclier=False
                else:
                    self.bouclier=True
            self.inv-=1
        elif self.bouclier:
            self.bouclier=False


        #gestion de la direction
        xm=pyxel.mouse_x
        ym=pyxel.mouse_y

        #x,y,taille x, taille y, couleur

        haut_dessus=ym<64
        a_droite=xm>64

        if xm>=0 and ym>=0:
            if self.combat<=0:
                if haut_dessus:
                    if a_droite:
                        if xm<=128-ym:
                            self.direction_attaque=Direction.NORD
                        else:
                            self.direction_attaque=Direction.EST
                    else:
                        if xm>=ym:
                            self.direction_attaque=Direction.NORD
                        else:
                            self.direction_attaque=Direction.OUEST
                else:
                    if a_droite:
                        if xm<=ym:
                            self.direction_attaque=Direction.SUD
                        else:
                            self.direction_attaque=Direction.EST
                    else:
                        if xm>=128-ym:
                            self.direction_attaque=Direction.SUD
                        else:
                            self.direction_attaque=Direction.OUEST


    def atck(self):
        if self.direction_attaque == Direction.EST:

            pyxel.blt(self.x + 8, self.y, 0, *Sprite.EPEE[Direction.EST][self.combat // 5 % 3], 8, 8, 0)

            # pyxel.rect(self.x + self.taille_x, self.y - ((self.taille_att_y - self.taille_y) / 2), self.taille_att_x, self.taille_att_y, 8)
            self.attaque_x = self.x + self.taille_x-1
            self.attaque_y = self.y - ((self.taille_att_y - self.taille_y) / 2)



        elif self.direction_attaque == Direction.OUEST:

            pyxel.blt(self.x - 8, self.y, 0, *Sprite.EPEE[Direction.EST][self.combat // 5 % 3], -8, 8, 0)

            # pyxel.rect(self.x - self.taille_att_x, self.y - ((self.taille_att_y - self.taille_y) / 2), self.taille_att_x, self.taille_att_y, 8)
            self.attaque_x = self.x - self.taille_att_x+1
            self.attaque_y = self.y - ((self.taille_att_y-self.taille_y) / 2)



        elif self.direction_attaque == Direction.SUD:

            pyxel.blt(self.x, self.y + 8, 0, *Sprite.EPEE[Direction.NORD][self.combat // 5 % 3], 8, -8, 0)

            # pyxel.rect(self.x - ((self.taille_att_y - self.taille_x) / 2), self.y + self.taille_y, self.taille_att_y, self.taille_att_x, 8)
            self.attaque_x = self.x - ((self.taille_att_y - self.taille_x) / 2)
            self.attaque_y = self.y + self.taille_y-1



        elif self.direction_attaque == Direction.NORD:

            pyxel.blt(self.x, self.y - 8, 0, *Sprite.EPEE[Direction.NORD][self.combat // 5 % 3], 8, 8, 0)

            # pyxel.rect(self.x - ((self.taille_att_y - self.taille_x) / 2), self.y-self.taille_att_x, self.taille_att_y, self.taille_att_x, 8)
            self.attaque_x = self.x - ((self.taille_att_y - self.taille_x) / 2)
            self.attaque_y = self.y - self.taille_att_x+1





    def draw(self):
        pyxel.blt(self.x, self.y, 0, *Sprite.HEROS[self.direction][(pyxel.frame_count // 6 % 2) if abs(self.dx) or abs(self.dy) else 1], 8, 8, COULEUR_TRANSPARENTE)

        if joueur.bouclier:
            pyxel.blt(joueur.x, joueur.y, 0, 88, 24, 8, 8, 0)

        # cette partie du code est utile (merci de ne pas le supprimer)

        if joueur.combat > 0:
            joueur.atck()
            joueur.combat -= 1

        #10 frames entre deux attaques
        elif joueur.combat > joueur.attente:
            joueur.combat -= 1

        # affichage des points
        pyxel.rect(2 + self.x - 64, 2 + self.y - 64, 44, 10, 7)
        pyxel.text(5 + self.x - 64, 5 + self.y - 64, 'POINTS:' + str(self.points), 0)

        for i in range(joueur.vies):
            pyxel.blt(5 + 10 * i + self.x - 64, 12 + self.y - 64, 0, 80, 48, 8, 8, 0)




class Projectile:

    def __init__(self, x, y, direction):

        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.direction = direction

        self.taille = 4


    def update(self):

        self.dx = 0
        self.dy = 0

        if self.direction == Direction.EST:
            self.dx = 1

        elif self.direction == Direction.OUEST:
            self.dx = -1

        elif self.direction == Direction.SUD:
            self.dy = -1

        elif self.direction == Direction.NORD:
            self.dy = 1


        if (self.dx and est_solide((self.x + self.dx) // 8, self.y // 8)) \
        or (self.dy and est_solide(self.x // 8, (self.y + self.dy) // 8)):
            explosions.append([self.x, self.y, 0])
            projectiles.remove(self)

        self.x += self.dx
        self.y += self.dy



        touche = False
        if joueur.combat > 0:
            if joueur.direction_attaque==Direction.EST or joueur.direction_attaque==Direction.OUEST:
                if joueur.attaque_x<=self.x<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=self.y<=joueur.attaque_y+joueur.taille_att_y:
                    touche=True
                elif joueur.attaque_x<=self.x<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=self.y+self.taille<=joueur.attaque_y+joueur.taille_att_y:
                    touche=True
                elif joueur.attaque_x<=self.x+self.taille<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=self.y<=joueur.attaque_y+joueur.taille_att_y:
                    touche=True
                elif joueur.attaque_x<=self.x+self.taille<=joueur.attaque_x+joueur.taille_att_x and joueur.attaque_y<=self.y+self.taille<=joueur.attaque_y+joueur.taille_att_y:
                    touche=True

            else:
                if joueur.attaque_y<=self.y<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=self.x<=joueur.attaque_x+joueur.taille_att_y:
                    touche=True
                elif joueur.attaque_y<=self.y+self.taille<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=self.x<=joueur.attaque_x+joueur.taille_att_y:
                    touche=True
                elif joueur.attaque_y<=self.y+self.taille<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=self.x+self.taille<=joueur.attaque_x+joueur.taille_att_y:
                    touche=True
                elif joueur.attaque_y<=self.y<=joueur.attaque_y+joueur.taille_att_x and joueur.attaque_x<=self.x+self.taille<=joueur.attaque_x+joueur.taille_att_y:
                    touche=True

        if touche:
            projectiles.remove(self)

        if self.x-self.taille<=joueur.x<=self.x+self.taille and self.y-self.taille<=joueur.y<=self.y+self.taille:

            projectiles.remove(self)

            if joueur.inv<=0:
                explosions.append([joueur.x,joueur.y,0])
                joueur.vies-=1
                joueur.inv=joueur.inv_frames
                if joueur.vies<=0:
                    joueur.vivant=False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, *Sprite.PROJECTILE, self.taille, self.taille, 0)



# OK
class Squelette:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.direction = Direction.EST

        self.duree_immobilisation = 30
        self.immobilise = self.duree_immobilisation

        self.taille=8


    def update(self):

        self.dx = 0
        self.dy = 0

        direction(self)

        self.x, self.y = deplacer(self.x, self.y, self.dx, self.dy)

        touche(self)


    def draw(self):
        # Frame du sprite selon la direction ou le frame_count
        pyxel.blt(self.x, self.y, 0, *Sprite.SQUELETTE[self.direction][(pyxel.frame_count // 6 % 2) if en_mouvement(self.dx, self.dy) else 1], self.taille, self.taille, COULEUR_TRANSPARENTE)



# OK
class Mage:

    def __init__(self,x,y):

        self.x = x
        self.y = y

        self.direction = Direction.EST

        self.duree_immobilisation = 30
        self.immobilise = self.duree_immobilisation

        self.taille = 8

        self.compteur = 0


    def update(self):

        direction(self)

        touche(self)

        self.compteur += 1
        if self.compteur == 100:
            projectiles.append(Projectile(self.x + 2, self.y + 2, self.direction))
            self.compteur=0


    def draw(self):
        pyxel.blt(self.x, self.y, 0, *Sprite.MAGE[self.direction], self.taille, self.taille, 0)



# OK
class ChauveSouris:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.direction = Direction.EST


        self.duree_immobilisation = 30
        self.immobilise = self.duree_immobilisation

        self.taille=8


    def update(self):

        self.dx = 0
        self.dy = 0

        direction(self)

        self.x += self.dx
        self.y += self.dy

        touche(self)


    def draw(self):
        # Frame du sprite selon la direction ou le frame_count
        w = -self.taille if self.direction == Direction.OUEST else self.taille
        pyxel.blt(self.x, self.y, 0, *Sprite.CHAUVE_SOURIS[pyxel.frame_count // 6 % 2], w, self.taille, COULEUR_TRANSPARENTE)





def game_over():
    pyxel.text(45,50, "GAME OVER", 7)
    pyxel.text(42.5,60, f"SCORE : {joueur.points}", 7)

    #affichage et changement du boutton restart
    if 40<=pyxel.mouse_x<=87 and 80<=pyxel.mouse_y<=90:
        pyxel.rect(41, 81, 46, 9, 11)
        pyxel.rectb(40, 80, 48, 11, 3)
        pyxel.text(50,83, "QUITTER", 0)
    else:
        pyxel.rectb(40, 80, 48, 11, 11)
        pyxel.text(50,83, "QUITTER", 7)


def quitter():
    pyxel.quit()





class Jeu:

    def __init__(self):

        # Initialisation de Pyxel
        pyxel.init(128, 128, title="Har Har")

        '''
        pyxel.colors[0] = 0x000000
        pyxel.colors[1] = 0xffa027
        pyxel.colors[2] = 0xffd827
        pyxel.colors[3] = 0xc9dea8
        pyxel.colors[4] = 0xe9ff9f
        pyxel.colors[5] = 0xa9ff9f
        pyxel.colors[6] = 0x2bb63e
        pyxel.colors[7] = 0x53a65f
        pyxel.colors[8] = 0x7db185
        pyxel.colors[9] = 0xcbd3cc
        pyxel.colors[10] = 0xffffff
        pyxel.colors[11] = 0xffffff
        '''




        # Chargement des ressources
        pyxel.load('sample2.pyxres')

        pyxel.mouse(True)





        global joueur
        joueur = Joueur()


        generation_terrain()


        # Musique
        pyxel.playm(0, loop=True)

        # Lancement du jeu
        pyxel.run(self.update, self.draw)



    def update(self):
        if joueur.vivant:
            joueur.update()
            contenu()

            for ennemi in ennemis:
                ennemi.update()

            for projectile in projectiles:
                projectile.update()


        elif 40<=pyxel.mouse_x<=87 and 80<=pyxel.mouse_y<=90 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            quitter()



    def draw(self):

        pyxel.cls(0)

        if joueur.vivant:

            pyxel.camera()
            pyxel.bltm(0, 0, 0, joueur.x-60, joueur.y-60, 128, 128, 0)
            pyxel.camera(joueur.x-60, joueur.y-60)

            pyxel.blt(60, 60, 0, 0, 144, -8, 8, 9)

            for ennemi in ennemis:
                ennemi.draw()

            for projectile in projectiles:
                projectile.draw()

            for explo in explosions:
                explosion(explo)

            joueur.draw()

        else:
            pyxel.camera(0, 0)
            game_over()


Jeu()