from cmu_graphics import *
import math
import random
'''FEATURES
full 360 degree camera scrolling
5 different powerups: health, ammo, infinite ammo, sword, and rayGun
(command f "HOTKEYS" to find hotkeys to spawn in powerups)
i = infinite ammo
r = raygun
t = sword
c = new level
p = die
0 = bosslevel


bossLevel at level10 press '0' to activate bosslevel
door with loading screen and boss spawn

Added rayGun powerup
used unit vectors to calculate direction for bullets and zombies

implemented countdown for round start
'No Ammo' messages when out of ammo
implemented health bars and hit markers for zombies
implemented running animation for player

used sprites for:
- zombies
-hot bar in bottom left
-powerups
-sword 
-player
-tiles


OOP:
made 4 different classes:
player class
zombie class
bullet class
Loot class
'''

def onAppStart(app):
    app.bestScore = 0 
    app.startScreen = True
    app.endScreen = False
    app.stepsPerSecond = 30
    app.images = {'smallZombie':'/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Enemies/Zombie_Small/small_zombie.png',
                 'bigZombie':'/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Enemies/Zombie_Big/big_zombie.png',
                 'dirtTile':'/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Tiles/dirt_tile.png',
                 'grassTile':'/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Tiles/grass_tile.png',
                 'normalZombie':'/Users/connorchoe/Desktop/normalZombie1.png',
                 'sword':'/Users/connorchoe/Desktop/sword.png',
                 'gun':'/Users/connorchoe/Downloads/gun.png',
                 'rayGun':'/Users/connorchoe/Downloads/rayGun.png',
                 'health':'/Users/connorchoe/Desktop/health.png',
                 'ammo':'/Users/connorchoe/Desktop/bullet.png',
                 'infiniteAmmo':'/Users/connorchoe/Downloads/infiniteAmmo.png',
                 'pause':'cmu://1073008/43666582/pause.png'
    }
    app.steps = 0
    app.width = 600
    app.height = 600
    
    app.rows = 50
    app.cols = 50
    app.boardTop = 0
    app.boardLeft = 0
    app.boardWidth = 1200
    app.boardHeight = 1200
    app.cellBorderWidth = 2
    app.tileSize = app.boardWidth/app.cols
    app.player = Player(app.boardWidth/2, app.boardHeight/2, app)
    app.screenLeft = app.player.x - app.width/2. #player is always centered on the canvas
    app.screenTop = app.player.y - app.height/2. #screen size is 600
    restart(app)
    
def reset(app):
    app.animation = False
    app.zombies = []
    app.counter = 3
    app.speed = 7
    spawnZombies(app)
    app.bullets = []
    app.lootSpawnTimer = 0 
    app.messageTimer = 0 
    #powerup
    app.weaponAnimationCounter = 0
    app.rayGun = False
    app.target = (None, None)

    
def restart(app):
    app.points = 0
    app.totalShots = 0 
    app.shotsHit = 0
    app.loot = []
    app.level = 1
    app.player.health = 100
    app.player.ammo = 50
    #bossLevel
    app.opacityLevel = 100
    app.bossLevel = False
    app.loadingScreen = False
    app.boss = False
    app.powerupTimer = 0
    app.startTimer = False
    reset(app)
    
    
def redrawAll(app):
    if app.startScreen:
        drawStartScreen(app)
        return
    elif app.endScreen:
        drawEndScreen(app)
        return

    drawRect(0, 0, 1200, 1200, fill = 'black')
    drawBoard(app)
    app.player.draw(app)
    for zombie in app.zombies:
        zombie.draw(app)
    for bullet in app.bullets:
        bullet.draw(app)
    drawLabel(f'Round {app.level}', app.width/2, 20, 
              size = 40, bold = True, fill = 'white')
    drawLabel(f'Zombies Left:{len(app.zombies)}', app.width - 100, 20,
              size = 20, bold = True, fill = 'red')
    drawUI(app)
    drawWeapon(app)
    for loot in app.loot:
        loot.draw(app)
    if app.player.outOfAmmo(app) and app.messageTimer < 30:
        drawLabel('Out of Ammo!', app.width/2, app.height/2, size = 20)
    if app.animation:
        drawAnimation(app)
    if app.level == 10 and not app.bossLevel:
        doorX = app.boardWidth - app.tileSize *2
        drawDoor(app, doorX)
    if app.loadingScreen:
        drawLoadingScreen(app)
        doorX = 0 
        drawDoor(app, doorX)
    if app.zombies == [] and app.level != 10:
        drawCounter(app)
    elif app.zombies == [] and app.bossLevel:
        drawCounter(app)
        
def drawWeapon(app):
    if app.player.weapon =='sword':
        image = app.images['sword']
        weaponWidth = 80
        weaponHeight= 80
        xOffSet = 10
        yOffSet = 45
        x =  app.player.x + xOffSet - app.screenLeft
        y = app.player.y - yOffSet - app.screenTop
        drawImage(image, x, y,
                  width = weaponWidth, height = weaponHeight)

def drawLoadingScreen(app):
    drawRect(0, 0,app.width, app.height, opacity = app.opacityLevel)
    
        
def startBossLevel(app):
    app.player.freeze = False

def drawDoor(app, doorX):
    doorSize = 50
    doorY = app.boardHeight/2
    door = '/Users/connorchoe/Desktop/dungeonDoor.png'
    drawImage(door, doorX - app.screenLeft, doorY - app.screenTop, width = doorSize, height = doorSize)

def drawAnimation(app):
    if app.player.weapon == 'sword':
        x = app.player.x - app.screenLeft
        y = app.player.y - app.screenTop
        drawCircle(x, y, 80, fill = 'white', opacity = 50)
        
    elif app.player.powerups == 'infiniteAmmo':
        drawRect(0, 0, app.width, app.height,
                fill = gradient('white', 'green'), opacity = 20)


def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height)
    title = '/Users/connorchoe/Desktop/survive112Title.png'
    drawImage(title, app.width/2, app.height/3, align = 'center', width = 400, height = 300)
   
    drawLabel("'WASD' to move", app.width/2, app.height*2/3, fill = 'red')
    drawLabel("'MOUSE1' to attack", app.width/2, app.height*2/3 + 20, fill = 'red')

    if app.steps%30 != 0:
        drawLabel("Press 'space' to Start", app.width/2, app.height/2,
                  size = 20, fill = 'red')
                  
def drawEndScreen(app):
    drawRect(0, 0, app.width, app.height)
    drawLabel("Game Over!", app.width/2, app.height/3, size = 40, 
              fill = 'red', bold = True)
    if app.steps%30 != 0:
        drawLabel("Press 'space'to Play Again", app.width/2, app.height/2, size = 20, 
                  fill = 'red')
    try:
        accuracy = (app.shotsHit * 100//app.totalShots)
    except:
        accuracy = 0
    drawLabel('Score',app.width/4, app.height*2/3 -40, size = 40, fill = 'red')
    Button(app.width/4, app.height*2/3, 100, 50, str(app.points)).draw()
    drawLabel('Accuracy',app.width*3/4, app.height*2/3 -40, size = 40, fill = 'red')
    Button(app.width*3/4, app.height*2/3, 100, 50, f'{accuracy}%').draw()
    drawLabel('Best Score', app.width/2, app.height*7/8 - 40, size = 40, fill = 'red')
    Button(app.width/2, app.height*7/8, 100, 50, str(app.bestScore)).draw()

    
                  
def drawNoAmmoMessage(app):
    drawLabel('No More Ammo!', app.width/2, app.height/2, size = 20)
    
def drawUI(app):
    if app.player.weapon == 'gun':
        ammo = app.player.ammo if app.player.ammo > 0 else 0
        drawLabel(f'{ammo}', app.width - 40, app.height - 20, size = 20, fill = 'white')
    imageSize = 50
    image = app.images[app.player.weapon]
    # drawRect(0, app.height -imageSize, imageSize, imageSize)
    drawImage(image, 0, app.height -imageSize, width = imageSize, 
              height = imageSize, border = 'black', borderWidth = 5)
    drawLabel(f'Score:{app.points}', 20, 20, size= 20, fill = 'red', 
              align = 'left', bold = True)
    
def spawnZombies(app):
    if app.level == 10 and app.bossLevel:
        app.zombies = [(Zombie(app.width*3/4, app.height/2, 3))]
        return
    elif app.level == 10:
        return
    count = 10 + 5 * (app.level-1)
    for zombie in range(count):
        edge = random.randint(0,2)
        typeIndex = random.randint(0, 2)
        if edge == 0: # top edge
            x = random.randint(app.boardLeft, app.boardLeft + app.boardHeight)
            y = app.boardTop + 10
        elif edge == 1: # right edge
            x = app.boardLeft + app.boardWidth - 10
            y = random.randint(app.boardTop, app.boardTop + app.boardHeight)
        elif edge == 2: #bottom edge
            x = random.randint(app.boardLeft, app.boardLeft + app.boardHeight)
            y = app.boardTop + app.boardHeight -10
            
        app.zombies.append(Zombie(x, y, typeIndex))

def moveTowardsPlayer(app):
    for zombie in app.zombies:
        directionX = (app.player.x - zombie.x)
        directionY = (app.player.y - zombie.y)
        magnitude = (directionX**2 + directionY**2)**0.5
        unitDirection = (directionX/magnitude, directionY/magnitude)
        zombie.move(unitDirection[0], unitDirection[1], app)
    
    

class Player:
    def __init__(self, x, y, app):
        self.x = x
        self.y = y
        self.health = 100
        self.radius = 10
        self.imageUrls = ['/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run0.png', 
                          '/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run1.png',
                          '/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run2.png',
                          '/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run3.png',
                          '/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run4.png',
                          '/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run5.png']
        self.idleImage = '/Users/connorchoe/Downloads/PostApocalypse_AssetPack_v1.1.2/Character/Main/Run/character_side_run0.png'
        self.imageIndex = 0
        self.weapons = ['gun', 'sword', 'rayGun']
        self.powerups = None
        self.weaponIndex = 0 
        self.weapon = self.weapons[self.weaponIndex]
        self.ammo = 50
        self.freeze = False
        self.moving = False
        
    def draw(self, app):
        # drawCircle(self.x - app.screenLeft,  self.y - app.screenTop, self.radius, fill = 'blue')
        drawImage(self.imageUrls[self.imageIndex], self.x - app.screenLeft,
                     self.y - app.screenTop, width = 30, height =30, align = 'center')
        drawLabel(f'Health:{self.health}', 110 , app.height - 20, size = 20, 
                  bold = True, fill = 'red')
        
    def move(self, dx, dy, app):
        if not self.freeze:
            self.x += dx
            self.y += dy
    
    def die(self, app):
        if self.health <= 0:
            app.endScreen = True
            if app.points > app.bestScore:
                app.bestScore = app.points
                
        
    def outOfAmmo(self, app):
        if self.ammo < 0:
            return True
        else:
            return False
        
    def playerInsideDoor(self, app):
        doorX = app.boardWidth - 50
        doorY = app.boardHeight/2
        doorSize = 50
        if (doorX < self.x - 10 < doorX + doorSize and #make sure player is completely covered
            doorY < self.y < doorY + doorSize):
                return True
        return False
 
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2)**0.5
    
        
def onStep(app): 
    app.steps += 1
    if not app.startScreen:
        app.lootSpawnTimer += 1
    app.player.die(app)
    handleBossLevel(app)
    playerAnimation(app)

    recenterCamera(app)
    moveZombies(app)
    handleBullets(app)
    powerUpTimer(app)
    handleLoot(app)
    levelSetting(app)
    noAmmoMessage(app)
    handleWeaponAnimations(app)
    if app.rayGun:
        updateRayGun(app)
    for zombie in app.zombies:
        if zombie.isHit:
            handleHitMarkers(app, zombie)
    
def handleHitMarkers(app, zombie):
    zombie.hitMarkerTimer += 1
    if zombie.hitMarkerTimer >= 10:
        zombie.hitMarkerTimer = 0 
        zombie.isHit = False

def updateRayGun(app):
    app.bullets = []
    for i in range(20):
        targetX, targetY = app.target
        app.bullets.append(Bullet(app.player.x, app.player.y, targetX, targetY, app, i))
    
        

def handleBossLevel(app):
    if app.player.playerInsideDoor(app):
        app.loadingScreen = True
    if app.loadingScreen:
        app.player.freeze = True
        app.player.x = app.boardLeft + 15
    if app.loadingScreen and app.steps % 15 == 0 and app.opacityLevel >0:
        app.opacityLevel -= 5
    if app.opacityLevel < 50:
        app.loadingScreen = False
        app.bossLevel = True
        startBossLevel(app)
    if app.bossLevel and app.boss == False:
        spawnZombies(app)
        app.boss = True
def playerAnimation(app):
    if app.steps % 10 == 0:
        app.player.imageIndex = (app.player.imageIndex +1) % len(app.player.imageUrls)
        
def recenterCamera(app):
    app.screenLeft = app.player.x - app.width/2
    app.screenTop = app.player.y - app.height/2
def moveZombies(app):
    if app.startScreen:
        return
    if app.steps % 2== 0 :
        moveTowardsPlayer(app)
    for zombie in app.zombies:
        if app.steps % 15 == 0:
            zombie.isAttacking(app.player)
def handleBullets(app):
    for bullet in app.bullets:
        if bullet.type == 'gun':
            bullet.move()
    #AI gave me this line to make my game run smoother
    app.bullets = [b for b in app.bullets if not isOffScreen(app, b)] 
    for bullet in app.bullets:
        for zombie in app.zombies:
            if bullet.isHittingZombie(zombie) and bullet in app.bullets:
                app.points += 40
                zombie.isHit = True
                if app.player.weapon == 'gun':
                    app.bullets.remove(bullet)
                    app.shotsHit += 1
              
    for zombie in app.zombies:
        if zombie.health <= 0:
            app.zombies.remove(zombie)
def powerUpTimer(app):          
    if app.startTimer: #reset after powerup
        app.powerupTimer += 1
        if app.powerupTimer >= 250:
            app.player.ammo = 50
            app.rayGun = False
            app.player.weapon = 'gun'
            app.bullets = []
            app.player.powerups = None
            app.powerupTimer = 0
            app.startTimer = False

def handleLoot(app):
    #adding loot
    if app.lootSpawnTimer > 300 and app.level != 10: # change to 300
        spawnLoot(app)
        app.lootSpawnTimer = 0
    elif app.lootSpawnTimer > 300 and app.bossLevel:
        spawnLoot(app)
        app.lootSpawnTimer = 0 
    #removing loot
    for loot in app.loot:
        if loot.isPickedUp(app):
            app.loot.remove(loot)
            activateLoot(app, loot)
def levelSetting(app):
    if app.zombies == [] and app.steps%30 == 0 and app.level != 10:
        app.counter -=1
    elif app.zombies == [] and app.bossLevel and app.steps%30 == 0:
        app.counter -= 1
    if app.counter < 0:
        app.level += 1
        reset(app)
        
def noAmmoMessage(app):
    if app.player.outOfAmmo(app):
        app.messageTimer += 1
        
def handleWeaponAnimations(app):
    if app.animation and app.player.weapon == 'sword':
        app.weaponAnimationCounter += 1
        if app.weaponAnimationCounter > 5:
            app.animation = False
            app.weaponAnimationCounter = 0 

def drawCounter(app):
    drawLabel(f'Next Round Starts in {app.counter}', app.width/2, app.height/2,
              size = 40, bold = True, fill ='red')

    
#zombie class
class Zombie:
    def __init__(self, x, y, typeIndex):
        self.x = x
        self.y = y
        self.types = ['fast', 'normal', 'tank', 'boss']
        self.type = self.types[typeIndex]
        self.hitMarkerTimer = 0
        self.isHit = False
        if typeIndex == 0:
            self.radius =12
            self.health = 50
            self.fullHealth = 50
            self.speed = 10
        elif typeIndex == 1:
            self.radius = 12
            self.health = 110
            self.fullHealth = 110
            self.speed =6
        elif typeIndex == 2:
            self.radius = 20
            self.health = 220
            self.fullHealth = 220
            self.speed = 4
        elif typeIndex == 3:
            self.radius = 100
            self.health = 10000
            self.fullHealth = 10000
            self.speed = 4

    def move(self, dx, dy, app):
        if dx == 0 and dy == 0:
            self.moving = False
        else:
            self.moving = True
            self.x += dx * self.speed
            self.y += dy * self.speed
    
    def draw(self, app):
        x = self.x - app.screenLeft
        y = self.y - app.screenTop
        # drawCircle(x, y, self.radius, fill = 'green') 
        if self.type == 'fast':
            zombie = app.images['smallZombie'] 
            zombieWidth = 20
            zombieHeight = 30
        elif self.type == 'normal':
            zombie = app.images['normalZombie']
            zombieWidth = 50
            zombieHeight = 50
            
        elif self.type == 'tank':
            zombie = app.images['bigZombie']
            zombieWidth = zombieHeight = 45
        elif self.type =='boss':
            zombie = '/Users/connorchoe/Desktop/boss.png'
            zombieWidth = 200
            zombieHeight = 200
        xOffSet = zombieWidth/2
        yOffset = zombieHeight/2
        drawImage(zombie, x-xOffSet, y-yOffset, width = zombieWidth, height = zombieHeight, visible = True)
        if self.health < self.fullHealth:
            self.drawHealthBar(app)
        self.drawHitMarker(app)

    def drawHealthBar(self, app):
        barWidth = self.radius * 2 
        barHeight = 10
        x = self.x - app.screenLeft -  barWidth/2
        if self.type =='boss':
            y = self.y - app.screenTop - self.radius
        else:
            y = self.y - app.screenTop - self.radius*2
        drawRect(x, y, barWidth, barHeight, fill = 'red', border = 'black')
        healthWidth = barWidth * (self.health/self.fullHealth) #find percent of health they have
        try:
            drawRect(x, y, healthWidth, barHeight, fill = 'green') 
        except:
            return
    def drawHitMarker(self, app):
        if self.isHit:
            if app.player.weapon == 'sword':
                damage = 150
            elif app.bullets != []:
                damage = app.bullets[-1].damage
            else: return
            x = self.x - app.screenLeft
            if self.type == 'boss':
                y = self.y - app.screenTop - self.radius
            else:
                y = self.y - app.screenTop - self.radius*2

            drawLabel(f'{damage}', x, y, size = 25, fill = 'white')

    def isAttacking(self, other):
        if isinstance(other, Player):
            if self.distance(self.x, self.y, other.x, other.y) < (self.radius + other.radius):
                other.health -=5
                return True
            else:return False
        return False
    

                
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2)**0.5
        
#bullet Class
class Bullet:
    def __init__(self, x, y, targetX, targetY, app, i):
        self.type = app.player.weapon
        if self.type == 'rayGun':
            self.i = i * 20
        self.x = x
        self.y = y
        
        self.targetX = targetX 
        self.targetY = targetY
        self.radius = 4
        self.speed = 15
        self.magnitude = ((targetX - x)**2 + (targetY - y)**2) **0.5
        self.dx = (targetX - x)/self.magnitude
        self.dy = (targetY- y)/self.magnitude
        
        self.damage = 40 if self.type =='gun' else 5

    def __repr__(self):
        return(f'start({self.x},{self.y}) end({self.targetX},{self.targetY})')
        
    def move(self):
        self.x +=  self.dx* self.speed
        self.y +=  self.dy* self.speed
        
    def draw(self, app):
        if self.type == 'rayGun':
            self.x = (self.x + (self.dx * self.i))
            self.y = (self.y + (self.dy * self.i))
            x = self.x - app.screenLeft
            y = self.y - app.screenTop
            drawCircle(x, y, self.radius, fill = 'blue')
        else: 
            x = self.x - app.screenLeft
            y = self.y - app.screenTop
            drawCircle(x, y, self.radius)
        
    def isHittingZombie(self, other):
        if isinstance(other, Zombie):
            if self.distance(self.x, self.y, other.x, other.y) < (self.radius + other.radius):
                other.health -= self.damage
                return True
            else: return False
        return False

    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2)**0.5
            
class Loot:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y 
        types = ['infiniteAmmo', 'rayGun', 'sword', 'health', 'health', 
                'ammo', 'ammo', 'ammo', 'ammo', 'ammo']
        self.type = types[type]
        self.radius = 15
        self.isUsed = False
        
    def draw(self, app):
        x = self.x - app.screenLeft
        y = self.y - app.screenTop
        if self.type == 'ammo':
            color = 'black'
        elif self.type == 'rayGun':
            color = 'red'
        elif self.type == 'sword':
            color = 'white'
        elif self.type == 'infiniteAmmo':
            color = 'green'
        elif self.type == 'health':
            color = 'blue'
        else:
            color = None
        drawCircle(x, y, self.radius, fill = color, opacity = 75)
        image = app.images[self.type]
        imageSize = self.radius * 2
        drawImage(image, x, y, width = imageSize,height = imageSize, align = 'center' )

    def isPickedUp(self, app):
        if self.distance(app.player.x, app.player.y, self.x, self.y) < (self.radius + app.player.radius):
            return True
        return False
        
        
    @staticmethod 
    def distance(x0, y0, x1, y1):
        return ((x1-x0)**2 + (y1-y0)**2)**0.5
        

class Button:
    def __init__(self, x, y, width, height, message):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.message = message
        self.messageSize = 40 
    def draw(self):
        if len(self.message) >= 4:
            self.messageSize = 40 * 3/len(self.message)
        drawRect(self.x - self.width/2, self.y - self.height/2, self.width, self.height, 
                 border = 'black', fill = 'red')
        drawLabel(self.message, self.x, self.y, size = self.messageSize)
    
        
def spawnLoot(app):
    x =  random.randint(app.boardLeft, app.boardLeft + app.boardWidth)
    y = random.randint(app.boardTop, app.boardTop + app.boardHeight)
    loot = [v for v in range(10)]
    i = random.randint(0, len(loot)-1)
    app.loot.append(Loot(x, y, loot[i]))
    
def activateLoot(app, loot):
    if loot.type == 'health':
        if app.player.health >= 80:
            app.player.health = 100
        else:
            app.player.health += 20
    elif loot.type == 'ammo':
        app.player.ammo  += 20
    elif loot.type == 'rayGun':
        app.player.weapon = 'rayGun'
        app.startTimer = True
    elif loot.type == 'sword':
        app.player.weapon = 'sword'
        app.startTimer = True
    elif loot.type == 'infiniteAmmo' and app.player.weapon == 'gun':
        app.player.powerups = 'infiniteAmmo'
        app.player.ammo = 99999
        app.animation = True
        app.startTimer = True
    
        
def clearRadius(app):
    app.animation = True
    if app.player.weapon == 'sword':
        for zombie in app.zombies:
            if distance(zombie.x, zombie.y,app.player.x, app.player.y) < 80:
                zombie.health -= 150
                zombie.isHit = True

 
def distance(x0,y0,x1,y1):  
    return ((x1-x0)**2 + (y1-y0)**2)**0.5
def isOffScreen(app, bullet):
    if (0< bullet.x < app.boardWidth and 
        0< bullet.y < app.boardHeight):
            return False
    return True
      
##drawing the board
def drawBoard(app): #only draw cells that are shown
    cellWidth = app.boardWidth/app.cols
    cellHeight = app.boardHeight/ app.rows
    startCol = max(0, int(app.screenLeft/cellWidth))
    startRow = max(0, int(app.screenTop/cellHeight))
    endCol = min(app.cols, int((app.screenLeft + app.width)/cellWidth) + 2)
    endRow = min(app.rows, int((app.screenTop + app.height)/cellHeight) + 2)

    for row in range(startRow, endRow):
        for col in range(startCol, endCol):
            drawCell(app, row, col)
#had claude explain the logic behind world and canvas coordinates
def drawCell(app, row, col):
    cellWidth = app.boardWidth/app.cols
    cellHeight = app.boardHeight/ app.rows
    cellWorldLeft  = app.boardLeft + col * cellWidth          #cell position relative to the world
    cellWorldTop = app.boardTop + row * cellHeight
    cellScreenLeft = cellWorldLeft - app.screenLeft             #cell position relative to canvas
    cellScreenTop = cellWorldTop - app.screenTop
    tile = app.images['dirtTile']
    if app.bossLevel or app.loadingScreen:
        tile = '/Users/connorchoe/Desktop/hellTile.png'
    drawImage(tile, cellScreenLeft, cellScreenTop, width = cellWidth, height = cellHeight)
            
#key press events

def onKeyPress(app, key): 
    if app.startScreen == True:
        if key == 'space':
            app.startScreen = False
    elif app.endScreen == True:
        if key =='space':
            app.endScreen = False
            restart(app)
    #HOTKEYS
    if key == '0':#boss level
        app.level = 10
        app.zombies = []
    if key == 'c':#new round
        while len(app.zombies) > 0:
            app.zombies.pop()
    if key == 'p':#remove ammo
        app.player.ammo = 0 
    if key == 'r':#spawn rayGun
        app.loot.append(Loot(app.width/2, app.height/2,1))
    if key == 'z':#player die
        app.player.health = -1
    if key == 't':#spawn sword
        app.loot.append(Loot(app.width/2, app.height/2,2))
    if key == 'i':#spawn infinite ammo
        app.loot.append(Loot(app.width/2, app.height/2,0))

    
    
def onKeyHold(app, keys):
    dx = dy = 0 
    if 'w' in keys and 's' not in keys:
        dy = -app.speed
    elif 's' in keys and 'w' not in keys:
        dy = app.speed
    if 'a' in keys and 'd' not in keys:
        dx = -app.speed
    elif 'd' in keys and 'a' not in keys:
        dx = app.speed
    if dx != 0 and dy != 0: #make sure diagonal movement is same speed 
        magnitude = (dx**2 + dy**2)**0.5
        dx = (dx/magnitude) *app.speed
        dy = (dy/magnitude) * app.speed
        
    newPosition = (app.player.x + dx, app.player.y + dy)
    if inBounds(app, newPosition):
        app.player.move(dx, dy, app)
#mousePressEvents

def onMousePress(app,mouseX, mouseY):
    #append world coordinates not canvas coordinates
    targetX = mouseX + app.screenLeft
    targetY = mouseY + app.screenTop
    if app.player.weapon == 'gun':
        app.player.ammo -= 1
        app.totalShots += 1
        if app.player.ammo < 0:
            app.messageTimer = 0 
            app.player.outOfAmmo(app)
            return
        app.bullets.append((Bullet(app.player.x, app.player.y, targetX, targetY, app, None)))
    elif app.player.weapon == 'rayGun':
        app.bullets = []
        app.rayGun = True
        app.target = (targetX, targetY)
     
    elif app.player.weapon == 'sword':
        clearRadius(app)

def onMouseDrag(app, mouseX, mouseY):
    if app.player.weapon == 'rayGun':
        app.bullets = []
        targetX = mouseX + app.screenLeft
        targetY = mouseY + app.screenTop
        app.target = (targetX, targetY)

def onMouseRelease(app, mouseX, mouseY):
    if app.player.weapon == 'rayGun':
        app.rayGun = False
        app.bullets = []

def inBounds(app, newPosition):
    if (app.boardLeft < newPosition[0] < (app.boardLeft + app.boardWidth) and 
        app.boardTop < newPosition[1] < (app.boardTop + app.boardHeight)):
            return True
    return False

def main():
    runApp()

main()
