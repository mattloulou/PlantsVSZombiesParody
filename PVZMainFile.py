###################################################################
# File Name: MatthewPechenBergPVZMainFile.py
# Description: This is the main file for my Plants Vs. Zombies Game
# Author: Matthew Pechen-Berg
# Date: June 16th, 2019
###################################################################

#---------------------------------#
# ~~~~~~ START GAME PROMPT ~~~~~~ #
#---------------------------------#

print "\nWelcome to Matthew Pechen-Berg's Plants vs. Zombies!\n\n"
print "The goal of the game is to place down plants on your lawn \nto defend against an infinite number of waves of zombies.\n"
print "In order to do this, you control a resource called 'sun' that\nyou must produce from sunflowers or receive randomly from the sky.\n"
print "The game ends when a zombie hits the left side of the screen.\n"
print "You can also use the shovel tool to dig up plants you no longer want.\n"
print "But first, you must create your arsenal of plants.\n"
print "--------------------------------CONTROLS--------------------------------\n"
print "LEFT CLICK: Select, deselect, and place plants, collect suns,\nselect and deselect the shovel, add and remove plants to your arsenal."
print "RIGHT CLICK: Deselect plants or the shovel"
print "THE 's' KEY: Toggle on/off the shovel"
print "NUMBERS 1-8: Select your plant #1-8\n"
print "------------------------------------------------------------------------\n"

userInput = raw_input("Hit ENTER here to start the game. -->")

#------------------------------------------------#
# ~~~~~~ DEFINING VARIABLES AND CONSTANTS ~~~~~~ #
#------------------------------------------------#

#basic initialization and definition of common constants and variables
from MatthewPechenBergPVZClasses import *
from random import randrange
import pygame
pygame.mixer.pre_init(44100, -16, 1, 512) #fixes pygame audio
pygame.init()
pygame.mixer.init()
HEIGHT = 600
WIDTH  = 800
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
TRANSPARENT_BLACK = (0,0,0,130)
TRANSPARENT_WHITE = (255,255,255,130)
HEAVY_TRANSPARENT_WHITE = (255,255,255,180)
FPS = 60
clock = pygame.time.Clock()

#loading miscellaneous images
level = pygame.image.load("MiscImages\Level.png").convert()
middleBox = pygame.image.load("MiscImages\Middle Box.png").convert_alpha()
emptyBox = pygame.image.load("MiscImages\Empty Border.png").convert_alpha()
startButton = pygame.image.load("MiscImages\startButton.png").convert_alpha()
selectBox = pygame.image.load("MiscImages\Plant Select.png").convert_alpha()
shovel = pygame.image.load("MiscImages\Shovel.png").convert_alpha()
startScreen = pygame.image.load("MiscImages\Start Screen.jpg").convert()
gameOverImage = pygame.image.load("MiscImages\GameOver.jpg").convert()

#defining some starting values
sun = [0]
plantSeedClicked = False
shovelClicked = False
runMenu = True
updateSeedSelected = False
seedSelectMusicInitialize = False
runGame = False
seedSelect = True
showStartButton = False
gameOver = False
sunTimer = 0
initializedGame = False
seedSelectMusicInitialized = False
totalColumns = 9
totalRows = 5
mouseX = 0
mouseY = 0
uselessData, uselessData, shovelImageWidth, shovelImageHeight = shovel.get_rect()
gameOverTimer = 0
notEnoughSunTimer = 0
rechargeTimer = 0

#loading plants sprite sheets
sunflowerSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Sunflower.png").convert_alpha()
twinSunflowerSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Twin Sunflower.png").convert_alpha()
peashooterSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Peashooter.png").convert_alpha()
repeaterSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Repeater.png").convert_alpha()
gatlingPeaSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Gatling Pea.png").convert_alpha()
snowPeaSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Frozen Pea.png").convert_alpha()
torchwoodSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Torchwood.png").convert_alpha()
wallNutSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Wall Nut.png").convert_alpha()
tallNutSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Tall-nut.png").convert_alpha()
spikeweedSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Spikeweed.png").convert_alpha()
spikerockSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Spikerock.png").convert_alpha()
melonPultSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Melon-pult.png").convert_alpha()
winterMelonSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Winter Melon.png").convert_alpha()
potatoMineSpriteSheet = pygame.image.load("Sprite Sheets\Plants\Potato Mine.png").convert_alpha()

#loading zombie sprite sheets
bucketZombie = pygame.image.load("Sprite Sheets\Zombies\Buckethead Zombie.png").convert_alpha()
coneZombie = pygame.image.load("Sprite Sheets\Zombies\Cone Zombie.png").convert_alpha()
zombie = pygame.image.load("Sprite Sheets\Zombies\Zombie.png").convert_alpha()
flagZombie = pygame.image.load("Sprite Sheets\Zombies\Flag Zombie.png").convert_alpha()

#zombie data lists
zombieNames = ['Flag Zombie','Zombie','Cone Zombie','Bucket Zombie']
zombieHealths = [200,200,560,1300]
zombieSpritesheets = [flagZombie,zombie,coneZombie,bucketZombie]
zombieSpritesheetRows = [5,5,5,7]

#loading projectile sprite sheets
peas = pygame.image.load("Sprite Sheets\Projectiles\Pea.png").convert_alpha()
melons = pygame.image.load("Sprite Sheets\Projectiles\Watermelon.png").convert_alpha()

#loading in plant Seed Package images
gatlingPeaSP = pygame.image.load("SeedPacks\Gatling_Pea_Seed.png").convert_alpha()
melonPultSP = pygame.image.load('SeedPacks\Melon_Pult_Seed.jpg').convert_alpha()
peashooterSP = pygame.image.load("SeedPacks\Peashooter_Seed_Image.png").convert_alpha()
potatoMineSP = pygame.image.load('SeedPacks\Potato_Mine_Seed.jpg').convert_alpha()
repeaterSP = pygame.image.load('SeedPacks\Repeater_Seed.png').convert_alpha()
snowPeaSP = pygame.image.load('SeedPacks\Snow_Pea_HD_Seed.png').convert_alpha()
spikerockSP = pygame.image.load('SeedPacks\Spikerock_Seed.png').convert_alpha()
spikeweedSP = pygame.image.load('SeedPacks\Spikeweed_Seed.jpg').convert_alpha()
sunflowerSP = pygame.image.load('SeedPacks\Sunflower_HD_Seed.png').convert_alpha()
tallNutSP = pygame.image.load('SeedPacks\Tall-Nut_Seed.jpg').convert_alpha()
torchwoodSP = pygame.image.load('SeedPacks\Torchwood_Seed.jpg').convert_alpha()
twinSunflowerSP = pygame.image.load('SeedPacks\Twin_Sunfower_Seed.png').convert_alpha()
wallNutSP = pygame.image.load('SeedPacks\Wall-Nut_Seed.jpg').convert_alpha()
WinterMelonSP = pygame.image.load('SeedPacks\Winter_HD.png').convert_alpha()

#loading in plant still-images
gatlingPeaStill = pygame.image.load("Plant Stills\Gatling Pea Still.png").convert_alpha()
melonPultStill = pygame.image.load('Plant Stills\Melon-pult Still.png').convert_alpha()
peashooterStill = pygame.image.load("Plant Stills\Peashooter Still.png").convert_alpha()
potatoMineStill = pygame.image.load('Plant Stills\Potato Mine Still.png').convert_alpha()
repeaterStill = pygame.image.load('Plant Stills\Repeater Still.png').convert_alpha()
snowPeaStill = pygame.image.load('Plant Stills\Snow Pea Still.png').convert_alpha()
spikerockStill = pygame.image.load('Plant Stills\Spikerock Still.png').convert_alpha()
spikeweedStill = pygame.image.load('Plant Stills\Spikeweed Still.png').convert_alpha()
sunflowerStill = pygame.image.load('Plant Stills\Sunflower Still.png').convert_alpha()
tallNutStill = pygame.image.load('Plant Stills\Tall-nut Still.png').convert_alpha()
torchwoodStill = pygame.image.load('Plant Stills\Torchwood Still.png').convert_alpha()
twinSunflowerStill = pygame.image.load('Plant Stills\Twin Sunflower Still.png').convert_alpha()
wallNutStill = pygame.image.load('Plant Stills\Wall-nut Still.png').convert_alpha()
WinterMelonStill = pygame.image.load('Plant Stills\Winter Melon Still.png').convert_alpha()

#plant data lists
plantFileLocations = ["Sprite Sheets\Plants\Sunflower.png","Sprite Sheets\Plants\Twin Sunflower.png","Sprite Sheets\Plants\Peashooter.png","Sprite Sheets\Plants\Repeater.png","Sprite Sheets\Plants\Gatling Pea.png","Sprite Sheets\Plants\Frozen Pea.png","Sprite Sheets\Plants\Torchwood.png","Sprite Sheets\Plants\Wall Nut.png","Sprite Sheets\Plants\Tall-nut.png","Sprite Sheets\Plants\Spikeweed.png","Sprite Sheets\Plants\Spikerock.png","Sprite Sheets\Plants\Melon-pult.png","Sprite Sheets\Plants\Winter Melon.png","Sprite Sheets\Plants\Potato Mine.png"]
plantSeedPackImages = [sunflowerSP,twinSunflowerSP,peashooterSP,repeaterSP,gatlingPeaSP,snowPeaSP,torchwoodSP,wallNutSP,tallNutSP,spikeweedSP,spikerockSP,melonPultSP,WinterMelonSP,potatoMineSP]
plantNames = ["Sunflower","Twin Sunflower","Peashooter","Repeater","Gatling Pea","Snow Pea","Torchwood","Wall-nut","Tall-nut","Spikeweed","Spikerock","Melon-pult","Winter Melon","Potato Mine"]
plantSunCosts = [50,150,100,200,450,150,175,50,125,100,250,325,500,25]
plantRechargeTimes = [5,15,5,5,15,5,10,20,20,5,10,20,20,25]
plantDescriptions = ['Sunflowers are essential for you to produce extra sun.','Twin Sunflowers give much more sun than the sunflower.','Peashooters shoot peas at attacking zombies.','Repeaters fire two peas at a time.','Gatling Peas shoot four peas at a time.','Snow Peas shoot peas that slow zombies down.','Torchwoods ignite peas that pass through them','Wall-nuts have hard shells to protect your other plants.','Tall-nuts have heavy-duty shells to protect your other plants.','Spikeweeds hurts any zombie that steps on them.','Spikerocks greatly damage zombies that walk over them.','Melon-pults do heavy damage to groups of zombies.','Winter Melons do heavy damage and slow groups of zombies.','Potato Mines explode on contact after being armed.']
plantImageStills = [sunflowerStill,twinSunflowerStill,peashooterStill,repeaterStill,gatlingPeaStill,snowPeaStill,torchwoodStill,wallNutStill,tallNutStill,spikeweedStill,spikerockStill,melonPultStill,WinterMelonStill,potatoMineStill]
plantHealths = [300,300,300,300,300,300,300,4000,8000,999999,999999,300,300,300]
plantSpriteSheets = [sunflowerSpriteSheet,twinSunflowerSpriteSheet,peashooterSpriteSheet,repeaterSpriteSheet,gatlingPeaSpriteSheet,snowPeaSpriteSheet,torchwoodSpriteSheet,wallNutSpriteSheet,tallNutSpriteSheet,spikeweedSpriteSheet,spikerockSpriteSheet,melonPultSpriteSheet,winterMelonSpriteSheet,potatoMineSpriteSheet]
plantSpriteSheetColumns = [4,4,4,4,4,4,4,2,2,4,4,4,4,4]
plantSpriteSheetRows = [3,3,2,2,1,2,1,3,3,2,2,2,2,3]
plantFPSs = [4,4,4,4,4,4,8,1,1,3,3,4,4,4]
plantTargetability = [True,True,True,True,True,True,True,True,True,False,False,True,True,True]

#other plant seed packages data
selectedPlants = []
totalPlants = 14
latestPlantPicked = -1
basicExample = ["Sunflower","Twin Sunflower","Peashooter","Repeater","Snow Pea","Wall-nut","Winter Melon","Potato Mine"]

#creating transparent grey rectangles for different things
backgroundGreyEffect = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
backgroundGreyEffect.fill(TRANSPARENT_BLACK)
seedGreyEffect = pygame.Surface((64,88),pygame.SRCALPHA)
seedGreyEffect.fill(TRANSPARENT_BLACK)
sideTileHoverEffect = pygame.Surface((80,80), pygame.SRCALPHA)
sideTileHoverEffect.fill(TRANSPARENT_WHITE)
mainTileHoverEffect = pygame.Surface((80,80), pygame.SRCALPHA)
mainTileHoverEffect.fill(HEAVY_TRANSPARENT_WHITE)

#defining wave-related values
wave = 0
zombieDifficulty = 0
waveInterval = 45
newWave = False
initialWaveDisplayTime = time.time()-3
waveTextWidth = 0
waveTextHeight = 0
initialSpawningTime = 99999999999999999999999999
zombieSpacing = 0
zombieSpacingLowerLimit = 600
zombieSpacingUpperLimit = 900

#creating sun font and text
sunFont = pygame.font.Font("Fonts\SERIO.ttf",14)
sunFontLarge = pygame.font.Font("Fonts\SERIO.ttf",24)
sunText = sunFont.render(str(sun[0]),1,WHITE)
needSunText = sunFont.render("You need more sun to buy that plant!",1,WHITE)
uselessData, uselessData, needSunTextWidth, needSunTextHeight = needSunText.get_rect()

#creating description and general font and text
basicFontMini = pygame.font.Font("Fonts\Burbank Big Condensed Light.ttf",30)
descriptionText = basicFontMini.render("Description: "+str(plantDescriptions[latestPlantPicked]),1,WHITE)
exampleBuildText = basicFontMini.render("Click here for an example loadout",1,WHITE)
helpText = basicFontMini.render("Click the seeds up here to remove them",1,WHITE)
hintText = basicFontMini.render("Hint: You must have at least one sunflower plant to succeed!",1,WHITE)
rechargeText = sunFontLarge.render("You must wait for the plant to recharge",1,WHITE)
uselessData, uselessData, rechargeTextWidth, rechargeTextHeight = rechargeText.get_rect()

#creating wave and score font, text, and some text dimensions
waveFont = pygame.font.Font("Fonts\SERIO.ttf",25)
waveText = waveFont.render("Wave #"+str(wave)+": a HUGE wave of zombies is approaching",1,RED)
scoreText = sunFont.render("Wave #"+str(wave),1,RED)
uselessData, uselessData, scoreTextWidth, scoreTextHeight = scoreText.get_rect()

#defining sound effects
waveSound = pygame.mixer.Sound('Sounds\The_Zombies..._Are_Coming!.ogg')
waveSound.set_volume(0.35)
shovelSound = pygame.mixer.Sound('Sounds\Shovel.ogg')
shovelSound.set_volume(0.25)
screamSound = pygame.mixer.Sound('Sounds\Scream.ogg')
screamSound.set_volume(0.25)
gameOverSound = pygame.mixer.Sound('Sounds\Plants VS Zombies Music - Game Over (Chomp Chomp).wav')
gameOverSound.set_volume(0.25)

#loading and setting up music
musicFileLocations = ['Music\BrainiacManiac.ogg','Music\CerebrawlPvZ1.ogg','Music\FrontLawnTheme.ogg','Music\GrasswalkPvZ1.ogg','Music\GrazeTheRoof.ogg','Music\LoonboonPvZ1.ogg','Music\MoongrainsPvZ1.ogg','Music\RigorMormist.ogg','Music\UltimateBattlePvZ1.ogg','Music\WateryGraves.ogg','Music\ZenGardenPvZ1.ogg','Music\ZombiesOnYourLawnPvZ1.ogg','Music\ZombieTime.ogg']
END_SONG = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(END_SONG)
recentSongs = []

#Some class definitions
defenders = Defenders()
attackers = Attackers()
miscAnimations = RunningAnimations()
suns = Suns()

#---------------------------------#
# ~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~ #
#---------------------------------#

def redrawGameWindow():
    gameWindow.fill(BLACK)
    if runMenu:
        displayMainMenuAspects()
    elif gameOver:
        displayGameOverElements()
    else:
        gameWindow.blit(level,(0,0))
        drawSprites()
        displayPlacementIndicators()
        drawSunText()
        drawSeedSelectMenuAspects()
        drawSelectedPlants()
        drawSeedRecharges()
        displayPlantSelectedImage()
        displayShovel()
        displayPlantStill()
        displayWaveText()
    pygame.display.update()

def drawSelectedPlants(): #draws the plants chosen by the user
    for i in range(len(selectedPlants)):
        gameWindow.blit(plantSeedPackImages[plantNames.index(selectedPlants[i])],(85+i*64,0))

def drawEmptyBoxes():
    for i in range(8):
        gameWindow.blit(emptyBox,(85+i*64,0))

def drawPlantSeeds(): #draws list of plants in seed select phase
    for i in range(totalPlants):
        gameWindow.blit(plantSeedPackImages[i],(176+((i%7)*64),230+88*(i/7)))
        if plantNames[i] in selectedPlants:
            gameWindow.blit(seedGreyEffect,((176+((i%7)*64),230+88*(i/7))))

def drawDescription(): #descriptions for clicked seeds
    if latestPlantPicked != -1:
        descriptionText = basicFontMini.render("Description: "+str(plantDescriptions[latestPlantPicked]),1,WHITE)
        unimportantData, unimportantData, descriptionWidth, descriptionHeight = descriptionText.get_rect()
        gameWindow.blit(descriptionText,(400-(descriptionWidth/2),206-(descriptionHeight/2)))

def drawSeedSelectMenuAspects():
    if seedSelect:
        displayShovelStill()
        gameWindow.blit(backgroundGreyEffect,(0,0))
        gameWindow.blit(middleBox,(0,0))
        drawEmptyBoxes()
        drawPlantSeeds()
        drawDescription()
        if showStartButton:
            gameWindow.blit(startButton,(275,502))
        else:
            gameWindow.blit(hintText,(55,539))
            
        #displaying general/useful text
        gameWindow.blit(exampleBuildText,(550,539))
        gameWindow.blit(helpText,(88,90))
        

def displayPlantStill(): #still images when a seed is selected
    if plantSeedClicked:
        gameWindow.blit(selectedImage,(mouseX-(selectedImageWidth/2),mouseY-10-(selectedImageHeight/2)))

def displayShovel():
    if not seedSelect:
        if shovelClicked:
            gameWindow.blit(shovel,(mouseX-shovelImageWidth/2,mouseY+43-shovelImageHeight))
        else:
            gameWindow.blit(shovel,(616,0))

def displayShovelStill(): #still shovel image when it is selected
    gameWindow.blit(shovel,(616,0))

def displayPlacementIndicators(): #shows where a plant will be placed
    if (plantSeedClicked or shovelClicked) and (mouseX - 40) >= 0 and (mouseX - 40) < 720 and (mouseY - 180) >= 0 and (mouseY - 180) < 400:
        for c in range(totalColumns):
            for r in range(totalRows):
                if ((mouseX - 40) >= 80*c and (mouseX - 40) < 80*(c+1)) or ((mouseY - 180) >= 80*r and (mouseY - 180) < 80*(r+1)):
                    gameWindow.blit(sideTileHoverEffect,(40+c*80,180+r*80))
                if ((mouseX - 40) >= 80*c and (mouseX - 40) < 80*(c+1)) and ((mouseY - 180) >= 80*r and (mouseY - 180) < 80*(r+1)):
                    gameWindow.blit(mainTileHoverEffect,(40+c*80,180+r*80))

def displayPlantSelectedImage(): #small border around selected seed
    if plantSeedClicked:
        gameWindow.blit(selectBox,(seedPosition*64+85,0))

def drawSprites():        
    if not seedSelect:
        defenders.update(attackers,miscAnimations,suns,gameWindow)
        attackers.update(defenders,miscAnimations,gameWindow)
        miscAnimations.update(defenders,attackers,gameWindow)
        suns.update(gameWindow)

def displayWaveText():
    if not seedSelect:
        if time.time() - initialWaveDisplayTime <= 3:
            gameWindow.blit(waveText,(400-(waveTextWidth/2),300-(waveTextHeight/2)))
        gameWindow.blit(scoreText,(750-(scoreTextWidth/2),60-(scoreTextHeight/2)))

def drawSunText():
    sunText = sunFont.render(str(sun[0]),1,WHITE)
    if notEnoughSunTimer != 0:
        if time.time() - notEnoughSunTimer < 0.1:
            sunText = sunFont.render(str(sun[0]),1,RED)
        elif time.time() - notEnoughSunTimer < 0.2:
            sunText = sunFont.render(str(sun[0]),1,WHITE)
        elif time.time() - notEnoughSunTimer < 0.3:
            sunText = sunFont.render(str(sun[0]),1,RED)
        elif time.time() - notEnoughSunTimer < 0.4:
            sunText = sunFont.render(str(sun[0]),4,WHITE)
    if time.time() - notEnoughSunTimer < 0.8:
        gameWindow.blit(needSunText,(400-(needSunTextWidth/2),100-(needSunTextHeight/2)))
    uselessData, uselessData, sunTextWidth, sunTextHeight = sunText.get_rect()
    gameWindow.blit(sunText,(41-(sunTextWidth/2),87-(sunTextHeight/2)))

def drawSeedRecharges(): #grey effect to indicate plant seed recharge times
    if not seedSelect:
        for i in range(8):
            plantIndex = plantNames.index(selectedPlants[i])
            if time.time()-plantLatestUses[plantIndex] > plantRechargeTimes[plantIndex]:
                fractionRemaining = 88
            else:
                fractionRemaining = 88.*(time.time()-plantLatestUses[plantIndex])/(plantRechargeTimes[plantIndex])        
            gameWindow.blit(seedGreyEffect,(85+i*64,-1*fractionRemaining))
        if time.time() - rechargeTimer < 1 and rechargeTimer != 0:
            gameWindow.blit(rechargeText,(400-(rechargeTextWidth/2),150 - (rechargeTextHeight/2)))

def displayMainMenuAspects():
    gameWindow.blit(startScreen,(0,0))
        
def initializeMainMusic(randomNumber):
    pygame.mixer.music.load(musicFileLocations[randomNumber])
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(END_SONG)

def displayGameOverElements():
    gameWindow.blit(gameOverImage,(0,0))
    gameWindow.blit(finalWaveText,(400-(finalWaveTextWidth/2),30))
    
#------------------------------------#
# ~~~~~~~~~~ MAIN PROGRAM ~~~~~~~~~~ #
#------------------------------------#

#start main menu music
pygame.mixer.music.load('Music\MainMenuPvZ1.ogg')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play()

while runMenu:

    redrawGameWindow()
    clock.tick(FPS)
    
    #get mouse position data
    mouse = pygame.mouse.get_pos()
    mouseX, mouseY = mouse

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouseX >= 240 and mouseX <=552 and mouseY >= 500 and mouseY <= 585: #start the game
            runGame = True
            runMenu = False
                
    while runGame:

        redrawGameWindow()
        clock.tick(FPS)
        
        while seedSelect:
            
            redrawGameWindow()
            clock.tick(FPS)

            #play seed select music
            if not seedSelectMusicInitialized:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('Music\ChooseYourSeedsPvZ1.ogg')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                seedSelectMusicInitialized = True

            #get mouse position data
            mouse = pygame.mouse.get_pos()
            mouseX, mouseY = mouse
            
            for event in pygame.event.get():            
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    #allow plants to be added or removed via the grid of plants
                    if (mouseX - 176) <= 448 and mouseX >= 176 and (mouseY - 230) <= 176 and mouseY >= 230:

                        #calculate seed index in main lists
                        seedColumn = (mouseX - 176)/64
                        seedRow = (mouseY - 230)/88
                        if seedRow >= 2:
                            seedRow = 1
                        if seedColumn >= 7:
                            seedColumn = 6
                        newPlantIndex = seedColumn+7*seedRow

                        #adding or removing it
                        latestPlantPicked = newPlantIndex
                        if plantNames[newPlantIndex] not in selectedPlants:
                            if len(selectedPlants) < 8:
                                selectedPlants.append(plantNames[newPlantIndex])
                        else:
                            selectedPlants.remove(plantNames[newPlantIndex])

                    #Remove seed from clicking on selected plants  
                    elif mouseX <= 597 and mouseX > 85 and mouseY <= 88:
                        seedPosition = (mouseX - 85)/64
                        if seedPosition == 8:
                            seedPosition = 7
                        if seedPosition < len(selectedPlants):
                            latestPlantPicked = plantNames.index(selectedPlants[seedPosition])
                            selectedPlants.pop(seedPosition)

                    #let users click start button
                    elif showStartButton and mouseX > 275 and mouseX < 524 and mouseY >= 502 and mouseY < 571:
                        seedSelect = False
                        showStartButton = False

                    #register default plant loadout selection
                    elif mouseX >= 530 and mouseY >= 519:
                        selectedPlants = list(basicExample)

                #exit seed select to start game
                if len(selectedPlants) == 8:
                    showStartButton = True
                else:
                    showStartButton = False

            startingTime = time.time()

        #initialize timers and other variables
        if not initializedGame:
            initializedGame = True
            sunTimer = time.time()
            plantLatestUses = [time.time()]*14
            pygame.mixer.music.stop()
            recentSongs.append(randrange(0,13))
            initializeMainMusic(recentSongs[0])
            
        #get mouse position data
        mouse = pygame.mouse.get_pos()
        mouseX, mouseY = mouse

        for event in pygame.event.get():

            #play new songs randomly when a song ends
            if event.type == END_SONG:
                if len(recentSongs) > 7:
                    recentSongs.pop(0)
                musicFound = False
                while not musicFound:
                    newNum = randrange(0,13)
                    if newNum not in recentSongs:
                        recentSongs.append(newNum)
                        musicFound = True
                initializeMainMusic(newNum)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    tileColumn = (mouseX-40)/80
                    tileRow = (mouseY-180)/80
                    suns.checkSunCollection(mouseX, mouseY, sun)

                    #quit button code
                    if mouseX >= 701 and mouseX <= 800 and mouseY >= 0 and mouseY <= 35:
                        runGame = False

                    #registering the selection of plants from clicking a selected plant
                    elif mouseX <= 597 and mouseX > 85 and mouseY <= 88:
                        seedPosition = (mouseX - 85)/64
                        if seedPosition == 8:
                            seedPosition = 7
                        if time.time() - plantLatestUses[plantNames.index(selectedPlants[seedPosition])] > plantRechargeTimes[plantNames.index(selectedPlants[seedPosition])]: #let the click go through if the plant is recharged
                            plantSeedClicked = True
                            shovelClicked = False
                            selectedImage = plantImageStills[plantNames.index(selectedPlants[seedPosition])]
                            uselessData, uselessData, selectedImageWidth,selectedImageHeight = selectedImage.get_rect()
                        else:
                            plantSeedClicked = False
                            rechargeTimer = time.time()

                    #registering clicking on shovel
                    elif mouseX >= 616 and mouseX <= 700 and mouseY >= 0 and mouseY <= 83 and not shovelClicked:
                        shovelClicked = True
                        plantSeedClicked = False
                        shovelSound.play()

                    
                    elif (plantSeedClicked or shovelClicked) and mouseX >= 40 and mouseX < 760 and mouseY >= 180 and mouseY < 580:
                        if plantSeedClicked: #placing the plant on the selected tile if there is space
                            plantSeedClicked = False
                            newPlantIndex = plantNames.index(selectedPlants[seedPosition])
                            if defenders.tileAvailable(tileColumn,tileRow,plantNames[newPlantIndex]):
                                if sun[0] >= plantSunCosts[newPlantIndex]:
                                    sun[0] = sun[0] - plantSunCosts[newPlantIndex]
                                    plantLatestUses[newPlantIndex] = time.time()
                                    defenders.append(Plant(plantNames[newPlantIndex],plantHealths[newPlantIndex],plantRechargeTimes[newPlantIndex],tileColumn,tileRow,plantSpriteSheets[newPlantIndex],plantSpriteSheetColumns[newPlantIndex],plantSpriteSheetRows[newPlantIndex],plantFPSs[newPlantIndex],plantTargetability[newPlantIndex],plantFileLocations[newPlantIndex]))
                                else:
                                    notEnoughSunTimer = time.time()
                        elif shovelClicked: #removes the plant on the tile clicked if there is one
                            shovelClicked = False
                            if not defenders.tileAvailable(tileColumn, tileRow):
                                for plant in defenders.plants:
                                    if plant.row == tileRow and plant.col == tileColumn:
                                        plant.health = 0
                                        shovelSound.play()
                    else:
                        shovelClicked, plantSeedClicked = False, False
                if event.button == 3:
                    shovelClicked, plantSeedClicked = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: #toggle shovel with the 's' key
                    plantSeedClicked = False
                    shovelSound.play()
                    if not shovelClicked:
                        shovelClicked = True
                    else:
                        shovelClicked = False

                #allows plant seeds to be selected with keys 1 through 8
                if event.key == pygame.K_1:
                    seedPosition = 0
                    updateSeedSelected = True
                elif event.key == pygame.K_2:
                    seedPosition = 1
                    updateSeedSelected = True
                elif event.key == pygame.K_3:
                    seedPosition = 2
                    updateSeedSelected = True
                elif event.key == pygame.K_4:
                    seedPosition = 3
                    updateSeedSelected = True
                elif event.key == pygame.K_5:
                    seedPosition = 4
                    updateSeedSelected = True
                elif event.key == pygame.K_6:
                    seedPosition = 5
                    updateSeedSelected = True
                elif event.key == pygame.K_7:
                    seedPosition = 6
                    updateSeedSelected = True
                elif event.key == pygame.K_8:
                    seedPosition = 7
                    updateSeedSelected = True
                if updateSeedSelected:
                    if time.time() - plantLatestUses[plantNames.index(selectedPlants[seedPosition])] > plantRechargeTimes[plantNames.index(selectedPlants[seedPosition])]:
                        selectedImage = plantImageStills[plantNames.index(selectedPlants[seedPosition])]
                        uselessData, uselessData, selectedImageWidth,selectedImageHeight = selectedImage.get_rect()
                        shovelClicked = False
                        plantSeedClicked = True
                        updateSeedSelected = False
                    else:
                        plantSeedClicked = False
                        updateSeedSelected = False
                        rechargeTimer = time.time()
                
        #spawn random suns:
        if time.time() - sunTimer > 10:
            skySunX = randrange(100,701)
            skySunY = randrange(100,501)
            suns.append(Sun(skySunX,skySunY))
            sunTimer = sunTimer + 10
                    
        #check for new wave
        newWave = False
        if time.time() - startingTime >= waveInterval:
            initialWaveDisplayTime = time.time()
            startingTime = time.time()
            wave = wave + 1
            scoreText = sunFont.render("Wave #"+str(wave),1,RED)
            uselessData, uselessData, scoreTextWidth, scoreTextHeight = scoreText.get_rect()
            waveSound.play()
            newWave = True

            #update wave text and determine difficulty
            if wave%3 != 0:
                waveText = waveFont.render("Wave #"+str(wave)+": a big wave of zombies is approaching!",1,RED)
                zombieDifficulty = int((wave)**1.3)
            else:
                waveText = waveFont.render("Wave #"+str(wave)+": a HUGE wave of zombies is approaching!!!",1,RED)
                zombieDifficulty = int((wave)**1.4)

            #determining what zombies get spawned and in what order
            uselessData, uselessData, waveTextWidth, waveTextHeight = waveText.get_rect()
            zombiesToSpawn = [0]
            zombieSpawnLanes = [randrange(0,5)]
            initialSpawningTime = time.time()
            spawnedZombies = 0
            zombieSpawnDuration = randrange(zombieSpacingLowerLimit,zombieSpacingUpperLimit)/float(100)
            while zombieDifficulty > 0:
                if wave <= 3:
                    newSpawn = randrange(1,3)
                else:
                    newSpawn = randrange(1,4)
                if zombieDifficulty >= newSpawn:
                    zombieDifficulty = zombieDifficulty - newSpawn
                    zombiesToSpawn.append(newSpawn)
                    zombieSpawnLanes.append(randrange(0,5))

            #increasing values as the game progresses
            waveInterval = 45 + wave**0.9
            zombieSpacingLowerLimit = 600 + 10*wave
            zombieSpacingUpperLimit = 900 + 10*wave
            zombieSpacing = zombieSpawnDuration/(len(zombiesToSpawn))

        #spawning in the new zombies
        if time.time() - initialSpawningTime > zombieSpacing and spawnedZombies < len(zombiesToSpawn):
            attackers.append(Zombie(zombieNames[zombiesToSpawn[spawnedZombies]],zombieHealths[zombiesToSpawn[spawnedZombies]],zombieSpawnLanes[spawnedZombies],zombiesToSpawn[spawnedZombies],zombieSpritesheetRows[zombiesToSpawn[spawnedZombies]],840,zombiesToSpawn[spawnedZombies]))
            initialSpawningTime = initialSpawningTime + zombieSpacing
            spawnedZombies = spawnedZombies + 1

        #checking for game over
        if attackers.checkWinners():
            gameOver = True
            runGame = False
            gameOverTimer = time.time()
            pygame.mixer.music.stop()
            gameOverSound.play()
            screamSound.play()
            finalWaveText = waveFont.render("You reached wave #"+str(wave),1,RED)
            uselessData, uselessData, finalWaveTextWidth, finalWaveTextHeight = finalWaveText.get_rect()

        while gameOver:
            
            redrawGameWindow()
            clock.tick(FPS)

            #keep screen up for a few seconds before it shuts down
            if time.time() - gameOverTimer > 6:
                gameOver = False

            pygame.event.clear()
            
#---------------------------------------#
pygame.quit()
