import pygame
from pygame import *
import pyganim


class Camera(object):
    def __init__(self, cam_func, w_cam, h_cam):
        self.cam_func = cam_func
        self.state = Rect(0, 0, w_cam, h_cam)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.cam_func(self.state, target.rect)


def camera_configure(cam, target_rect):
    xcam, ycam, _, _ = target_rect
    _, _, w, h = cam
    xcam, ycam = -xcam + windowWidth / 2, -ycam + windowHeight / 2

    xcam = min(0, xcam)
    xcam = max(-(cam.width - windowWidth), xcam)
    ycam = max(-(cam.height - windowHeight), ycam)
    ycam = min(0, ycam)

    return Rect(xcam, ycam, w, h)


class Platform(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image.load("other/grass2.jpg"), (platformWigth, platformHeight))
        self.rect = Rect(x, y, platformWigth, platformHeight)


class Player(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.winner = False
        self.onGround = False
        self.bodyRotation = 1
        self.yMove = 0
        self.xMove = 0
        self.startX = x
        self.startY = y
        self.image = Surface((heroWidth, heroHeight))
        self.image.fill(Color(heroColor))
        self.rect = Rect(x, y, heroWidth, heroHeight)
        self.image.set_colorkey(Color(heroColor))
        for anim in heroRunRightAnimation:
            boltAnim1.append((anim, animationDelay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim1)
        self.boltAnimRight.scale((heroWidth, heroHeight))
        self.boltAnimRight.play()
        for anim in heroRunLeftAnimation:
            boltAnim2.append((anim, animationDelay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim2)
        self.boltAnimLeft.scale((heroWidth, heroHeight))
        self.boltAnimLeft.play()
        self.boltAnimRightStay = pyganim.PygAnimation(heroIdleRightAnimation)
        self.boltAnimRightStay.scale((heroWidth, heroHeight))
        self.boltAnimRightStay.play()
        self.boltAnimRightStay.blit(self.image, (0, 0))
        self.boltAnimLeftStay = pyganim.PygAnimation(heroIdleLeftAnimation)
        self.boltAnimLeftStay.scale((heroWidth, 32))
        self.boltAnimLeftStay.play()
        self.boltAnimLeftStay.blit(self.image, (0, 0))
        self.boltAnimJumpLeft = pyganim.PygAnimation(heroJumpLeftAnimation)
        self.boltAnimJumpLeft.scale((heroWidth, heroHeight))
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpRight = pyganim.PygAnimation(heroJumpRightAnimation)
        self.boltAnimJumpRight.scale((heroWidth, heroHeight))
        self.boltAnimJumpRight.play()

    def update(self, left, right, up, platforms):
        self.rect.y += self.yMove
        self.collide(0, self.yMove, platforms)
        self.rect.x += self.xMove
        self.collide(self.xMove, 0, platforms)
        if up:
            if self.onGround:
                self.yMove = -jumpPower
            if self.bodyRotation:
                self.image.fill(Color(heroColor))
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.image.fill(Color(heroColor))
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
        if left:
            self.xMove = -moveSpeed
            self.image.fill(Color(heroColor))
            self.boltAnimLeft.blit(self.image, (0, 0))
            self.bodyRotation = 0

        if right:
            self.xMove = moveSpeed
            self.image.fill(Color(heroColor))
            self.boltAnimRight.blit(self.image, (0, 0))
            self.bodyRotation = 1
        if not (left or right):
            self.xMove = 0
        if not (left or right) and self.onGround:
            if self.bodyRotation:
                self.image.fill(Color(heroColor))
                self.boltAnimRightStay.blit(self.image, (0, 0))
            else:
                self.image.fill(Color(heroColor))
                self.boltAnimLeftStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.yMove += gravity
        self.onGround = False

    def collide(self, xMove, yMove, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if not isinstance(p, Gem) and xMove > 0:
                    self.rect.right = p.rect.left

                if not isinstance(p, Gem) and xMove < 0:
                    self.rect.left = p.rect.right

                if not isinstance(p, Gem) and yMove > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yMove = 0
                if not isinstance(p, Gem) and yMove < 0:
                    self.rect.top = p.rect.bottom
                    self.yMove = 0

                if isinstance(p, BlockDie):
                    self.die()

                if isinstance(p, Gem):
                    self.winner = True

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.transform.scale(image.load("other/d0.png"), (platformWigth, platformHeight))


class Gem(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.transform.scale(image.load("other\gem-1.png"), (platformWigth, platformHeight))
        boltAnim = []
        for anim in animationGem:
            boltAnim.append(("other/" + anim, 100))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.scale((platformWigth, platformHeight))
        self.boltAnim.play()

    def update(self):
        self.boltAnim.blit(self.image, (0, 0))


if __name__ == "__main__":
    boltAnim2 = []
    boltAnim1 = []
    animationDelay = 45
    animationGem = ['gem-1.png',
                    'gem-2.png',
                    'gem-3.png',
                    'gem-4.png',
                    'gem-5.png']
    heroRunRightAnimation = ['other/r0.png',
                             'other/r1.png',
                             'other/r2.png',
                             'other/r3.png',
                             'other/r4.png',
                             'other/r5.png',
                             'other/r6.png',
                             'other/r7.png', ]
    heroRunLeftAnimation = ['other/l0.png',
                            'other/l1.png',
                            'other/l2.png',
                            'other/l3.png',
                            'other/l4.png',
                            'other/l5.png',
                            'other/l6.png',
                            'other/l7.png']
    heroJumpLeftAnimation = [('other/lj0.png', 1)]
    heroJumpRightAnimation = [('other/rj0.png', 1)]
    heroIdleRightAnimation = [('other/ir0.png', 1)]
    heroIdleLeftAnimation = [('other/il0.png', 1)]
    timer = pygame.time.Clock()
    moveSpeed = 5.5
    heroWidth = 22
    heroHeight = 32
    platformWigth = 32
    platformHeight = 32
    heroColor = "#888888"
    windowWidth = 800
    windowHeight = 640
    display = (windowWidth, windowHeight)
    up = left = right = False
    jumpPower = 11.4
    gravity = 0.45
    entities = pygame.sprite.Group()
    platforms = []
    level = [
        "----------------------------------",
        "-                        G       -",
        "-                       --       -",
        "-        *          -  -         -",
        "-                                -",
        "-            --                  -",
        "--                               -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "-            *                   -",
        "-                           ---- -",
        "-                                -",
        "-                                -",
        "-  *   ---                  *    -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-           ***                  -",
        "-                                -",
        "----------------------------------"]
    hero = Player(55, (len(level) - 3) * platformHeight)
    entities.add(hero)
    total_level_width = len(level[0]) * platformWigth
    total_level_height = len(level) * platformHeight
    camera = Camera(camera_configure, total_level_width, total_level_height)
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "G":
                g = Gem(x, y)
                entities.add(g)
                platforms.append(g)
            x += platformWigth
        y += platformHeight
        x = 0
    pygame.init()
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("game")
    bg = Surface((windowWidth, windowWidth))
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
        camera.update(hero)
        for e in entities:
            if isinstance(e, Gem):
                e.update()
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
    pygame.quit()
