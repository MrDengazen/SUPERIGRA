import pygame
from pygame import *
import pyganim


class Platform(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image1, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Player(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))
        for anim in ANIMATION_RIGHT:
            boltAnim1.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim1)
        self.boltAnimRight.scale((22, 32))
        self.boltAnimRight.play()
        for anim in ANIMATION_LEFT:
            boltAnim2.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim2)
        self.boltAnimLeft.scale((22, 32))
        self.boltAnimLeft.play()
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.scale((22, 32))
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим
        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.scale((22, 32))
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.scale((22, 32))
        self.boltAnimJumpRight.play()
        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.scale((22, 32))
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0
        if not up and not (left or right):
            self.image.fill(Color(COLOR))
            self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

if __name__ == "__main__":
    image1 = image.load("other\grass2.jpg")
    boltAnim2 = []
    boltAnim1 = []
    ANIMATION_DELAY = 100
    ANIMATION_RIGHT = ['other/r0.png',
                       'other/r1.png',
                       'other/r2.png',
                       'other/r3.png',
                       'other/r4.png',
                       'other/r5.png',
                       'other/r6.png',
                       'other/r7.png', ]
    ANIMATION_LEFT = ['other/l0.png',
                      'other/l1.png',
                      'other/l2.png',
                      'other/l3.png',
                      'other/l4.png',
                      'other/l5.png',
                      'other/l6.png',
                      'other/l7.png']
    ANIMATION_JUMP_LEFT = [('other/lj0.png', 1)]
    ANIMATION_JUMP_RIGHT = [('other/rj0.png', 1)]
    ANIMATION_JUMP = [('other/rj0.png', 1)]
    ANIMATION_STAY = [('other/i0.png', 1)]
    timer = pygame.time.Clock()
    MOVE_SPEED = 5.5
    WIDTH = 22
    HEIGHT = 32
    COLOR = "#888888"
    width = 800
    height = 640
    display = (width, height)
    PLATFORM_WIDTH = 32
    PLATFORM_HEIGHT = 32
    PLATFORM_COLOR = "#FF6262"
    hero = Player(55, 55)
    up = left = right = False
    JUMP_POWER = 11.3
    GRAVITY = 0.45
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)
    level = [
        "-------------------------",
        "-                       -",
        "-                       -",
        "-                       -",
        "-            --         -",
        "-                       -",
        "--                      -",
        "-                       -",
        "-                   --- -",
        "-                       -",
        "-                       -",
        "-      ---              -",
        "-                       -",
        "-   -----------         -",
        "-                       -",
        "-                -      -",
        "-                   --  -",
        "-                       -",
        "-                       -",
        "-------------------------"]
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    pygame.init()
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("IGRA TOP")
    bg = Surface((width, height))
    bg.fill(Color((180, 233, 255)))
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == QUIT:
                running = False
        screen.blit(bg, (0, 0))
        timer.tick(60)
        hero.update(left, right, up, platforms)
        entities.draw(screen)
        pygame.display.update()
    pygame.quit()