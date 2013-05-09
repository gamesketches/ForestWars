import sys, pygame, os
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

platformListing = []
TERMINALVELOCITY = 2
TERMINALHORIZONTALVELOCITY = 5
CURRENTSCREEN = "platformer"

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class mapNode(pygame.sprite.Sprite):
    """Nodes on the map when in the strategy mode"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.selected = False
        self.unselectedImage, self.rect = load_image("node.bmp")
        self.selectedImage, self.rect = load_image("selectedNode.bmp")
        self.images = [self.unselectedImage, self.selectedImage]
        self.image = self.unselectedImage
        self.mouseStatus = "unclicked"

    def update(self):
        "Check if selected, switch state accordingly"
        for i in pygame.event.get():
            if i.type == MOUSEBUTTONDOWN and self.mouseStatus is "unclicked":
                if pygame.mouse.get_pressed()[0] == 1 and \
                   self.rect.collidepoint(pygame.mouse.get_pos()):
                    if not self.selected:
                        self.selected = not self.selected
                        self.image = self.images[self.selected]
                        self.mouseStatus = "beingClicked"
                    else:
                        global CURRENTSCREEN
                        CURRENTSCREEN = "switch"
                        print "yo"
            elif i.type == MOUSEBUTTONUP and self.mouseStatus is "beingClicked":
                self.mouseStatus = "unclicked"

class Player(pygame.sprite.Sprite):
    """Player object when platforming"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walkingLeft, self.walkingRight = self.loadAnimations('BoyKnight.png')
        self.frame = 0
        self.rect = pygame.Rect(0,0,32,32)
        self.grounded = False
        self.velocity = [0,0]

    def update(self):
        "Move character, check collisions with platforms, gravity"
        self.image = self.walkingRight[self.frame]
        self.frame = not self.frame

        # input handling
        if pygame.key.get_pressed()[K_RIGHT] and self.velocity[0] < TERMINALHORIZONTALVELOCITY:
            self.velocity[0] += 1
        elif pygame.key.get_pressed()[K_LEFT] and self.velocity[0] > -TERMINALHORIZONTALVELOCITY:
            self.velocity[0] += -1
        elif pygame.key.get_pressed()[K_UP] and self.grounded:
            self.velocity[1] += -20
            self.grounded = False
            
        if not self.grounded:
            if self.checkGrounded():
                self.velocity[1] = 0
            else:
                if self.velocity[1] <= TERMINALVELOCITY:
                    self.velocity[1] += 1
        else:
            self.checkGrounded()
            if self.velocity[0] > 0:
                self.velocity[0] -= 0.3
            else:
                self.velocity[0] += 0.3
                
        self.rect = self.rect.move((self.velocity[0],self.velocity[1]))

    def checkGrounded(self):
        for i in platformListing:
            if i.hitBox.colliderect(self.rect.move(0,self.velocity[1])):
                self.grounded = True
                return True
        self.grounded = False
        return False
        
            

    def loadAnimations(self, filename):
        walkingRight = []
        walkingLeft = []

        master_image, master_rect = load_image(filename)

        print type(master_image)

        walkingLeft.append(master_image.subsurface((0,64),(32,32)))
        walkingLeft.append(master_image.subsurface((32,64,32,32)))

        walkingRight.append(master_image.subsurface((0,96,32,32)))
        walkingRight.append(master_image.subsurface((32,96,32,32)))

        return walkingLeft, walkingRight
                           

class Platform:
    """ Platforms for getting higher. Container for a Surface and rect"""
    def __init__(self, topLeft, width, height, color=(0,0,0)):
        self.visualPlatform = pygame.Surface((width,height))
        self.visualPlatform.convert()
        self.visualPlatform.fill(color)
        self.hitBox = pygame.Rect(topLeft,(width,height))
        platformListing.append(self)

class Goal(pygame.sprite.Sprite):
    """ Goal rect for the platforming segments """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Goal.png')

def main():
    pygame.init()
    screen = pygame.display.set_mode((700,400))
    pygame.display.set_caption("Forest Wars!")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))

    ground = Platform((0,350),700,50)

    platform1 = Platform((400, 200), 300, 20)
    platform2 = Platform((100, 100), 100, 20)

    screen.blit(background, (0,0))

    global CURRENTSCREEN

    player = Player()
    goal = Goal()

    myNode = mapNode()

    myNode.rect = myNode.rect.move(200,200)

    goal.rect = goal.rect.move(200, 0)

    allsprites = pygame.sprite.Group(player, goal)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
        if CURRENTSCREEN is "platformer":
            print "yoyo"
            screen.blit(background, (0,0))
            for i in platformListing:
                screen.blit(i.visualPlatform, i.hitBox.topleft)

            if player.rect.colliderect(goal.rect):
                CURRENTSCREEN = "map"
                player.rect = player.rect.move((-100, 100))
                allsprites.empty()
                allsprites.add(myNode)
                
            allsprites.update()
            allsprites.draw(screen)
        elif CURRENTSCREEN is "map":
            background.fill((0,0,0))
            screen.blit(background, (0,0))
            allsprites.update()
            allsprites.draw(screen)
        elif CURRENTSCREEN is "switch":
            background.fill((250,250,250))
            allsprites.empty()
            allsprites.add(player,goal)
            CURRENTSCREEN = "platformer"
        pygame.display.flip()

if __name__ == '__main__':
    main()

    
        
        
