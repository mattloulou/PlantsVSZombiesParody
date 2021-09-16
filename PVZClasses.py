########################################################################################
# File Name: MatthewPechenBergPVZClasses.py
# Description: This is the file that contains the classes for my Plants Vs. Zombies Game
# Author: Matthew Pechen-Berg
# Date: June 16th, 2019
########################################################################################

#basic initialization and definition of common constants and variables
import time 
import pygame
pygame.init()
pygame.mixer.init()
gameWindow=pygame.display.set_mode((800,600))
pygame.mixer.pre_init(44100, -16, 1, 512) #fixes pygame audio
import operator
from math import sqrt
from random import randrange

#zombie spritesheet names
zombieSpritesheetLocations = ["Sprite Sheets\Zombies\Flag Zombie.png","Sprite Sheets\Zombies\Zombie.png","Sprite Sheets\Zombies\Cone Zombie.png","Sprite Sheets\Zombies\Buckethead Zombie.png"]

#loading projectile and misc. sprite images
explosion = pygame.image.load('Sprite Sheets\Other\Explosion.png').convert_alpha()
peas = pygame.image.load('Sprite Sheets\Projectiles\Pea.png').convert_alpha()
melons = pygame.image.load('Sprite Sheets\Projectiles\Watermelon.png').convert_alpha()
flag = pygame.image.load("Sprite Sheets\Zombies\Flag.png").convert_alpha()
arms = pygame.image.load("Sprite Sheets\Zombies\Arms.png").convert_alpha()
heads = pygame.image.load("Sprite Sheets\Zombies\Heads.png").convert_alpha()
sunImage = pygame.image.load("MiscImages\Sun.png").convert_alpha()

#misc animations lists
mAnimationNames = ['Flag','Arms','Heads','Explosion','Peas','Watermelons']
mAnimationSpritesheets = [flag,arms,heads,explosion,peas,melons]
mAnimationSpritesheetColumns = [11,8,13,12,4,8]
mAnimationSpritesheetRows = [1,3,4,1,3,2]
mAnimationTimeBased = [True,True,True,True,False,False]
mAnimationDuration = [1,1,1,1,0,0]
mAnimationFPS = [11,8,13,12,12,12]

#setting up sounds
zombieBite = pygame.mixer.Sound('Sounds\ZombieBite.ogg')
zombieBite.set_volume(0.18)
gulp = pygame.mixer.Sound('Sounds\Gulp.ogg')
gulp.set_volume(0.1)
groan1 = pygame.mixer.Sound('Sounds\Groan.ogg')
groan1.set_volume(0.2)
groan2 = pygame.mixer.Sound('Sounds\Groan2.ogg')
groan2.set_volume(0.2)
groan3 = pygame.mixer.Sound('Sounds\Groan3.ogg')
groan3.set_volume(0.2)
groan4 = pygame.mixer.Sound('Sounds\Groan4.ogg')
groan4.set_volume(0.2)
groan5 = pygame.mixer.Sound('Sounds\Groan5.ogg')
groan5.set_volume(0.2)
groan6 = pygame.mixer.Sound('Sounds\Groan6.ogg')
groan6.set_volume(0.2)
splat1 = pygame.mixer.Sound('Sounds\Splat.ogg')
splat1.set_volume(0.15)
splat2 = pygame.mixer.Sound('Sounds\Splat2.ogg')
splat2.set_volume(0.15)
splat3 = pygame.mixer.Sound('Sounds\Splat3.ogg')
splat3.set_volume(0.15)
shoot1 = pygame.mixer.Sound('Sounds\Throw.ogg')
shoot1.set_volume(0.15)
shoot2 = pygame.mixer.Sound('Sounds\Throw2.ogg')
shoot2.set_volume(0.15)
sunCollect = pygame.mixer.Sound('Sounds\Points.ogg')
sunCollect.set_volume(0.25)
potatoExplode = pygame.mixer.Sound('Sounds\Potato_mine.ogg') 
potatoExplode.set_volume(0.25)
ignite1 = pygame.mixer.Sound('Sounds\Ignite.ogg') 
ignite1.set_volume(0.1)
ignite2 = pygame.mixer.Sound('Sounds\Ignite2.ogg') 
ignite2.set_volume(0.1)
melonImpact1 = pygame.mixer.Sound('Sounds\melonImpact.ogg') 
melonImpact1.set_volume(0.1)
melonImpact2 = pygame.mixer.Sound('Sounds\melonImpact2.ogg') 
melonImpact2.set_volume(0.1)

#----------------------------------------#
# ~~~~~~~~~~ Global Functions ~~~~~~~~~~ #
#----------------------------------------#

def calculateDistance(x1, x2, y1, y2):
    distance = sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

#------------------------------------#
# ~~~~~~~~~~ Classes ~~~~~~~~~~~~~~~ #
#------------------------------------#

class MainUnits(pygame.sprite.Sprite):
    """The common functions in some classes"""

    def damageTintTimer(self):
        if self.lastFrameHealth != self.health:
            self.damageTimer = time.time()
        self.lastFrameHealth = self.health

#------------------------------------------------------------------------------------------------------------------------#
        
class Plant(MainUnits):
    """The 'towers' in the game, the different plants that can be placed by the user."""

    def __init__(self, name = "", health = 0, recharge = 0, col = 0, row = 0, spriteSheet = None, spriteSheetColumns = 0, spriteSheetRows = 0, fps = 0, targetable = True, fileLocation = ''):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.health = health
        self.baseHealth = health
        self.recharge = recharge
        self.col = col
        self.row = row
        self.spritesheet = spriteSheet
        self.spritesheetColumns = spriteSheetColumns
        self.spritesheetRows = spriteSheetRows
        self.animationFPS = fps
        self.targetable = targetable
        self.horizontalIndex = 0
        self.verticalIndex = 0
        self.rect = self.spritesheet.get_rect()     
        self.sheetWidth = self.rect.width
        self.rect.width = self.sheetWidth / self.spritesheetColumns
        self.sheetHeight = self.rect.height
        self.rect.height = self.sheetHeight / self.spritesheetRows
        self.initialTime = time.time()
        self.plantTime = time.time()
        self.attackAnimationTimer = time.time()
        self.triggered = False
        self.attackTimer = 0
        self.initiated = False
        self.centreX = (self.col+1)*80
        self.centreY = 140+(self.row+1)*80
        self.damageSpritesheet = pygame.image.load(fileLocation).convert_alpha()
        self.damageSpritesheet.fill((100, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        self.damageTimer = 0
        self.lastFrameHealth = health

    def __str__(self):
        return "("+str(name)+", health: "+str(health)+", recharge: "+str(recharge)+", col: "+str(col)+", row: "+str(row)+")"

    def update(self): #update the spritesheet image
        self.spritesheet.set_clip(self.rect.width*self.horizontalIndex,self.rect.height*self.verticalIndex, self.rect.width, self.rect.height)
        if time.time() - self.damageTimer < 0.1 and self.health > 0:
            self.image = self.damageSpritesheet.subsurface(self.spritesheet.get_clip())
        else:
            self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
            
    def loadNextImage(self):
        if (time.time() - self.initialTime) > (1./self.animationFPS):
            self.horizontalIndex = (self.horizontalIndex + 1) % self.spritesheetColumns
            self.initialTime = self.initialTime + (1./self.animationFPS)

    #run various actions
    def runActions(self,other,other2,other3):
        self.explode(other,other2)
        self.changeAppearance()
        self.prickZombies(other)
        self.spawnSun(other3)
        self.shoot(other,other2)
        self.launch(other,other2)
        self.damageTintTimer()

    #potato mine functionality
    def explode(self,other,other2):
        if self.name == "Potato Mine":

            #update potato mine if fuse timer ends
            if time.time() - self.plantTime >= 14: 
                self.targetable = False
                self.verticalIndex = 2

                #check for activation
                if not self.triggered:
                    for zombie in other.zombies:
                        if zombie.x+80 < self.col*80+120 and zombie.row == self.row and zombie.health > 0:
                            self.triggered = True
                if self.triggered and self.attackTimer == 0: #initiate attack timer
                    self.attackTimer = time.time()
                if self.attackTimer != 0 and time.time()-self.attackTimer >= 2: #activate explosion
                    self.health = 0
                    for zombie in other.zombies:
                        if zombie.row == self.row and abs((zombie.x + (zombie.rect.width/2)) - (self.col+1)*80) <=70:
                            zombie.health = 0
                    other2.append(Animation(mAnimationNames[3],mAnimationSpritesheets[3],mAnimationSpritesheetColumns[3],mAnimationSpritesheetRows[3],mAnimationTimeBased[3],mAnimationDuration[3],self.row,mAnimationFPS[3],(self.col+1)*80-48,172+self.row*80))
                    potatoExplode.play()

            #update potato mine animation set
            elif time.time() - self.plantTime >= 13:
                self.verticalIndex = 1

    #wall-nut and tall-nut functionality
    def changeAppearance(self): #change nut appearance as the health lowers
        if "nut" in self.name:
            if self.health < self.baseHealth/3.:
                self.verticalIndex = 2
            elif self.health < self.baseHealth/3.*2:
                self.verticalIndex = 1

    #spikeweed and spikerock functionality
    def prickZombies(self,other):
        if 'Spike' in self.name:
            if not self.initiated:
                self.attackTimer = time.time()
                self.initiated = True
                self.damage = 14 
                if 'weed' in self.name:
                    self.damage = 7

            #Deal damage to zombies on top of it
            self.triggered = False
            for zombie in other.zombies: #check if zombies walk on it
                if zombie.row == self.row and zombie.x - self.centreX < -15 and zombie.x - self.centreX > -125 and zombie.health > 0:
                    self.triggered = True
                    self.verticalIndex = 1
            if self.triggered == False:
                self.attackTimer = time.time()
                self.verticalIndex = 0

            #deal damage to zombies on it
            if time.time() - self.attackTimer > 0.526:
                self.attackTimer = self.attackTimer + 0.526
                for zombie in other.zombies:
                    if zombie.row == self.row and zombie.x - self.centreX < -15 and zombie.x - self.centreX > -125 and zombie.health > 0:
                        zombie.health = zombie.health - self.damage

    #sunflower and twin-sunflower functionality
    def spawnSun(self,other):
        if 'flower' in self.name:
            if not self.initiated:
                self.initiated = True
                self.spawnInterval = 34
                self.spawnQuantity = 1
                if 'win' in self.name: #for twin sunflower
                    self.spawnQuantity = 2

            #spawn suns after required down-time
            if (time.time() - self.plantTime) >= self.spawnInterval:
                for i in range(self.spawnQuantity):
                    self.newSunX = randrange(self.centreX - 100,self.centreX + 101)
                    self.newSunY = randrange(self.centreY - 100,self.centreY + 101)
                    if self.newSunX < 40:
                        self.newSunX = 40
                    if self.newSunY < 100:
                        self.newSunY = 100
                    if self.newSunY > 520:
                        self.newSunY = 520
                    if self.newSunX > 720:
                        self.newSunX = 720
                    other.append(Sun(self.newSunX,self.newSunY))
                    self.plantTime = self.plantTime + self.spawnInterval

            #update the sunflower colour if suns are closer to coming out
            elif (time.time() - self.plantTime) >= (self.spawnInterval - 1):
                self.verticalIndex = 2
            elif (time.time() - self.plantTime) >= (self.spawnInterval - 3.5):
                self.verticalIndex = 1
            else:
                self.verticalIndex = 0

    #functionality for pea-shooting plants
    def shoot(self,other,other2):
        if 'pea' in self.name or 'Pea' in self.name:
            if not self.initiated: #initiate basic data
                self.projectileType = 1
                self.initiated = True
                self.attackTimer = time.time()
                self.fire = False
                self.fire2 = False
                self.fire3 = False
                self.fire4 = False
                self.finishedFiring = False
                self.finishedFiring2 = False
                self.finishedFiring3 = False
                self.fireSound = False
                if 'Snow' in self.name:
                    self.projectileType = 0

            #Activate commence pea firing (quantity based off the plant type)
            self.triggered = False
            for zombie in other.zombies:
                if zombie.row == self.row and zombie.x < 790 and zombie.x + 90 > self.centreX and zombie.health > 0:
                    self.triggered = True
            if not self.triggered:
                self.attackTimer = time.time()
            if time.time() - self.attackTimer > 1.95 and not self.fire4:
                self.fire4 = True
                self.attackTimer = self.attackTimer + 1.5
            if time.time() - self.attackTimer > 1.8 and not self.fire3 and not self.finishedFiring3:
                self.fire3 = True
            if time.time() - self.attackTimer > 1.65 and not self.fire2 and not self.finishedFiring2:
                self.fire2 = True
            if time.time() - self.attackTimer > 1.5 and not self.fire and not self.finishedFiring:
                if self.name != 'Gatling Pea':
                    self.attackAnimationTimer = time.time()
                    self.verticalIndex = 1
                self.fire = True

            #spawn in the peas after they are queued to fire (if called upon)
            if self.name != 'Gatling Pea' and time.time() - self.attackAnimationTimer > 1./self.animationFPS:
                self.verticalIndex = 0
            if self.fire:
                other2.append(Animation(mAnimationNames[4],mAnimationSpritesheets[4],mAnimationSpritesheetColumns[4],mAnimationSpritesheetRows[4],mAnimationTimeBased[4],mAnimationDuration[4],self.row,mAnimationFPS[4],self.centreX-48,self.centreY-63,self.projectileType))
                self.fire = False
                self.finishedFiring = True
                self.fireSound = True
            elif self.fire2:
                if self.name != 'Peashooter' and self.name != 'Snow Pea':
                    other2.append(Animation(mAnimationNames[4],mAnimationSpritesheets[4],mAnimationSpritesheetColumns[4],mAnimationSpritesheetRows[4],mAnimationTimeBased[4],mAnimationDuration[4],self.row,mAnimationFPS[4],self.centreX-48,self.centreY-63,self.projectileType))
                    self.fireSound = True
                self.fire2 = False
                self.finishedFiring2 = True
            elif self.fire3:
                if self.name == 'Gatling Pea':
                    other2.append(Animation(mAnimationNames[4],mAnimationSpritesheets[4],mAnimationSpritesheetColumns[4],mAnimationSpritesheetRows[4],mAnimationTimeBased[4],mAnimationDuration[4],self.row,mAnimationFPS[4],self.centreX-48,self.centreY-63,self.projectileType))
                    self.fireSound = True
                self.fire3 = False
                self.finishedFiring3 = True
            elif self.fire4:
                if self.name == 'Gatling Pea':
                    other2.append(Animation(mAnimationNames[4],mAnimationSpritesheets[4],mAnimationSpritesheetColumns[4],mAnimationSpritesheetRows[4],mAnimationTimeBased[4],mAnimationDuration[4],self.row,mAnimationFPS[4],self.centreX-48,self.centreY-63,self.projectileType))
                    self.fireSound = True
                self.fire4 = False
                self.finishedFiring = False
                self.finishedFiring2 = False
                self.finishedFiring3 = False
                
            #play a sound effect upon firing
            if self.fireSound:
                randomNumber = randrange(1,3)
                if randomNumber == 1:
                    shoot1.play()
                else:
                    shoot2.play()
                self.fireSound = False

    #Winter Melon and Melon-pult functionality
    def launch(self,other,other2):
        if 'elon' in self.name:
            if not self.initiated: #initialize melon plant data
                self.projectileType = 1
                self.initiated = True
                self.attackTimer = time.time()
                self.attackAnimationTimer = 0
                self.fire = False
                self.resetAnimation = False
                if self.name == "Melon-pult":
                    self.projectileType = 0
            self.triggered = False
            other.zombies.sort(key=operator.attrgetter('x'))

            #check for targets and establish required parabola variables
            for zombie in other.zombies:
                if zombie.row == self.row and zombie.x > self.centreX and zombie.x < 790 and zombie.health > 0 and not self.triggered:
                    self.triggered = True
                    self.targetZombieY = 126+80*zombie.row
                    self.xInt1 = self.centreX - 63
                    self.xInt2 = zombie.x+10
                    self.vY = self.centreY - 313
                    self.vX = (self.xInt1 + self.xInt2)/2
                    zombie.melonMarks = zombie.melonMarks + 1

            #reset timer if not triggered
            if not self.triggered:
                self.attackTimer = time.time()

            #initiate an attack
            if time.time() - self.attackTimer > 4 and self.horizontalIndex == 0 and self.verticalIndex != 1:
                self.attackTimer = self.attackTimer + 4
                self.verticalIndex = 1
                self.fire = True
                self.resetAnimation = True
                self.attackAnimationTimer = time.time()

            #spawn a watermelon
            if self.fire and self.horizontalIndex == 3:
                self.initialCoefficient = ((self.centreY-63)-(self.vY))/float(((self.centreX-48)-self.vX)**2)
                other2.append(Animation(mAnimationNames[5],mAnimationSpritesheets[5],mAnimationSpritesheetColumns[5],mAnimationSpritesheetRows[5],mAnimationTimeBased[5],mAnimationDuration[5],self.row,mAnimationFPS[5],self.centreX-48,self.centreY-63,self.projectileType,self.initialCoefficient,self.vX,self.vY,self.xInt2 - self.xInt1))
                self.fire = False

            #reset animation back to basic
            if time.time() - self.attackAnimationTimer > 1 and self.resetAnimation:
                self.verticalIndex = 0
                self.resetAnimation = False       
                
#------------------------------------------------------------------------------------------------------------------------#
           
class Defenders(object):
    """Contains the total defense structures on the lawn"""

    def __init__(self, plants=[]):
        self.plants = plants

    def checkDeaths(self): #remove dead plants
        self.livingPlants = []
        for plant in self.plants:
            if plant.health > 0 and plant.row >= 0 and plant.row <=4 and plant.col >= 0 and plant.col <= 8:
                self.livingPlants.append(plant)
        self.plants = self.livingPlants

    #the main repeatedly updating functions
    def update(self,other,other2,other3,screen):
        self.checkDeaths()
        self.plants.sort(key=operator.attrgetter('row'))
        self.drawPlants(screen)
        self.runPlantActions(other,other2,other3)
    
    def runPlantActions(self,other,other2,other3):
        for plant in self.plants:
            plant.runActions(other,other2,other3)

    def append(self,other):
        self.plants.append(other)

    #check if tiles are available
    def tileAvailable(self, col=0, row=0, name=''):
        for plant in self.plants:
            if plant.col == col and plant.row == row:
                if plant.name == name and (name == "Wall-nut" or name == "Tall-nut") and plant.health != plant.baseHealth:
                    plant.health = 0
                else:
                    return False
        return True

    def drawPlants(self,screen):
        for plant in self.plants:
            plant.loadNextImage()
            plant.update()
            tileCentreX = 80+80*plant.col
            tileCentreY = 220+80*plant.row
            unimportantData, unimportantData, frameImageWidth, frameImageHeight = plant.image.get_rect()
            screen.blit(plant.image,(tileCentreX-(frameImageWidth/2),tileCentreY-15-(frameImageHeight/2)))

#------------------------------------------------------------------------------------------------------------------------#

class Zombie(MainUnits):
    """The enemies in the game.""" 

    def __init__(self, name = "", health = 0, row = 0, spritesheet = 0, spritesheetRows = 0, x = 840, zombieType = 0, col = 0):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.health = health
        self.baseHealth = health
        self.x = x
        self.col = (self.x - 40)/80
        self.row = row
        self.spritesheet = pygame.image.load(zombieSpritesheetLocations[spritesheet])
        self.spritesheetRows = spritesheetRows
        self.horizontalIndex = 0
        self.verticalIndex = 0
        self.changeableFPS = 4
        self.baseFPS = 4
        self.rect = self.spritesheet.get_rect()     
        self.sheetWidth = self.rect.width
        self.rect.width = self.sheetWidth / 4
        self.sheetHeight = self.rect.height
        self.rect.height = self.sheetHeight / self.spritesheetRows
        self.spawnTime = time.time()
        self.movementTime = time.time()
        self.initialTime = time.time()
        self.attackMode = False
        self.animationStagesChanged = 0
        self.frozen = False
        self.freezeTime = 0
        self.zombieType = zombieType
        self.deathTimer = 0
        self.melonMarks = 0
        self.dropHead = False
        self.dropHand = False
        self.dropFlag = False
        self.lostHead = False
        self.lostHand = False
        self.lostFlag = False
        self.damageSpritesheet = pygame.image.load(zombieSpritesheetLocations[spritesheet]).convert_alpha()
        self.damageSpritesheet.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        self.frozenSpritesheet = pygame.image.load(zombieSpritesheetLocations[spritesheet]).convert_alpha()
        self.frozenSpritesheet.fill((190, 0, 0, 100), special_flags=pygame.BLEND_SUB)
        self.damageTimer = 0
        self.lastFrameHealth = health

    def __str__(self):
        return "("+str(name)+", health: "+str(health)+", recharge: "+str(recharge)+", col: "+str(col)+", row: "+str(row)+")"

    def update(self): #update the zombie's selected image
        self.spritesheet.set_clip(self.rect.width*self.horizontalIndex,self.rect.height*self.verticalIndex, self.rect.width, self.rect.height)
        if time.time() - self.damageTimer < 0.1 and self.health > 0:
            self.image = self.damageSpritesheet.subsurface(self.spritesheet.get_clip())
        elif self.frozen and self.health > 0:
            self.image = self.frozenSpritesheet.subsurface(self.spritesheet.get_clip())
        else:
            self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())

    def loadNextImage(self): #load the next frame
        if (time.time() - self.initialTime) > (1./self.changeableFPS) and self.health > 0:
            self.horizontalIndex = (self.horizontalIndex + 1) % self.baseFPS
            self.initialTime = self.initialTime + (1./self.changeableFPS)

    def runActions(self,other,other2): #run the various zombie actions
        self.col = (self.x - 40)/80
        if self.health > 0:
            self.enemyInteractions(other)
        self.switchAnimations(other2)
        self.damageTintTimer()
        self.dethaw()

    def checkEnemies(self,other): #check if a zombie is on top of an enemy
        self.attackingColumn = (self.x +30)/80
        for plant in other.plants:
            if plant.row == self.row and plant.col == self.attackingColumn and plant.targetable:
                return True
        return False

    def moveLeft(self): #make the zombie walk left
        if not self.frozen and time.time() - self.movementTime > 0.25 and self.deathTimer == 0:
            if self.horizontalIndex == 0:
                self.x = self.x - 5
            elif self.horizontalIndex == 1:
                self.x = self.x - 2
            elif self.horizontalIndex == 2:
                self.x = self.x - 7 
            else:
                self.x = self.x - 2
            if self.name == "Flag Zombie":
                self.x = self.x - 2
            self.movementTime = self.movementTime + 0.25
        elif self.frozen and time.time() - self.movementTime > 0.25 and self.deathTimer == 0:
            if self.horizontalIndex == 0:
                self.x = self.x - 3
            elif self.horizontalIndex == 1:
                self.x = self.x - 1
            elif self.horizontalIndex == 2:
                self.x = self.x - 4 
            else:
                self.x = self.x - 1
            if self.name == "Flag Zombie":
                self.x = self.x - 2
            self.movementTime = self.movementTime + 0.25
            
    def enemyInteractions(self,other): #zombie interactions with plants
        if self.checkEnemies(other) and self.attackMode == False:
            if self.spritesheetRows == 7:
                self.verticalIndex = self.verticalIndex + 4
            else:
                self.verticalIndex = self.verticalIndex + 3
            self.changeableFPS = 8
            self.attackMode = True
            self.attackTimer = time.time() - 0.25
        elif self.attackMode: #attack plants if in attack mode
            if (time.time() - self.attackTimer) > 0.5:
                self.attackTimer = self.attackTimer + 0.5
                attackedPlant = False
                other.plants.sort(reverse=True, key=operator.attrgetter('col'))
                self.behindColumn = (self.x +40)/80
                for plant in other.plants:
                    if plant.row == self.row and (plant.col == self.attackingColumn or plant.col == self.behindColumn) and not attackedPlant: #deal damage to the plant it is attacking
                        if not self.frozen: #deal less damage if frozen
                            plant.health = plant.health - 20
                        plant.health = plant.health - 30
                        
                        #play the sound effect
                        if plant.health <= 0:
                            gulp.play()
                        else:
                            zombieBite.play()
                        attackedPlant = True
            
        #move left when there is no plant
        else: 
            self.moveLeft()

        #change animations if eating a plant
        if not self.checkEnemies(other) and self.attackMode: 
            self.attackMode = False
            if self.spritesheetRows == 7:
                self.verticalIndex = self.verticalIndex - 4
            else:
                self.verticalIndex = self.verticalIndex - 3
            self.changeableFPS = 4
            self.movementTime = time.time()
            self.horizontalIndex = 0

    def switchAnimations(self,other): #switch the animations based on health for bucket zombies
        if self.name == "Bucket Zombie":
            if self.health <= 0 and self.deathTimer == 0 :
                self.verticalIndex = 3
                self.deathTimer = time.time()
                self.dropHand = True
                self.dropHead = True
            elif self.health <= 433 and self.animationStagesChanged == 1:
                self.verticalIndex = self.verticalIndex + 1
                self.animationStagesChanged = self.animationStagesChanged + 1
                self.dropHand = True
            elif self.health <= 866 and self.animationStagesChanged == 0:
                self.verticalIndex = self.verticalIndex + 1
                self.animationStagesChanged = self.animationStagesChanged + 1
                self.dropHand = True

            #drop body parts at certain health milestones
            if self.dropHand and not self.lostHand:
                other.append(Animation(mAnimationNames[1],mAnimationSpritesheets[1],mAnimationSpritesheetColumns[1],mAnimationSpritesheetRows[1],mAnimationTimeBased[1],mAnimationDuration[1],self.row,mAnimationFPS[1],self.x,270+80*self.row-144,1))
                self.lostHand = True
            if self.dropHead and not self.lostHead:
                other.append(Animation(mAnimationNames[2],mAnimationSpritesheets[2],mAnimationSpritesheetColumns[2],mAnimationSpritesheetRows[2],mAnimationTimeBased[2],mAnimationDuration[2],self.row,mAnimationFPS[2],self.x,270+80*self.row-144,self.zombieType))
                self.lostHead = True

        else: #switch the animations based on health for non-bucket zombies
            if self.health <= 0 and self.deathTimer == 0:
                self.verticalIndex = 2
                self.deathTimer = time.time()
                self.animationStagesChanged = self.animationStagesChanged + 1
                self.dropHand = True
                self.dropHead = True
                if self.name == "Flag Zombie":
                    self.dropFlag = True
            elif self.health <= self.baseHealth/2 and self.animationStagesChanged == 0:
                self.verticalIndex = self.verticalIndex + 1
                self.animationStagesChanged = self.animationStagesChanged + 1
                self.dropHand = True

            #drop body parts at certain health milestones
            if self.dropHand and not self.lostHand:
                other.append(Animation(mAnimationNames[1],mAnimationSpritesheets[1],mAnimationSpritesheetColumns[1],mAnimationSpritesheetRows[1],mAnimationTimeBased[1],mAnimationDuration[1],self.row,mAnimationFPS[1],self.x,270+80*self.row-144,self.zombieType))
                self.lostHand = True
            if self.dropHead and not self.lostHead:
                other.append(Animation(mAnimationNames[2],mAnimationSpritesheets[2],mAnimationSpritesheetColumns[2],mAnimationSpritesheetRows[2],mAnimationTimeBased[2],mAnimationDuration[2],self.row,mAnimationFPS[2],self.x,270+80*self.row-144,self.zombieType))
                self.lostHead = True
            if self.dropFlag and not self.lostFlag:
                other.append(Animation(mAnimationNames[0],mAnimationSpritesheets[0],mAnimationSpritesheetColumns[0],mAnimationSpritesheetRows[0],mAnimationTimeBased[0],mAnimationDuration[0],self.row,mAnimationFPS[0],self.x,270+80*self.row-144))
                self.lostFlag = True

    def dethaw(self): #remove frozen effects after 8 seconds
        if self.frozen and time.time() - self.freezeTimer > 8:
            self.frozen = False

#------------------------------------------------------------------------------------------------------------------------#
            
class Attackers(object): 
    """ The collective class to store the zombies """
    
    def __init__(self, other = []):
        self.zombies = other

    def checkDeaths(self): #remove dead zombies
        self.livingZombies = []
        for zombie in self.zombies:
            if zombie.health > 0 or time.time() - zombie.deathTimer < 3:
                self.livingZombies.append(zombie)
        self.zombies = self.livingZombies
        
    def update(self,other,other2,screen): #use general functions for all zombies
        self.zombies.sort(key=operator.attrgetter('row'))
        self.drawZombies(screen)
        self.zombieActions(other,other2)
        self.checkDeaths()

    def zombieActions(self,other,other2): #iterate through each zombie's individual actions
        for zombie in self.zombies:
            zombie.runActions(other,other2)
        self.makeGroan()
            
    def append(self,other):
        self.zombies.append(other)

    def drawZombies(self,screen):
        for zombie in self.zombies:
            zombie.loadNextImage()
            zombie.update()   
            unimportantData, unimportantData, unimportantData, frameImageHeight = zombie.image.get_rect()
            screen.blit(zombie.image,(zombie.x,270+80*zombie.row-frameImageHeight))

    def checkWinners(self): #check if any zombies won
        for zombie in self.zombies:
            if zombie.x < -80:
                return True
        return False

    def makeGroan(self): #randomly make sound effects based on number of zombies
        randomNum = randrange(1,7000)
        if randomNum <= len(self.zombies):
            groanNum = randrange(6)
            if groanNum == 0:
                groan1.play()
            elif groanNum == 1:
                groan2.play()
            elif groanNum == 2:
                groan3.play()
            elif groanNum == 3:
                groan4.play()
            elif groanNum == 4:
                groan5.play()
            else:
                groan6.play()
        
#------------------------------------------------------------------------------------------------------------------------#

class Animation(pygame.sprite.Sprite):
    """Used to animate things such as projectiles and explosions"""

    def __init__(self, name = "", spriteSheet = None, spriteSheetColumns = 0, spriteSheetRows = 0, timeBased = False, duration = 0, row = 0, fps = 0, x = 0, y = 0, verticalIndex = 0, initialCoefficient = 0, vX = 0, vY = 0, distance = 0):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.row = row
        self.spritesheet = spriteSheet
        self.spritesheetColumns = spriteSheetColumns
        self.spritesheetRows = spriteSheetRows
        self.animationFPS = fps
        self.horizontalIndex = 0
        self.verticalIndex = verticalIndex
        self.rect = self.spritesheet.get_rect()     
        self.sheetWidth = self.rect.width
        self.rect.width = self.sheetWidth / self.spritesheetColumns
        self.sheetHeight = self.rect.height
        self.rect.height = self.sheetHeight / self.spritesheetRows
        self.initialTime = time.time()
        self.durationStartTime = time.time()
        self.duration = duration
        self.timeBased = timeBased
        self.x = x
        self.y = y
        self.initialCoefficient = initialCoefficient
        self.vX = vX
        self.vY = vY
        self.killed = False
        self.projectileType = self.verticalIndex
        self.initialprojectileType = self.projectileType
        self.distance = distance
        self.ignited = False
        
    def update(self):
        self.spritesheet.set_clip(self.rect.width*self.horizontalIndex,self.rect.height*self.verticalIndex, self.rect.width, self.rect.height)
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())

    def loadNextImage(self):
        if (time.time() - self.initialTime) > (1/float(self.animationFPS)):
            self.horizontalIndex = (self.horizontalIndex + 1) % self.spritesheetColumns
            self.initialTime = self.initialTime + (1/float(self.animationFPS))

    def peaDamage(self,other): #deal damage to zombies on collision 
        if self.name == 'Peas':
            for zombie in other.zombies: #check for collision
                if self.x-10 > zombie.x and self.x < zombie.x+55 and self.row == zombie.row and not self.timeBased and not self.killed and zombie.health > 0:
                    self.killed = True
                    randomNum = randrange(1,4)

                    #deal the damage to the zombie
                    zombie.health = zombie.health - 20
                    if self.projectileType == 2:
                        zombie.health = zombie.health - 20
                        zombie.frozen = False
                    elif self.projectileType == 0: #apply freeze effect for the zombie
                        zombie.frozen = True
                        zombie.freezeTimer = time.time()

                    #playing sound effect
                    if randomNum == 1:
                        splat1.play()
                    elif randomNum == 2:
                        splat2.play()
                    else:
                        splat3.play()

    def removeDeadAnimations(self): #remove animations after they expire
        if self.x > 780 or self.y > 600 or self.y > (140 + (self.row+1)*80):
            self.killed = True
            if self.name == "Watermelons":
                
                #play a sound on watermelon impact
                randomNumber = randrange(1,3)
                if randomNumber == 1:
                    melonImpact1.play()
                else:
                    melonImpact2.play()

    def ignite(self,other): #ignite peas when passing through torchwood
        if self.name == 'Peas':
            for plant in other.plants:
                if plant.name == 'Torchwood' and plant.row == self.row and self.x+53 > plant.centreX - 40: #hit detection
                    if self.initialprojectileType == 0: #convert frozen pea to normal
                        self.projectileType = 1
                        self.verticalIndex = 1
                    elif not self.ignited: #convert normal peas to fire
                        self.projectileType = 2
                        self.verticalIndex = 2
                        self.ignited = True

                        #play a sound effect
                        randomNumber = randrange(1,3)
                        if randomNumber == 1:
                            ignite1.play()
                        else:
                            ignite2.play()
                            
    def movePea(self): #move pea right
        if self.name == 'Peas':
            self.x = self.x + 5

    def moveMelon(self): #move melon along a parabola
        if self.name == "Watermelons":
            self.x = self.x + (self.distance/150.)
            self.y = int((self.initialCoefficient)*((self.x-self.vX)**2) + self.vY)

    def melonDamage(self,other): #damage zombies after melon hit 
        if self.name == "Watermelons":
            for zombie in other.zombies:
                if self.x > zombie.x and (120+80*zombie.row) < self.y and self.x < zombie.x+55 and self.row == zombie.row and not self.timeBased and not self.killed and zombie.health > 0:
                    self.killed = True
                    zombie.health = zombie.health - 25 #deal extra damage to the main target
                    for adjacentZombie in other.zombies:
                        if abs(adjacentZombie.x - zombie.x) <= 60 and abs(adjacentZombie.row - zombie.row) <= 1: #deal splash damage
                            adjacentZombie.health = adjacentZombie.health - 25
                            if self.projectileType == 1: #freeze zombies for winter melons
                                adjacentZombie.frozen = True
                                adjacentZombie.freezeTimer = time.time() + 4
                    zombie.freezeTimer = time.time()

                    #play a sound effect
                    randomNumber = randrange(1,3)
                    if randomNumber == 1:
                        melonImpact1.play()
                    else:
                        melonImpact2.play()
        
    def runActions(self,other,other2):
        self.ignite(other)
        self.peaDamage(other2)
        self.removeDeadAnimations()
        self.movePea()
        self.moveMelon()
        self.melonDamage(other2)
                
#------------------------------------------------------------------------------------------------------------------------#

class RunningAnimations(object):
    """ The collective class for running all misc. animations"""
    
    def __init__(self, other = []):
        self.animations = other

    def checkFinishedAnimations(self): #delete all finished animations
        self.ongoingAnimations = []
        for animation in self.animations:
            if not animation.killed and (time.time() - animation.durationStartTime < animation.duration or not animation.timeBased):
                self.ongoingAnimations.append(animation)
        self.animations = self.ongoingAnimations
        
    def update(self,other,other2,screen): #iterate through many functions in this class
        self.checkFinishedAnimations()
        self.drawAnimations(screen)
        self.projectileActions(other,other2)

    def projectileActions(self,other,other2):
        for projectile in self.animations:
            projectile.runActions(other,other2)

    def append(self,other):
        self.animations.append(other)

    def drawAnimations(self,screen):
        for animation in self.animations:
            animation.loadNextImage()
            animation.update()
            screen.blit(animation.image,(int(animation.x),int(animation.y)))

#------------------------------------------------------------------------------------------------------------------------#

class Sun(object):
    """ A class to store sun data """

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.spawnTime = time.time()

#------------------------------------------------------------------------------------------------------------------------#

class Suns(object):
    """ A class to colletively store suns """

    def __init__(self, suns = []):
        self.suns = suns
        
    def checkExpiry(self): #delete suns after they expire
        self.ongoingSuns = []
        for sun in self.suns:
            if time.time() - sun.spawnTime <= 10:
                self.ongoingSuns.append(sun)
        self.suns = self.ongoingSuns

    def checkSunCollection(self, mouseX, mouseY, sunBalance): #check if suns are collected
        for sun in self.suns:
            if calculateDistance(sun.x,mouseX,sun.y,mouseY) <= 35:
                sunBalance[0] = sunBalance[0] + 50
                sun.spawnTime = time.time() - 100
                sunCollect.play()

    def drawSuns(self,screen):
        for sun in self.suns:
            screen.blit(sunImage,(sun.x-64,sun.y-64))

    def update(self, screen): #iterate through functions in this class
        self.checkExpiry()
        self.drawSuns(screen)

    def append(self, other):
        self.suns.append(other)
        
    











            
        
