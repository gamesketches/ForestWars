import sys, pygame, os
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

platformListing = []

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.conver()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Player(pygame.sprite.Sprite):
    """Player object when platforming"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        "Move character, check collisions with platforms, gravity"

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

if __name__ == '__main__':
    main()

    
        
        
