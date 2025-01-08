import random, sys
import pygame as pg

pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
clock = pg.time.Clock()
running = True
running2 = True
hugeassfont = pg.font.SysFont('Arial', 150, 1, 0)
hugeassfontplus = pg.font.SysFont('Arial', 160, 1, 0)
bigfont = pg.font.SysFont('Arial', 40)
font = pg.font.SysFont('Arial', 30)
smallfont = pg.font.SysFont('Arial', 20)
vsmallfont = pg.font.SysFont('Arial', 14)
atkfont = pg.font.SysFont('Arial', 17)
width = screen.get_width()
height = screen.get_height()
replay = False
ask = False

class J :
  """
    Contient :  Outils d'initiation de personnage et godmode
                Outils de lancement d'attaque avec système de coup critique et raté d'attaque aléatoire
                Outils de défense avec système de faille défensive avec système de défense critique et raté de déffence aléatoire
                Outils de boite info
                Outils info_attaque et info_defence (Donne les informations nécessaires d'attaque et de défense du joueur)
                Outils getforce, getmana, getpv, getnom, setpv, setpc, setmana et setforce
  """
  def __init__(self,nom,pv,mana,precision,force,defence,id,turn) :
    self.nom = nom

    if self.nom == "N°0" :
      self.nom = "GODMOD"
      self.pv = 10000
      self.mana = 5000
      self.force = 999
      self.prec = 100
      self.defence = 999
      self.id = id
      self.turn = False
    
    elif force + precision + defence <= 100 and 0 <precision <= 25 and pv + mana <= 3000 :
      self.pv = pv
      self.pc = 1
      self.mana = mana
      self.force = force
      self.prec = precision
      self.defence = defence
      self.id = id
      self.turn = False

  def attack(self, bouton_quit, bouton_1, bouton_2, bouton_3, adv, lst_joueur) :
    bouton_1.settexte("Physical"), bouton_2.settexte("Reinforced"), bouton_3.settexte("Magic")
    self.boite_info()
    running = True
    selecAtta = False
    selecMA = False
    atta_type = ""
    mana_uti = ""

    while running :
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
      bouton_1.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_2.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_3.setheight(screen.get_height() - 55, screen.get_height() - 15)
      for ev in pg.event.get():

        if ev.type == pg.QUIT:
          pg.quit()
          running = False
          sys.exit()
        
        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
            pg.quit()
            sys.exit()
          elif bouton_1.getwidth()[0] <= mouse[0] <= bouton_1.getwidth()[1] and bouton_1.getheight()[0] <= mouse[1] <= bouton_1.getheight()[1] :
            if not selecAtta : 
              atta_type = "Physical"
              selecMA = True
          elif bouton_2.getwidth()[0] <= mouse[0] <= bouton_2.getwidth()[1] and bouton_2.getheight()[0] <= mouse[1] <= bouton_2.getheight()[1] :
            if not selecAtta : 
              atta_type = "Reinforced"
          elif bouton_3.getwidth()[0] <= mouse[0] <= bouton_3.getwidth()[1] and bouton_3.getheight()[0] <= mouse[1] <= bouton_3.getheight()[1] :
            if not selecAtta : 
              atta_type = "Magic"
        
        if ev.type == pg.KEYDOWN :
          if ev.key == pg.K_BACKSPACE :
            mana_uti = mana_uti[:-1]
          elif ev.key == pg.K_RETURN : 
            selecMA = True
          
        if ev.type == pg.TEXTINPUT:
          mana_uti += ev.text  # Ajoute le texte Unicode directement
      
      bouton_quit.affiche_bouton()
      
      if not(selecAtta) : 
        selecAtta = self.selec_atta(atta_type, selecAtta, bouton_1, bouton_2, bouton_3)
        if selecAtta : 
          for joueur in lst_joueur : 
            joueur.boite_info()
          adv.boite_info()
          pg.display.flip()
          pg.time.delay(1500)
      
      if not(selecMA) and selecAtta : 
        selecMA = self.mana_atta(mana_uti, selecMA)
        if selecMA : 
          for joueur in lst_joueur : 
            joueur.boite_info()
          adv.boite_info()
          pg.display.flip()
          pg.time.delay(1500)

      if selecMA : 
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        cp_crit = random.randint(1,100)

        if 100 - (35 - self.prec) < cp_crit <= 100 :
          if mana_uti != 0 :
            self.affiche_texte("Your defence has failed", lst_joueur, 2.5, adv)
            self.mana -= mana_uti
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(0)

          else :
            self.affiche_texte("Your defence has failed", lst_joueur, 2.5, adv)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(0)

        elif 1 <= cp_crit <= self.prec :
          if atta_type == "Physical" :
            degats = self.force * 7.5
            self.affiche_texte("You inflict " + str(degats) + " physical damages on a critical hit", lst_joueur, 2.5, adv)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(degats)

          elif atta_type == "Reinforced" :
            degats = self.force * 2 * 1.5 + int(mana_uti) * 2.5 * 1.5
            self.affiche_texte("You inflict " + str(degats) + " physical damages on a critical hit thanks to your mana reinforced attack", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(degats)

          elif atta_type == "Magic" :
            degats = int(mana_uti) * 1.5
            self.affiche_texte("You inflict " + str(degats) + " magic damages on a critical hit", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(degats)

        else :
          if atta_type == "Physical" :
            degats = self.force * 5
            self.affiche_texte("You inflict " + str(degats) + " physical damages", lst_joueur, 2.5, adv)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(degats)

          elif atta_type == "Reinforced" :
            degats = self.force * 2 + int(mana_uti) * 2.5
            self.affiche_texte("You inflict " + str(degats) + " physical damages thanks to your mana reinforced attack", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(degats)

          elif atta_type == "Magic" :
            degats = int(mana_uti)
            self.affiche_texte("You inflict " + str(degats) + " damages with your magic attack", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)
            pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
            return(degats)
      
      for joueur in lst_joueur : 
        joueur.boite_info()
      adv.boite_info()
      pg.display.flip()

  def defences(self, degats, bouton_quit, bouton_1, bouton_2, bouton_3, adv, lst_joueur) :
    bouton_1.settexte("Physical"), bouton_2.settexte("Enchanted"), bouton_3.settexte("Magic")
    running = True
    selecDef = False
    selecMD = False
    def_type = ""
    mana_uti = ""
    
    while running :
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
      bouton_1.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_2.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_3.setheight(screen.get_height() - 55, screen.get_height() - 15)
      for ev in pg.event.get():

        if ev.type == pg.QUIT:
          pg.quit()
          running = False
          sys.exit()
        
        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
            pg.quit()
            sys.exit()
          elif bouton_1.getwidth()[0] <= mouse[0] <= bouton_1.getwidth()[1] and bouton_1.getheight()[0] <= mouse[1] <= bouton_1.getheight()[1] :
            if not selecDef : 
              def_type = "Physical"
              selecMD = True
          elif bouton_2.getwidth()[0] <= mouse[0] <= bouton_2.getwidth()[1] and bouton_2.getheight()[0] <= mouse[1] <= bouton_2.getheight()[1] :
            if not selecDef : 
              def_type = "Enchanted"
          elif bouton_3.getwidth()[0] <= mouse[0] <= bouton_3.getwidth()[1] and bouton_3.getheight()[0] <= mouse[1] <= bouton_3.getheight()[1] :
            if not selecDef : 
              def_type = "Magic"
        
        if ev.type == pg.KEYDOWN :
          if ev.key == pg.K_BACKSPACE :
            mana_uti = mana_uti[:-1]
          elif ev.key == pg.K_RETURN : 
            selecMD = True
          
        if ev.type == pg.TEXTINPUT:
          mana_uti += ev.text  # Ajoute le texte Unicode directement
      
      bouton_quit.affiche_bouton()
    
      if not(selecDef) : 
        selecDef = self.selec_def(def_type, selecDef, bouton_1, bouton_2, bouton_3)
        if selecDef : 
          for joueur in lst_joueur : 
            joueur.boite_info()
          adv.boite_info()
          pg.display.flip()
          pg.time.delay(1500)
      
      if not(selecMD) and selecDef : 
        selecMD = self.mana_atta(mana_uti, selecMD)
        if selecMD : 
          for joueur in lst_joueur : 
            joueur.boite_info()
          adv.boite_info()
          pg.display.flip()
          pg.time.delay(1500)
    
      if selecMD : 
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        def_crit = random.randint(1,100)

        if 100 - (35 - self.prec) < def_crit <= 100 :
          if int(mana_uti) != 0 :
            self.affiche_texte("Your defence failed and you endured the attack head-on", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)
            self.pv -= degats

          else :
            self.affiche_texte("Your defence failed and you endured the attack head-on", lst_joueur, 2.5, adv)
            self.pv -= degats

        elif 1 <= def_crit <= self.prec :
          if def_type == "Physical" :
            degats_def = self.defence * 2.5
            self.affiche_texte("You parry " + str(degats_def) + " physical damages on a perfect defence", lst_joueur, 2.5, adv)

            if degats_def <= degats :
              self.pv -= (degats - degats_def)

          elif def_type == "Enchanted" :
            degats_def = self.defence * 2.5 + int(mana_uti) * 3
            self.affiche_texte("You parry " + str(degats_def) + " damages with one of the most magificent enchanted defence", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)

            if degats_def <= degats :
              self.pv -= (degats - degats_def)

          elif def_type == "Magic" :
            degats_def = int(mana_uti) * 2.5
            self.affiche_texte("You parry " + str(degats_def) + " damages with a magical defence worthy of the world's greatest mages", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)

            if degats_def <= degats :
              self.pv -= (degats - degats_def)

        else :
          if def_type == "Physical" :
            degats_def = self.defence * 2.5
            self.affiche_texte("You parry " + str(degats_def) + " physical damages", lst_joueur, 2.5, adv)

            if degats_def <= degats :
              self.pv -= (degats - degats_def)

          elif def_type == "Enchanted" :
            degats_def = self.defence * 1.5 + int(mana_uti) * 2
            self.affiche_texte("You parry " + str(degats_def) + " damages with an enchanted defence", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)

            if degats_def <= degats :
              self.pv -= (degats - degats_def)

          elif def_type == "Magic" :
            degats_def = int(mana_uti) * 1.5
            self.affiche_texte("You parry " + str(degats_def) + " damages with a magical defence", lst_joueur, 2.5, adv)
            self.mana -= int(mana_uti)

            if degats_def <= degats :
              self.pv -= (degats - degats_def)
        
        running = False
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      
      for joueur in lst_joueur : 
        joueur.boite_info()
      adv.boite_info()
      pg.display.flip()

  def selec_atta(self, atta_type, selecAtta, bouton_1, bouton_2, bouton_3) :
    bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton()
    if not selecAtta :
      if atta_type == "" :
        screen.blit(atkfont.render("Which attack will you choose ?", True, (255, 255, 255)), (int(screen.get_width()/5), 15))
      else :
        screen.blit(atkfont.render("You use an attack of the " + str(atta_type) + " type", True, (255, 255, 255)), (int(screen.get_width()/5), 15))
        selecAtta = True
        return selecAtta
  
  def selec_def(self, def_type, selecDef, bouton_1, bouton_2, bouton_3) :
    bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton()
    if not selecDef :
      if def_type == "" :
        screen.blit(atkfont.render("Which defence will you choose ?", True, (255, 255, 255)), (int(screen.get_width()/5), 15))
      else :
        screen.blit(atkfont.render("You use a defence of the " + str(def_type) + " type", True, (255, 255, 255)), (int(screen.get_width()/5), 15))
        selecDef = True
        return selecDef
  
  def mana_atta(self, mana_uti, selecMD) :
    if not selecMD :
        screen.blit(atkfont.render("Howmuch mana will you use ? " + str(mana_uti), True, (255, 255, 255)), (int(screen.get_width()/5), 15))
    else :
        screen.blit(atkfont.render("You're going to consume " + str(mana_uti) + " mana points", True, (255, 255, 255)), (int(screen.get_width()/5), 15))
        selecMD = True
        return selecMD
  
  def boite_info(self) : 
    if self.turn == True : 
      pg.draw.rect(screen, (0, 255, 0), [13, 13 + (120 * (self.id - 1) + 20 * (self.id - 1)), 219, 119])
    pg.draw.rect(screen, (255, 255, 255), [15, 15 + (120 * (self.id - 1) + 20 * (self.id - 1)), 215, 115])
    pg.draw.rect(screen, (200, 200, 200), [18, 18 + (120 * (self.id - 1) + 20 * (self.id - 1)), 209, 109])
    pg.draw.rect(screen, (170, 170, 170), [18, 21 + (120 * (self.id - 1) + 20 * (self.id - 1)), 206, 106])
    pg.draw.rect(screen, (130, 130, 130), [21, 21 + (120 * (self.id - 1) + 20 * (self.id - 1)), 203, 103])
    pg.draw.rect(screen, (50, 50, 50), [40, 52 + (120 * (self.id - 1) + 20 * (self.id - 1)), 160, 1])
    pg.draw.rect(screen, (50, 50, 50), [122, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 1, 40])
    retirer = vsmallfont.render(str(self.pv)+" HP", 1, (255, 255, 255)).get_rect()[2]
    pos_0 = 165 + retirer
    pos_1 = 116
    pos_2 = 218
    screen.blit(vsmallfont.render(self.nom, 1, (255, 255, 255)), [25, 30 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25])
    screen.blit(vsmallfont.render(str(self.pv)+" HP", 1, (255, 255, 255)), [pos_0 - retirer, 30 + (120 * (self.id - 1) + 20 * (self.id - 1)), retirer, 25])
    screen.blit(vsmallfont.render("Stats :", 1, (255, 255, 255)), [25, 55 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25])
    screen.blit(vsmallfont.render("Strength :", 1, (255, 255, 255)), [25, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25])
    screen.blit(vsmallfont.render("Defence :", 1, (255, 255, 255)), [127, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25])
    screen.blit(vsmallfont.render("Mana :", 1, (255, 255, 255)), [25, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25])
    screen.blit(vsmallfont.render("Accuracy :", 1, (255, 255, 255)), [127, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), 50, 25])
    retirer = vsmallfont.render(str(self.force), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.force), 1, (255, 255, 255)), [pos_1 - retirer, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), retirer, 25])
    screen.blit(vsmallfont.render(str(self.defence), 1, (255, 255, 255)), [pos_2 - retirer, 75 + (120 * (self.id - 1) + 20 * (self.id - 1)), retirer, 25])
    retirer = vsmallfont.render(str(self.mana), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.mana), 1, (255, 255, 255)), [pos_1 - retirer, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), retirer, 25])
    retirer = vsmallfont.render(str(self.prec)+"%", 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.prec)+"%", 1, (255, 255, 255)), [pos_2 - retirer, 95 + (120 * (self.id - 1) + 20 * (self.id - 1)), retirer, 25])

  def affiche_texte(self,texte,liste_joueur,temps,adv) : 
    bouton_quit = Bouton(screen.get_width() - 155, screen.get_width() - 15, screen.get_height() - 55, screen.get_height() - 15, 'Quit', font, (255, 255, 255), "")
    duree = temps * 60
    while duree > 0 :
      clock.tick(60)
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
      for ev in pg.event.get():

        if ev.type == pg.QUIT:
          pg.quit()
          duree = 0
          sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
            pg.quit()
            duree = 0
            sys.exit()
            
      screen.blit(atkfont.render(texte, 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
      for joueur in liste_joueur : 
        joueur.boite_info()
      adv.boite_info()
      bouton_quit.affiche_bouton()
      pg.display.flip()
      duree -= 1
  
  def info_attaque(self) :
    msg = smallfont.render("A physical attack doesn't consume mana, an enchanted one consumes from 1 to 50 mana points and a magic one between 51 and 500 mana points (:", 1, (255, 255, 255))
    text_rect = msg.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(msg, text_rect)

  def info_defence(self) :
    msg = smallfont.render("A physical defence doesn't consume mana, a reinforced one consumes from 1 to 50 mana points and a magic one between 51 and 500 mana points (:", 1, (255, 255, 255))
    text_rect = msg.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 + 50))
    screen.blit(msg, text_rect)

  def getforce(self) :
    return(self.force)

  def getmana(self) :
    return(self.mana)

  def getpv(self) :
    return(self.pv)

  def getnom(self) :
    return(self.nom)
  
  def getid(self) : 
    return(self.id)

  def setpv(self,pv) :
    self.pv = pv

  def setpc(self,pc) :
    self.pc = pc

  def setmana(self,mana) :
    self.mana = mana

  def setforce(self,force) :
    self.force = force
  
  def setturn(self, turn) : 
    self.turn = turn

class Banshee :
  """
    Contient :  Outils d'initiation de la banshee
                Les pv de la banshee évoluent en fonction du nombre de joueurs
                Outils de choix de la cible (peu dévelopée pour le moment)
                Outils de lancement d'attaque (peu dévelopée pour le moment)
                Outils de défense avec système de faille défensive (peu dévelopée pour le moment)
                Outils de boite info
                Outils getpv
  """
  def __init__(self, liste_joueur) :
    self.nom = "Banshee"

    if len(liste_joueur) > 1 :
      self.pv = int(2500 * (len(liste_joueur) * (1 + (len(liste_joueur) - 1 ) * 0.25)))

    else :
      self.pv = 2500

    self.force = 0
    self.mana = 10000
    self.defence = 0
    self.prec = 10
    self.turn = True

  def choose_target(self, liste_joueur):
    if not liste_joueur :
      print("Il n'y a aucun joueur à attaquer.")
      return None

    target = liste_joueur[0]

    for joueur in liste_joueur :
      if joueur.pv > target.pv :
        target = joueur.nom
    return(target)

  def attack(self, joueur_att, liste_joueur) :
    crit = random.randint(1,100)
    att_banshee = random.randint(1,100)
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
    self.affiche_texte("The Banshee prepares her attack", liste_joueur, 3)
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
    
    if 0 < att_banshee <= 60 :
      degats = 250
      self.affiche_texte("The Banshee attacks " + str(joueur_att.getnom()) + " consuming a small amout of mana to inflict " + str(degats) + " damages", liste_joueur, 4)
      self.mana -= 150
      return degats, att_banshee

    if 60 < att_banshee <= 95 :
      degats = 500
      self.affiche_texte("The Banshee attacks " + str(joueur_att.getnom()) + " consuming a great amout of mana to inflict " + str(degats) + " damages", liste_joueur, 4)
      self.mana -= 375
      return degats, att_banshee

    if 95 < att_banshee <= 100 and self.pv <= 1500 :
      degats = self.pv
      self.affiche_texte("The Banshee sacrifices what's left of her health to inflict " + str(degats)+ " damages to all players", liste_joueur, 4)
      self.pv = 0
      self.mana -= 500
      for joueur in liste_joueur :
        joueur.pv -= degats
      return 0,att_banshee

    if 95 < att_banshee <= 100 :
      degats = 750
      self.affiche_texte("The Banshee tries to use her most powerful attack by sacrificing what's left of her health but wasn't weakened enough to use it, instead she inflicts " + str(degats)+ " damages to all players", liste_joueur, 4)
      self.pv -= 125
      self.mana -= 375
      for joueur in liste_joueur :
        joueur.pv -= degats
      return 0,att_banshee

  def defences(self, degats, liste_joueur) :
    def_crit = random.randint(1,100)
    if 100 - (35 - self.prec) < def_crit <= 100 :
      self.affiche_texte("Your attack went through a breach in the Banshee's shield and so she endures it head-on and takes " + str(degats + 50)+ " damages", liste_joueur, 4)
      self.pv -= degats + 50

    elif degats != 0 :
      self.affiche_texte("The Banshee's shield reduces the damages she takes to " + str(degats - 50), liste_joueur, 4)
      self.pv -= degats - 50
    

  def boite_info(self) : 
    retirer = vsmallfont.render(str(self.pv)+" HP", 1, (255, 255, 255)).get_rect()[2]
    pos_0 = screen.get_width() + retirer
    pos_1 = screen.get_width() - 20
    pos_2 = screen.get_width()
    if self.turn == True : 
      pg.draw.rect(screen, (0, 255, 0), [pos_1 - 13 - 219, 13, 239, 129])
    pg.draw.rect(screen, (255, 255, 255), [pos_1 - 15 - 215, 15, 235, 125])
    pg.draw.rect(screen, (200, 200, 200), [pos_1 - 18 - 209, 18, 229, 119])
    pg.draw.rect(screen, (170, 170, 170), [pos_1 - 18 - 206, 21, 226, 116])
    pg.draw.rect(screen, (130, 130, 130), [pos_1 - 21 - 203, 21, 223, 113])
    pg.draw.rect(screen, (50, 50, 50), [pos_1 - 210, 52, 200, 1])
    pg.draw.rect(screen, (50, 50, 50), [pos_1 - 123, 75, 1, 40])
    screen.blit(vsmallfont.render(self.nom, 1, (255, 255, 255)), [pos_1 - 220, 30, 50, 25])
    screen.blit(vsmallfont.render(str(self.pv)+" HP", 1, (255, 255, 255)), [pos_0 - 79 - retirer, 30, retirer, 25])
    screen.blit(vsmallfont.render("Stats :", 1, (255, 255, 255)), [pos_1 - 220, 55, 50, 25])
    screen.blit(vsmallfont.render("Strength :", 1, (255, 255, 255)), [pos_1 - 220, 75, 50, 25])
    screen.blit(vsmallfont.render("Defence :", 1, (255, 255, 255)), [pos_1 - 118, 75, 50, 25])
    screen.blit(vsmallfont.render("Mana :", 1, (255, 255, 255)), [pos_1 - 220, 95, 50, 25])
    screen.blit(vsmallfont.render("Accuracy :", 1, (255, 255, 255)), [pos_1 - 118, 95, 50, 25])
    retirer = vsmallfont.render(str(self.force), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.force), 1, (255, 255, 255)), [pos_1 - 129 - retirer, 75, retirer, 25])
    screen.blit(vsmallfont.render(str(self.defence), 1, (255, 255, 255)), [pos_2 - 27 - retirer, 75, retirer, 25])
    retirer = vsmallfont.render(str(self.mana), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.mana), 1, (255, 255, 255)), [pos_1 - 129 - retirer, 95, retirer, 25])
    retirer = vsmallfont.render(str(self.prec)+"%", 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.prec)+"%", 1, (255, 255, 255)), [pos_2 - 27 - retirer, 95, retirer, 25])

  def affiche_texte(self,texte,liste_joueur,temps) : 
    bouton_quit = Bouton(screen.get_width() - 155, screen.get_width() - 15, screen.get_height() - 55, screen.get_height() - 15, 'Quit', font, (255, 255, 255), "")
    duree = temps * 60
    while duree > 0 :
      clock.tick(60)
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
      for ev in pg.event.get():

        if ev.type == pg.QUIT:
          pg.quit()
          duree = 0
          sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
            pg.quit()
            duree = 0
            sys.exit()
            
      screen.blit(atkfont.render(texte, 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
      for joueur in liste_joueur : 
        joueur.boite_info()
      self.boite_info()
      bouton_quit.affiche_bouton()
      pg.display.flip()
      duree -= 1

  def getpv(self) :
    return(self.pv)
  
  def setturn(self, turn) : 
    self.turn = turn

class Night_walker :
  def __init__(self,liste_joueur) :
    self.nom = "Night Walker"

    if len(liste_joueur) > 1 :
      self.pv = int(1500 * (len(liste_joueur) * (1 + (len(liste_joueur) - 1 ) * 0.25)))
      self.pvbase = int(1500 * (len(liste_joueur) * (1 + (len(liste_joueur) - 1 ) * 0.25)))

    else :
      self.pv = 1500
      self.pvbase = 1500

    self.force = 25
    self.mana = 1000
    self.defence = 25
    self.prec = 37.5
    self.objet_lourd = 3 * len(liste_joueur)
    self.ombre = 0
    self.turn = True

  def choose_target(self,liste_joueur) :
    if not liste_joueur :
      print("Il n'y a aucun joueur à attaquer.")
      return None

    target = liste_joueur[0]

    for joueur in liste_joueur :
      if joueur.pv > target.pv :
        target = joueur.nom
    return(target)

  def attack(self,target,liste_joueur) :
    crit = random.randint(1,100)
    attatype = random.randint(1,100)
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
    self.affiche_texte("The Night Walker prepares his attack", liste_joueur, 4)
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])

    if 100 - (35 - self.prec) < crit <= 100 :
      self.affiche_texte("The Night Walker prepares his attack", liste_joueur, 4)

    elif 0 < crit <= self.prec :
      if 0 < attatype <= 60 :
        degats = self.force * 7.5
        self.mana += len(liste_joueur) * 100
        self.affiche_texte("The Night Walker attacks " + str(target.getnom()) + " quickly and inflicts " + str(degats) + " damages on a critical hit", liste_joueur, 4)
        return(degats)

      elif 60 < attatype <= 95 and self.objet_lourd > 0 :
        degats = self.force * 15
        self.affiche_texte("The Night Walker attacks " + str(target.getnom()) + " using a heavy object found somewhere around the place with surprising strength and inflicts " + str(degats) + " damages", liste_joueur, 4)
        self.objet_lourd -= 1
        return(degats)

      elif 95 < attatype <= 100 :
        degats = self.force * 7.5
        self.ombre += len(liste_joueur)
        self.affiche_texte("The Night Walker attacks " + str(target.getnom()) + " quickly and inflicts " + str(degats) + " damages on a critical hit before disappearing in the shadows", liste_joueur, 4)
        return(degats)

    else :
      if 0 < attatype <= 60 :
        degats = self.force * 5
        self.mana += len(liste_joueur) * 50
        self.affiche_texte("The Night Walker attacks " + str(target.getnom()) + " quickly and inflicts " + str(degats) + " damages", liste_joueur, 4)
        return(degats)

      elif 60 < attatype <= 95 and self.objet_lourd > 0 :
        degats = self.force * 7.5
        self.affiche_texte("The Night Walker attacks " + str(target.getnom()) + " using a heavy object found somewhere around the place and inflicts " + str(degats) + " damages", liste_joueur, 4)
        self.objet_lourd -= 1
        return(degats)

      elif 95 < attatype <= 100 :
        degats = self.force * 5
        self.ombre += len(liste_joueur)
        self.affiche_texte("The Night Walker attacks " + str(target.getnom()) + " quickly and inflicts " + str(degats) + " damages before disappearing in the shadows", liste_joueur, 4)
        return(degats)

  def defences(self,degats,liste_joueur) :
    crit = random.randint(1,100)
    deftype = random.randint(1,100)
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
    self.affiche_texte("The Night Walker prepares his defence", liste_joueur, 4)
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])

    if self.ombre >= 1 :
      self.affiche_texte("The Night Walker moves too fast in the shadows for you to land a hit", liste_joueur, 4)
      self.ombre -= 1

    elif 100 - (35 - self.prec) < crit <= 100 and self.ombre == 0 :
      self.affiche_texte("The Night Walker defences fails", liste_joueur, 4)


    elif 0 < crit <= self.prec and self.ombre == 0 :
      if 0 < deftype <= 60 :
        degats_def = self.defence * 10
        self.affiche_texte("The Night Walker manages to prepare his best defence and parries " + str(degats_def) + " damages", liste_joueur, 4)
        self.pv -= degats - degats_def

      if 60 < deftype <= 95 :
        degats_def = self.defence * 7.5 + 150
        self.affiche_texte("The Night Walker surprisingly quickly changes some parts of his body into shadows using a small amount of mana and parries " + str(degats_def) + " damages", liste_joueur, 4)
        self.pv -=  degats - degats_def
        self.mana -= 100

      if 95 < deftype <= 100 :
        self.affiche_texte("The Night Walker morphs into shadows and dodge every damages", liste_joueur, 4)
        self.ombre += len(liste_joueur)
        self.mana -= 250

    elif self.ombre == 0 :
      if 0 < deftype <= 60 :
        degats_def = self.defence * 5
        self.affiche_texte("The Night Walker manages to parry " + str(degats_def) + " damages", liste_joueur, 4)
        self.pv -= degats - degats_def

      if 60 < deftype <= 95 :
        degats_def = self.defence * 4 + 150
        self.affiche_texte("The Night Walker changes some parts of his body into shadows using a small amount of mana and parries " + str(degats_def) + " damages", liste_joueur, 4)
        self.pv -=  degats - degats_def
        self.mana -= 100

      if 95 < deftype <= 100 :
        degats_def = degats * 0.75
        self.affiche_texte("The Night Walker changes most of his body into shadows using a great amount of mana and parries" + str(degats_def) + " damages", liste_joueur, 4)
        self.pv -= degats - degats_def
        self.mana -= 250

  def boite_info(self) : 
    retirer = vsmallfont.render(str(self.pv)+" HP", 1, (255, 255, 255)).get_rect()[2]
    pos_0 = screen.get_width() + retirer
    pos_1 = screen.get_width() - 20
    pos_2 = screen.get_width()
    if self.turn == True : 
      pg.draw.rect(screen, (0, 255, 0), [pos_1 - 13 - 219, 13, 239, 129])
    pg.draw.rect(screen, (255, 255, 255), [pos_1 - 15 - 215, 15, 235, 125])
    pg.draw.rect(screen, (200, 200, 200), [pos_1 - 18 - 209, 18, 229, 119])
    pg.draw.rect(screen, (170, 170, 170), [pos_1 - 18 - 206, 21, 226, 116])
    pg.draw.rect(screen, (130, 130, 130), [pos_1 - 21 - 203, 21, 223, 113])
    pg.draw.rect(screen, (50, 50, 50), [pos_1 - 210, 52, 200, 1])
    pg.draw.rect(screen, (50, 50, 50), [pos_1 - 123, 75, 1, 40])
    screen.blit(vsmallfont.render(self.nom, 1, (255, 255, 255)), [pos_1 - 220, 30, 50, 25])
    if self.pv < self.pvbase/4 : 
      screen.blit(vsmallfont.render(str(self.pv)+" HP", 1, (255, 255, 255)), [pos_0 - 79 - retirer, 30, retirer, 25])
    else :
      retirer = vsmallfont.render("?"+" HP", 1, (255, 255, 255)).get_rect()[2]
      screen.blit(vsmallfont.render("?"+" HP", 1, (255, 255, 255)), [pos_0 - 79 - retirer, 30, retirer, 25])
    screen.blit(vsmallfont.render("Stats :", 1, (255, 255, 255)), [pos_1 - 220, 55, 50, 25])
    screen.blit(vsmallfont.render("Strength :", 1, (255, 255, 255)), [pos_1 - 220, 75, 50, 25])
    screen.blit(vsmallfont.render("Defence :", 1, (255, 255, 255)), [pos_1 - 118, 75, 50, 25])
    screen.blit(vsmallfont.render("Mana :", 1, (255, 255, 255)), [pos_1 - 220, 95, 50, 25])
    screen.blit(vsmallfont.render("Accuracy :", 1, (255, 255, 255)), [pos_1 - 118, 95, 50, 25])
    screen.blit(vsmallfont.render("Shadow :", 1, (255, 255, 255)), [pos_1 - 220, 115, 50, 25])
    retirer = vsmallfont.render(str(self.force), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.force), 1, (255, 255, 255)), [pos_1 - 129 - retirer, 75, retirer, 25])
    screen.blit(vsmallfont.render(str(self.defence), 1, (255, 255, 255)), [pos_2 - 27 - retirer, 75, retirer, 25])
    retirer = vsmallfont.render(str(self.mana), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.mana), 1, (255, 255, 255)), [pos_1 - 129 - retirer, 95, retirer, 25])
    retirer = vsmallfont.render(str(self.prec)+"%", 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.prec)+"%", 1, (255, 255, 255)), [pos_2 - 27 - retirer, 95, retirer, 25])
    retirer = vsmallfont.render(str(self.ombre), 1, (255, 255, 255)).get_rect()[2]
    screen.blit(vsmallfont.render(str(self.ombre), 1, (255, 255, 255)), [pos_2 - 27 - retirer, 115, retirer, 25])

  def affiche_texte(self,texte,liste_joueur,temps) : 
    bouton_quit = Bouton(screen.get_width() - 155, screen.get_width() - 15, screen.get_height() - 55, screen.get_height() - 15, 'Quit', font, (255, 255, 255), "")
    duree = temps * 60
    while duree > 0 :
      clock.tick(60)
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
      bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
      for ev in pg.event.get():

        if ev.type == pg.QUIT:
          pg.quit()
          duree = 0
          sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
            pg.quit()
            duree = 0
            sys.exit()
            
      screen.blit(atkfont.render(texte, 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
      for joueur in liste_joueur : 
        joueur.boite_info()
      self.boite_info()
      bouton_quit.affiche_bouton()
      pg.display.flip()
      duree -= 1
  
  def getpv(self) :
    return(self.pv)

  def setpv(self,pv) :
    self.pv = pv
  
  def setturn(self, turn) : 
    self.turn = turn

class Bouton :
  def __init__(self,widthtop,widthbot,heighttop,heightbot,texte,font,color,state) : 
    self.widthtop = widthtop
    self.widthbot = widthbot
    self.width = widthbot - widthtop
    self.heighttop = heighttop
    self.heightbot = heightbot
    self.height = heightbot - heighttop
    self.texte = texte
    self.font = font
    self.color = color
    self.state = state
  
  def affiche_bouton(self):
    center_rect = pg.draw.rect(screen, (179, 179, 179), [self.widthtop + 5, self.heighttop + 5, self.width - 5, self.height - 5])
    surf_texte = self.font.render(self.texte, 1, self.color)
    rect_texte = surf_texte.get_rect()
    rect_texte.center = center_rect.center
    mouse = pg.mouse.get_pos()
    if self.state == "Down" :
      pg.draw.rect(screen, (17, 17, 17), [self.widthtop, self.heighttop, self.width + 5, self.height + 5])
      for loop in range(5) : 
        pg.draw.rect(screen, (131, 131, 131), [self.widthtop, self.heighttop + loop, self.width + 5 - loop, 1])
      for loop in range(5) : 
        pg.draw.rect(screen, (131, 131, 131), [self.widthtop + loop, self.heighttop, 1, self.height + 5 - loop])
      
      pg.draw.rect(screen, (69, 69, 69), [self.widthtop + 5, self.heighttop + 5, self.width - 5, self.height - 5])
      screen.blit(surf_texte, rect_texte)
    
    elif self.state == "Dead" : pg.draw.rect(screen, (0, 0, 0), [self.widthtop, self.heighttop, self.width, self.height])
    
    elif self.widthtop <= mouse[0] <= self.widthbot and self.heighttop <= mouse[1] <= self.heightbot and not self.state == "Down" :
      pg.draw.rect(screen, (191, 191, 191), [self.widthtop, self.heighttop, self.width + 5, self.height + 5])
      for loop in range(5) : 
        pg.draw.rect(screen, (77, 77, 77), [self.widthtop, self.heighttop + loop, self.width + 5 - loop, 1])
      for loop in range(5) : 
        pg.draw.rect(screen, (77, 77, 77), [self.widthtop + loop, self.heighttop, 1, self.height + 5 - loop])
      
      pg.draw.rect(screen, (129, 129, 129), [self.widthtop + 5, self.heighttop + 5, self.width - 5, self.height - 5])
      screen.blit(surf_texte, rect_texte)
    
    elif self.state == "Nonselec" :
      pg.draw.rect(screen, (47, 47, 47), [self.widthtop, self.heighttop, self.width + 5, self.height + 5])
      for loop in range(5) : 
        pg.draw.rect(screen, (161, 161, 161), [self.widthtop, self.heighttop + loop, self.width + 5 - loop, 1])
      for loop in range(5) : 
        pg.draw.rect(screen, (161, 161, 161), [self.widthtop + loop, self.heighttop, 1, self.height + 5 - loop])
        
      pg.draw.rect(screen, (99, 99, 99), [self.widthtop + 5, self.heighttop + 5, self.width - 5, self.height - 5])
      screen.blit(surf_texte, rect_texte)
    
    else :
      pg.draw.rect(screen, (77, 77, 77), [self.widthtop, self.heighttop, self.width + 5, self.height + 5])
      for loop in range(5) : 
        pg.draw.rect(screen, (191, 191, 191), [self.widthtop, self.heighttop + loop, self.width + 5 - loop, 1])
      for loop in range(5) : 
        pg.draw.rect(screen, (191, 191, 191), [self.widthtop + loop, self.heighttop, 1, self.height + 5 - loop])
      
      pg.draw.rect(screen, (129, 129, 129), [self.widthtop + 5, self.heighttop + 5, self.width - 5, self.height - 5])
      screen.blit(surf_texte, rect_texte)
  
  def getwidth(self) : 
    return([self.widthtop,self.widthbot])
  
  def getheight(self) : 
    return([self.heighttop,self.heightbot])
  
  def getstate(self) : 
    return(self.state)
  
  def setstate(self, state) : 
    if state in ["", "Down", "Nonselec", "Dead"]:
      self.state = state
  
  def settexte(self, texte) : 
    if type(texte) == str : 
      self.texte = texte
  
  def setwidth(self, widthtop, widthbot) : 
    self.widthtop = widthtop
    self.widthbot = widthbot
    self.width = widthbot - widthtop
  
  def setheight(self, heighttop, heightbot) : 
    self.heighttop = heighttop
    self.heightbot = heightbot
    self.height = heightbot - heighttop

class Texte_Histoire : 
  def __init__(self,heighttop,texte,font) :
    self.widthtop = screen.get_width()/2
    self.heighttop = heighttop
    self.texte = texte
    self.font = font
    self.color = (255, 255, 255)
    self.state = 2
  
  def afficher(self) :
    if self.state == 1 or self.state == 3 : 
      self.widthtop = screen.get_width()/2
      text = atkfont.render(self.texte, True, self.color)
      text_rect = text.get_rect(center = (self.widthtop, self.heighttop))
      screen.blit(text, text_rect)
    self.next_turn()
  
  def next_turn(self) : 
    if self.heighttop == 150 : 
      self.state = 3
      self.color = (15, 15, 15)
    if self.heighttop <= 120 : 
      self.state = 1
    if self.heighttop < 0 : 
      self.state = 0
    if self.state == 1 : 
      self.color = (self.color[0]-2, self.color[1]-2, self.color[2]-2)
    if self.state == 3 : 
      self.color = (self.color[0]+8, self.color[1]+8, self.color[2]+8)
    self.heighttop -= 1
  
  def get_state(self) : 
    return(self.state)
  
  def get_heighttop(self) : 
    return(self.heighttop)
  
  def get_texte(self) : 
    return(self.texte)
  
  def get_state(self) : 
    return(self.state)
  
  def get_color(self) : 
    return(self.color)
  
  def get_font(self) : 
    return(self.font)

class Histoire :
  def __init__(self,texte,font2) : 
    self.bouton_quit = Bouton(screen.get_width() - 155, screen.get_width() - 15, screen.get_height() - 55, screen.get_height() - 15, 'Quit', font, (255, 255, 255), "")
    self.font = font2
    self.texte = self.creer_lst_texte(texte)
  
  def creer_lst_texte(self,texte) :
    lst_texte = [] 
    for loop in range(len(texte)) : 
      lst_texte.append(Texte_Histoire(151 + 30 * loop, texte[loop], self.font))
    return(lst_texte)
  
  def affiche_histoire(self) :
    game_over = True
    while game_over :
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      self.bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
      self.bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
      for ev in pg.event.get():

        if ev.type == pg.QUIT:
          pg.quit()
          game_over = False
          sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if self.bouton_quit.getwidth()[0] <= mouse[0] <= self.bouton_quit.getwidth()[1] and self.bouton_quit.getheight()[0] <= mouse[1] <= self.bouton_quit.getheight()[1] and not self.bouton_quit.getstate() in ["Down", "Dead"] :
            pg.quit()
            game_over = False
            sys.exit()
            
      for loop in self.texte : 
        loop.afficher()
      
      self.bouton_quit.affiche_bouton()
      
      pg.display.flip()
      pg.time.delay(50)
      game_over = not(self.texte[-1].get_state() == 0)
  
  def state_up(self) : 
    self.state += 1
  
  def state_restart(self) : 
    self.state = 1
  
  def getwidth(self) : 
    return([self.widthtop,self.widthbot])
  
  def getheight(self) : 
    return([self.heighttop,self.heightbot])
  
  def getstate(self) : 
    return(self.state)
  
  def settexte(self, texte) : 
    if type(texte) == str : 
      self.texte = texte
  
  def setwidthtop(self, widthtop) : 
    self.widthtop = widthtop
  
  def setheighttop(self, heighttop) : 
    self.heighttop = heighttop

def creation_perso(nom, pv, mana, force, defence, precision, id, turn) :
  """
    Outils de création de personnage.
    creation_perso est automatiquement lancé avec la fonction Jouer, il n'est pas utile de l'appeler diréctement.
    id est un entier associé directement despuis la fonction Jouer.
    Sortie : instance de la classe J
  """
  if nom == "N°0" :
    Joueur = J(nom,0,0,0,0,0,id,True)
    return(Joueur)
  
  if force + precision + defence <= 100 and precision <= 25 and pv + mana <= 3000 :
    Joueur = J(nom,pv,mana,precision,force,defence,id,turn)
    return(Joueur)

def banshee_fight(liste_joueur, nb_joueur, bouton_quit, bouton_1, bouton_2, bouton_3) :
  banshee = Banshee(liste_joueur)
  for joueur in liste_joueur : 
    joueur.boite_info()
  banshee.boite_info()
  pg.display.flip()
  game_over = 0

  while game_over == 0 :
    joueur_att = banshee.choose_target(liste_joueur)
    degats_infliges = banshee.attack(joueur_att, liste_joueur)

    if not 95 < degats_infliges[1] <= 100 :
      banshee.setturn(False)
      joueur_att.setturn(True)
      joueur_att.defences(degats_infliges[0], bouton_quit, bouton_1, bouton_2, bouton_3, banshee, liste_joueur)
      joueur_att.setturn(False)

    for joueur in liste_joueur :
      joueur.setturn(True)
      dgt_joueur = joueur.attack(bouton_quit, bouton_1, bouton_2, bouton_3, banshee, liste_joueur)
      joueur.setturn(False)
      banshee.setturn(True)
      banshee.defences(dgt_joueur, liste_joueur)
      banshee.setturn(False)

      for joueur in liste_joueur :
        if joueur.getpv() <= 0 :
          del(liste_joueur[joueur.getid() - 1])

      if len(liste_joueur) == 0:
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        screen.blit(atkfont.render("The banshee's screams shredded all the adventurers to pieces", 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
        screen.blit(atkfont.render("Game Over", 1, (255, 255, 255)), [int(screen.get_width()/5), 130])
        pg.display.flip()
        pg.time.delay(1500)
        game_over = 1
        break

      if banshee.getpv() <= 0 :
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        if len(liste_joueur) < nb_joueur :
          screen.blit(atkfont.render("You have won at the cost of your comrades' lives", 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
          pg.display.flip()
          pg.time.delay(1500)
          game_over = 2
          break
        else :
          pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
          screen.blit(atkfont.render("Congratulations, you have defeated the banshee", 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
          pg.display.flip()
          pg.time.delay(1500)
          game_over = 2
          break

def NW_fight(liste_joueur,nb_joueur, bouton_quit, bouton_1, bouton_2, bouton_3) :
  NW = Night_walker(liste_joueur)
  for joueur in liste_joueur : 
    joueur.boite_info()
  NW.boite_info()
  pg.display.flip()
  game_over = 0

  while game_over == 0 :
    joueur_att = NW.choose_target(liste_joueur)
    degats_infliges = NW.attack(joueur_att,liste_joueur)
    joueur_att.setturn(True)
    NW.setturn(False)
    joueur_att.defences(degats_infliges, bouton_quit, bouton_1, bouton_2, bouton_3, NW, liste_joueur)
    joueur_att.setturn(False)
    NW.setturn(True)

    joueur_att = NW.choose_target(liste_joueur)
    degats_infliges = NW.attack(joueur_att,liste_joueur)
    joueur_att.setturn(True)
    NW.setturn(False)
    joueur_att.defences(degats_infliges, bouton_quit, bouton_1, bouton_2, bouton_3, NW, liste_joueur)
    joueur_att.setturn(False)
    
    NW.setturn(False)

    for joueur in liste_joueur :
      joueur.setturn(True)
      dgt_joueur = joueur.attack(bouton_quit, bouton_1, bouton_2, bouton_3, NW, liste_joueur)
      joueur.setturn(False)
      NW.setturn(True)
      NW.defences(dgt_joueur, liste_joueur)
      NW.setturn(False)

      for joueur in liste_joueur :
        if joueur.getpv() <= 0 :
          del(liste_joueur[joueur.getid() - 1])

      if len(liste_joueur) == 0:
        pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
        screen.blit(atkfont.render("The darkness has engulfed all the players", 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
        screen.blit(atkfont.render("Game Over", 1, (255, 255, 255)), [int(screen.get_width()/5), 130])
        pg.display.flip()
        pg.time.delay(1500)
        game_over = 1
        break

      if NW.getpv() <= 0 :
        if len(liste_joueur) < nb_joueur :
          pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
          screen.blit(atkfont.render("You have won at the cost of your comrades' lives", 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
          pg.display.flip()
          pg.time.delay(1500)
          game_over = 2
          break
        else :
          pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
          screen.blit(atkfont.render("Congratulations, you have defeated the banshee", 1, (255, 255, 255)), [int(screen.get_width()/5), 100])
          pg.display.flip()
          pg.time.delay(1500)
          game_over = 2
          break

def nbperso(perso, selecPerso, bouton_1, bouton_2, bouton_3, bouton_4) :
    bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton(), bouton_4.affiche_bouton()
    if not selecPerso :
        if perso == 0 :
            screen.blit(atkfont.render("How many player do you want to create ? (4 max)", True, (255, 255, 255)), (15, 15))
        else :
            screen.blit(atkfont.render("You have chosen to play with : " + str(perso), True, (255, 255, 255)), (15, 15))
            selecPerso = True
            return selecPerso

def nom(nom, selecNOM) :
    if not selecNOM :
        screen.blit(atkfont.render("What's your name, adventurer ? " + str(nom), True, (255, 255, 255)), (15, 15))
    else :
        screen.blit(atkfont.render("Your name is : " + str(nom), True, (255, 255, 255)), (15, 15))
        selecNOM = True
        return selecNOM

def nbpv(pv, selecPV, bouton_1, bouton_2, bouton_3, bouton_4) :
    bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton(), bouton_4.affiche_bouton()
    if not selecPV :
        if pv == 0 :
            screen.blit(atkfont.render("How many health points do you have ? ", True, (255, 255, 255)), (15, 15))
        else :
            screen.blit(atkfont.render("You have " + str(pv) + " HP", True, (255, 255, 255)), (15, 15))
            selecPV = True
            return selecPV

def nbmana(mana, selecMana, bouton_1, bouton_2, bouton_3, bouton_4) :
    bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton(), bouton_4.affiche_bouton()
    if not selecMana :
        if mana == 0 :
            screen.blit(atkfont.render("What is the size of your mana pool ?", True, (255, 255, 255)), (15, 15))
        else :
            screen.blit(atkfont.render("You have " + str(mana) + " mana", True, (255, 255, 255)), (15, 15))
            selecMana = True
            return selecMana

def nbstats(stats, force, Def, prec, selecStats, bouton_1, bouton_2, bouton_3, bouton_4) :
    bouton_1.affiche_bouton(), bouton_2.affiche_bouton(), bouton_3.affiche_bouton(), bouton_4.affiche_bouton()
    if not selecStats :
        if stats == 0 :
            screen.blit(atkfont.render("What are your stats? (Strength / Defense / Accuracy)", True, (255, 255, 255)), (15, 15))
        else :
            screen.blit(atkfont.render("You have " + str(force) + " strength", True, (255, 255, 255)), (15, 15))
            screen.blit(atkfont.render("You have " + str(Def) + " defence", True, (255, 255, 255)), (15, 45))
            screen.blit(atkfont.render("You have " + str(prec) + " % accuracy", True, (255, 255, 255)), (15, 75))
            selecStats = True
            return selecStats

def Jouer():
  """
    La fonction Jouer permet de lancer le jeu (créer les personnages entre 1 et 4, de donner les informations essentielles au jeu et de lancer la partie)
    Aucune entrée et sortie
    Pour le moment ne fait que combattre le / les joueur(s) contre la banshee ou Le marcheur de la nuit
  """
  perso = 0
  liste_joueur = []
  selecPerso = False
  selecNOM = False
  selecPV = False
  selecMana = False
  selecStat = False
  name = ""
  pv = 0
  mana = 0
  stats = 0
  force = 0
  Def = 0
  prec = 0
  game_over = 0
  loop = 0
  stop = 0
  hist = 1
  
  bouton_quit = Bouton(screen.get_width() - 155, screen.get_width() - 15, screen.get_height() - 55, screen.get_height() - 15, 'Quit', font, (255, 255, 255), "")
  bouton_compris = Bouton(screen.get_width() - 155, screen.get_width() - 15, screen.get_height() - 120, screen.get_height() - 80, 'Understood', atkfont, (255, 255, 255), "")
  bouton_1 = Bouton(15, 155, screen.get_height() - 55, screen.get_height() - 15, '1 Player', atkfont, (255, 255, 255), "")
  bouton_2 = Bouton(170, 310, screen.get_height() - 55, screen.get_height() - 15, '2 Players', atkfont, (255, 255, 255), "")
  bouton_3 = Bouton(325, 465, screen.get_height() - 55, screen.get_height() - 15, '3 Players', atkfont, (255, 255, 255), "")
  bouton_4 = Bouton(480, 620, screen.get_height() - 55, screen.get_height() - 15, '4 Players', atkfont, (255, 255, 255), "")
  
  while game_over == 0 :
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
    bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
    bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
    bouton_compris.setheight(screen.get_height() - 120, screen.get_height() - 80)
    bouton_compris.setwidth(screen.get_width() - 155, screen.get_width() - 15)
    bouton_1.setheight(screen.get_height() - 55, screen.get_height() - 15)
    bouton_2.setheight(screen.get_height() - 55, screen.get_height() - 15)
    bouton_3.setheight(screen.get_height() - 55, screen.get_height() - 15)
    bouton_4.setheight(screen.get_height() - 55, screen.get_height() - 15)
    
    for ev in pg.event.get():

      if ev.type == pg.QUIT:
        pg.quit()
        game_over = 3
        sys.exit()

      if ev.type == pg.MOUSEBUTTONDOWN:
        mouse = pg.mouse.get_pos()
        if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
          pg.quit()
          game_over = 3
          sys.exit()
          
        elif bouton_1.getwidth()[0] <= mouse[0] <= bouton_1.getwidth()[1] and bouton_1.getheight()[0] <= mouse[1] <= bouton_1.getheight()[1] :
            if not selecPerso : 
              perso = 1
            
            elif not selecPV :
              pv = 2500
              bouton_2.setstate("Down"), bouton_3.setstate("Down"), bouton_4.setstate("Down")
            
            elif not selecMana and 3000 - pv == 500 :
              mana = 500
            
            elif not selecStat : 
              force = 25
              Def = 50
              prec = 25
              stats = 1
              
        elif bouton_2.getwidth()[0] <= mouse[0] <= bouton_2.getwidth()[1] and bouton_2.getheight()[0] <= mouse[1] <= bouton_2.getheight()[1] :
            if not selecPerso : 
              perso = 2
            
            elif not selecPV :
              pv = 2000
              bouton_1.setstate("Down"), bouton_3.setstate("Down"), bouton_4.setstate("Down")
            
            elif not selecMana and 3000 - pv == 1000 :
              mana = 1000
            
            elif not selecStat : 
              force = 30
              Def = 45
              prec = 25
              stats = 1
              
        elif bouton_3.getwidth()[0] <= mouse[0] <= bouton_3.getwidth()[1] and bouton_3.getheight()[0] <= mouse[1] <= bouton_3.getheight()[1] :
            if not selecPerso : 
              perso = 3
            
            elif not selecPV :
              pv = 1500
              bouton_1.setstate("Down"), bouton_2.setstate("Down"), bouton_4.setstate("Down")
            
            elif not selecMana and 3000 - pv == 1500 :
              mana = 1500
            
            elif not selecStat : 
              force = 40
              Def = 40
              prec = 20
              stats = 1
              
        elif bouton_4.getwidth()[0] <= mouse[0] <= bouton_4.getwidth()[1] and bouton_4.getheight()[0] <= mouse[1] <= bouton_4.getheight()[1] :
            if not selecPerso : 
              perso = 4
            
            elif not selecPV :
              pv = 1000
              bouton_1.setstate("Down"), bouton_2.setstate("Down"), bouton_3.setstate("Down")
            
            elif not selecMana and 3000 - pv == 2000 :
              mana = 2000
            
            elif not selecStat : 
              force = 50
              Def = 40
              prec = 10
              stats = 1
      
      if ev.type == pg.KEYDOWN :
        if ev.key == pg.K_BACKSPACE :
          name = name[:-1]
        elif ev.key == pg.K_RETURN : 
          selecNOM = True
          bouton_1.settexte("2500"), bouton_2.settexte("2000"), bouton_3.settexte("1500"), bouton_4.settexte("1000")
      
      if ev.type == pg.TEXTINPUT:
        name += ev.text  # Ajoute le texte Unicode directement

    bouton_quit.affiche_bouton()

    if not selecPerso :
        selecPerso = nbperso(perso, selecPerso, bouton_1, bouton_2, bouton_3, bouton_4)
        if selecPerso :
            pg.display.flip()
            pg.time.delay(1000)
        pg.display.flip()
        
    else : 
      if perso > 0 :
        if not selecNOM : 
          selecNOM = nom(name, selecNOM)
          if selecPV : 
            pg.display.flip()
            pg.time.delay(1000)
          pg.display.flip()
        
        if name == "N°0" and selecNOM: 
          selecPV = True
          selecMana = True
          selecStat = True
        
        if (not selecPV) and selecNOM: 
          selecPV = nbpv(pv,selecPV, bouton_1, bouton_2, bouton_3, bouton_4)
          if selecPV : 
            bouton_1.settexte("500"), bouton_2.settexte("1000"), bouton_3.settexte("1500"), bouton_4.settexte("2000")
            pg.display.flip()
            pg.time.delay(1000)
          pg.display.flip()
        
        if (not selecMana) and selecPV : 
          selecMana = nbmana(mana, selecMana, bouton_1, bouton_2, bouton_3, bouton_4)
          if selecMana : 
            bouton_1.settexte("25/50/25"), bouton_2.settexte("30/45/25"), bouton_3.settexte("40/40/20"), bouton_4.settexte("50/40/10")
            bouton_1.setstate(""), bouton_2.setstate(""), bouton_3.setstate(""), bouton_4.setstate("")
            pg.display.flip()
            pg.time.delay(1000)
          pg.display.flip()
        
        if (not selecStat) and selecMana : 
          selecStat = nbstats(stats, force, Def, prec, selecStat, bouton_1, bouton_2, bouton_3, bouton_4)
          if selecStat : 
            pg.display.flip()
            pg.time.delay(1000)
          pg.display.flip()
        
        if selecStat and loop == 0  : 
          J1 = creation_perso(name, pv, mana, force, Def, prec, 1, False)
          liste_joueur.append(J1)
          perso -= 1
          if perso > 0 : 
            name = ""
            pv = 0
            mana = 0
            force = 0
            Def = 0
            prec = 0
            stats = 0
            loop += 1
            selecNOM = False
            selecPV = False
            selecMana = False
            selecStat = False
          if perso == 0 : 
            while stop == 0 :
              bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
              bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              bouton_compris.setheight(screen.get_height() - 110, screen.get_height() - 70)
              bouton_compris.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              for ev in pg.event.get() : 
                if ev.type == pg.QUIT : 
                  pg.quit()
                  game_over = 3
                  sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN : 
                  mouse = pg.mouse.get_pos()
                  if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
                    pg.quit()
                    game_over = 3
                    sys.exit()
                  elif bouton_compris.getwidth()[0] <= mouse[0] <= bouton_compris.getwidth()[1] and bouton_compris.getheight()[0] <= mouse[1] <= bouton_compris.getheight()[1] and not bouton_compris.getstate() in ["Down", "Dead"] :
                    stop = 1
              pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
              J1.info_attaque()
              J1.info_defence()
              bouton_quit.affiche_bouton()
              bouton_compris.affiche_bouton()
              pg.display.flip()

        if selecStat and loop == 1 : 
          J2 = creation_perso(name, pv, mana, force, Def, prec, 2, False)
          liste_joueur.append(J2)
          perso -= 1
          if perso > 0 : 
            name = ""
            pv = 0
            mana = 0
            force = 0
            Def = 0
            prec = 0
            stats = 0
            loop += 1
            selecNOM = False
            selecPV = False
            selecMana = False
            selecStat = False
          if perso == 0 : 
            while stop == 0 :
              bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
              bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              bouton_compris.setheight(screen.get_height() - 110, screen.get_height() - 70)
              bouton_compris.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              for ev in pg.event.get() : 
                if ev.type == pg.QUIT : 
                  pg.quit()
                  game_over = 3
                  sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN : 
                  mouse = pg.mouse.get_pos()
                  if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
                    pg.quit()
                    game_over = 3
                    sys.exit()
                  elif bouton_compris.getwidth()[0] <= mouse[0] <= bouton_compris.getwidth()[1] and bouton_compris.getheight()[0] <= mouse[1] <= bouton_compris.getheight()[1] and not bouton_compris.getstate() in ["Down", "Dead"] :
                    stop = 1
              pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
              J1.info_attaque()
              J1.info_defence()
              bouton_quit.affiche_bouton()
              bouton_compris.affiche_bouton()
              pg.display.flip()

        if selecStat and loop == 2 : 
          J3 = creation_perso(name, pv, mana, force, Def, prec, 3, False)
          liste_joueur.append(J3)
          perso -= 1
          if perso > 0 : 
            name = ""
            pv = 0
            mana = 0
            force = 0
            Def = 0
            prec = 0
            stats = 0
            loop += 1
            selecNOM = False
            selecPV = False
            selecMana = False
            selecStat = False
          if perso == 0 : 
            while stop == 0 :
              bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
              bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              bouton_compris.setheight(screen.get_height() - 110, screen.get_height() - 70)
              bouton_compris.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              for ev in pg.event.get() : 
                if ev.type == pg.QUIT : 
                  pg.quit()
                  game_over = 3
                  sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN : 
                  mouse = pg.mouse.get_pos()
                  if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
                    pg.quit()
                    game_over = 3
                    sys.exit()
                  elif bouton_compris.getwidth()[0] <= mouse[0] <= bouton_compris.getwidth()[1] and bouton_compris.getheight()[0] <= mouse[1] <= bouton_compris.getheight()[1] and not bouton_compris.getstate() in ["Down", "Dead"] :
                    stop = 1
              pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
              J1.info_attaque()
              J1.info_defence()
              bouton_quit.affiche_bouton()
              bouton_compris.affiche_bouton()
              pg.display.flip()

        if selecStat and loop == 3 : 
          J4 = creation_perso(name, pv, mana, force, Def, prec, 4, False)
          liste_joueur.append(J4)
          perso -= 1
          if perso > 0 : 
            name = ""
            pv = 0
            mana = 0
            force = 0
            Def = 0
            prec = 0
            stats = 0
            loop += 1
            selecNOM = False
            selecPV = False
            selecMana = False
            selecStat = False
          if perso == 0 : 
            while stop == 0 :
              bouton_quit.setheight(screen.get_height() - 55, screen.get_height() - 15)
              bouton_quit.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              bouton_compris.setheight(screen.get_height() - 110, screen.get_height() - 70)
              bouton_compris.setwidth(screen.get_width() - 155, screen.get_width() - 15)
              for ev in pg.event.get() : 
                if ev.type == pg.QUIT : 
                  pg.quit()
                  game_over = 3
                  sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN : 
                  mouse = pg.mouse.get_pos()
                  if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
                    pg.quit()
                    game_over = 3
                    sys.exit()
                  elif bouton_compris.getwidth()[0] <= mouse[0] <= bouton_compris.getwidth()[1] and bouton_compris.getheight()[0] <= mouse[1] <= bouton_compris.getheight()[1] and not bouton_compris.getstate() in ["Down", "Dead"] :
                    stop = 1
              pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
              J1.info_attaque()
              J1.info_defence()
              bouton_quit.affiche_bouton()
              bouton_compris.affiche_bouton()
              pg.display.flip()
      
      else : 
        adversaire_selec = random.randint(1,2)

        if adversaire_selec == 1 :
          if hist == 1 : 
            NW = Night_walker(liste_joueur)
            histo = Histoire(["You enter a dark room, darker than the blackest night of your life", 
                      "Emerging from this darkness, you can see the one you are about to fight", 
                      "The ancient knight in black armor, dead for many years", 
                      "The Night Walker"],atkfont)
            histo.affiche_histoire()
            hist = 0
          for joueur in liste_joueur : 
            joueur.boite_info()
          NW.boite_info()
          pg.display.flip()
          game_over = 1
          NW_fight(liste_joueur, len(liste_joueur), bouton_quit, bouton_1, bouton_2, bouton_3)

        if adversaire_selec == 2 :
          if hist == 1 : 
            banshee = Banshee(liste_joueur)
            histo = Histoire(["You arrive in a clearing illuminated by the moonlight and rejoice at finally being in a peaceful place", 
                              "After eating, you sit by the fire, then go to sleep", 
                              "In the middle of the night, you wake up without knowing why. You thought you heard a scream, but there is no sign of it, so you go back to sleep", 
                              "Barely asleep again, you hear that scream once more...", 
                              "You leave your makeshift shelter and find yourself in a thick fog", 
                              "You hear screams coming from all directions", 
                              "The fog seems to be concentrating at one point and starts to form a silhouette", 
                              "You find yourself face to face with a banshee"],atkfont)
            histo.affiche_histoire()
            hist = 0
          for joueur in liste_joueur : 
            joueur.boite_info()
          banshee.boite_info()
          pg.display.flip()
          game_over = 1
          banshee_fight(liste_joueur, len(liste_joueur), bouton_quit, bouton_1, bouton_2, bouton_3)

def JouerBoucle() :
    running = True
    bouton_oui = Bouton(screen.get_width() / 2 - 275, screen.get_width() / 2 - 100, screen.get_height() / 2 + 10, screen.get_height() / 2 + 60, 'YES', smallfont, (0, 200, 0), "")
    bouton_non = Bouton(screen.get_width() / 2 + 100, screen.get_width() / 2 + 275, screen.get_height() / 2 + 10, screen.get_height() / 2 + 60, 'NO', smallfont, (200, 0, 0), "")
    replay = False
    while running : 
      pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
      bouton_oui.setheight(screen.get_height() / 2 + 10, screen.get_height() / 2 + 60)
      bouton_oui.setwidth(screen.get_width() / 2 - 275, screen.get_width() / 2 - 100)
      bouton_non.setheight(screen.get_height() / 2 + 10, screen.get_height() / 2 + 60)
      bouton_non.setwidth(screen.get_width() / 2 + 100, screen.get_width() / 2 + 275)
      
      for ev in pg.event.get():
        if ev.type == pg.QUIT:
          pg.quit()
          sys.exit()

        if ev.type == pg.MOUSEBUTTONDOWN:
          mouse = pg.mouse.get_pos()
          if bouton_non.getwidth()[0] <= mouse[0] <= bouton_non.getwidth()[1] and bouton_non.getheight()[0] <= mouse[1] <= bouton_non.getheight()[1] :
            pg.quit()
            running = False
            sys.exit()
            
          elif bouton_oui.getwidth()[0] <= mouse[0] <= bouton_oui.getwidth()[1] and bouton_oui.getheight()[0] <= mouse[1] <= bouton_oui.getheight()[1] :
            replay = True
            running = False
          
          elif bouton_non.getwidth()[0] <= mouse[0] <= bouton_non.getwidth()[1] and bouton_non.getheight()[0] <= mouse[1] <= bouton_non.getheight()[1] :
            running = False
            
      text = smallfont.render("Do you want to play again ?", True, (255, 255, 255))
      text_rect = text.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 - 20))
      screen.blit(text, text_rect)
      bouton_oui.affiche_bouton()
      bouton_non.affiche_bouton()
      pg.display.flip() 
    
    return(replay)    

def afficher_nom_jeu() : 
  screen_w_2_10 = screen.get_width()/2 - screen.get_width()/10
  screen_w_5 = screen.get_width()/5
  screen_h_10 = screen.get_height()/10
  pg.draw.rect(screen, (120, 120, 120), [screen_w_2_10 - 10, 40, screen_w_5 + 20, screen_h_10 + 20])
  for loop in range(10) : 
    pg.draw.rect(screen, (180, 180, 180), [screen_w_2_10 - 10, 40 + loop, screen_w_5 + 20 - loop, 1])
  
  for loop in range(10) : 
    pg.draw.rect(screen, (180, 180, 180), [screen_w_2_10 - 10 + loop, 50, 1, screen_h_10 + 10 - loop])
  center_rect = pg.draw.rect(screen, (150, 150, 150), [screen.get_width()/2 - screen.get_width()/10, 50, screen.get_width()/5, screen.get_height()/10]) 
  surf_texte = bigfont.render("D&D?", 1, (255, 255, 255))
  rect_texte = surf_texte.get_rect()
  rect_texte.center = center_rect.center
  screen.blit(surf_texte, rect_texte)

def jouer_bloc(bouton_Jouer, bouton_quit) : 
  screen_w_2_10 = screen.get_width()/2 - screen.get_width()/10
  screen_w_5 = screen.get_width()/5
  screen_h_2_8 = screen.get_height()/2 - screen.get_height()/8
  screen_h_4 = screen.get_height()/4  
  pg.draw.rect(screen, (120, 120, 120), [screen_w_2_10 - 10, screen_h_2_8 - 10, screen_w_5 + 20, screen_h_4 + 20])
  pg.draw.rect(screen, (150, 150, 150), [screen_w_2_10, screen_h_2_8, screen_w_5, screen_h_4])
  for loop in range(10) : 
    pg.draw.rect(screen, (180, 180, 180), [screen_w_2_10 - 10, screen_h_2_8 - 10 + loop, screen_w_5 + 20 - loop, 1])
  for loop in range(10) : 
    pg.draw.rect(screen, (180, 180, 180), [screen_w_2_10 - 10 + loop, screen_h_2_8 - 5, 1, screen_h_4 + 15 - loop])
  bouton_Jouer.affiche_bouton()
  bouton_quit.affiche_bouton()

bouton_Jouer = Bouton(screen.get_width() / 2 - 100, screen.get_width() / 2 + 100, screen.get_height() / 2 - 25, screen.get_height() / 2 + 25, 'Play', font, (0, 200, 0), "")
bouton_quit = Bouton(screen.get_width() / 2 - 100, screen.get_width() / 2 + 100, screen.get_height() - 165, screen.get_height() - 115, 'Quit', font, (255, 255, 255), "")

while running :
    pg.draw.rect(screen, (0, 0, 0), [0, 0, screen.get_width(), screen.get_height()])
    bouton_Jouer.setwidth(screen.get_width() / 2 - 100, screen.get_width() / 2 + 100)
    bouton_Jouer.setheight(screen.get_height() / 2 - 25, screen.get_height() / 2 + 25)
    bouton_quit.setwidth(screen.get_width() / 2 - 100, screen.get_width() / 2 + 100)
    bouton_quit.setheight(screen.get_height() - 165, screen.get_height() - 115)
    for ev in pg.event.get():

      if ev.type == pg.QUIT:
        pg.quit()
        running = False
        sys.exit()
      
      if ev.type == pg.MOUSEBUTTONDOWN:
        mouse = pg.mouse.get_pos()
        if bouton_quit.getwidth()[0] <= mouse[0] <= bouton_quit.getwidth()[1] and bouton_quit.getheight()[0] <= mouse[1] <= bouton_quit.getheight()[1] and not bouton_quit.getstate() in ["Down", "Dead"] :
          pg.quit()
          running = False
          sys.exit()
        elif bouton_Jouer.getwidth()[0] <= mouse[0] <= bouton_Jouer.getwidth()[1] and bouton_Jouer.getheight()[0] <= mouse[1] <= bouton_Jouer.getheight()[1] :
          Jouer()
          ask = True
      
      if ev.type == pg.KEYDOWN :
        if ev.key == pg.K_BACKSPACE :
          mana_uti = mana_uti[:-1]
        elif ev.key == pg.K_RETURN : 
          selecMD = True
        
      if ev.type == pg.TEXTINPUT:
        mana_uti += ev.text  # Ajoute le texte Unicode directement
    
    if ask : 
      running = JouerBoucle()
      replay = running
    
    if replay : 
      Jouer()
    
    if not replay : 
      afficher_nom_jeu()
      jouer_bloc(bouton_Jouer, bouton_quit)
    
    pg.display.flip()