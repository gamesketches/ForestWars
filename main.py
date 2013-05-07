import sys, pygame, os
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

platformListing = []
TERMINALVELOCITY = 2

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
        if not self.grounded:
            if self.checkGrounded():
                self.velocity[1] = 0
            else:
                if self.velocity[1] <= TERMINALVELOCITY:
                    self.velocity[1] += 1
                self.rect = self.rect.move((self.velocity[0],self.velocity[1]))

    def checkGrounded(self):
        for i in platformListing:
            if i.hitBox.colliderect(self.rect.move(0,self.velocity[1])):
                self.grounded = True
                return True
        else:
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((700,400))
    pygame.display.set_caption("Forest Wars!")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250,250,250))

    ground = Platform((0,350),700,50)

    screen.blit(background, (0,0))
    screen.blit(ground.visualPlatform, ground.hitBox.topleft)
    pygame.display.flip()

    player = Player()

    allsprites = pygame.sprite.Group()

    allsprites.add(player)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()

        screen.blit(background, (0,0))
        screen.blit(ground.visualPlatform, ground.hitBox.topleft)

        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()

    
        
        
