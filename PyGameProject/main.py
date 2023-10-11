
import pygame
import os

pygame.font.init()
pygame.mixer.init()

Width, Height = 900, 500
Win = pygame.display.set_mode((Width, Height))
White = (255, 255, 255)
Black = (0, 0, 0)
RED = (255, 0, 0)
Yellow = (255, 255, 0)
Border = pygame.Rect(Width // 2 - 4, 0, 8, Height)
FPS = 60
Velocity = 5
YellowBullets = []
RedBullets = []
MaxBullets = 3
WinnerFont = pygame.font.SysFont("comiscans", 100)
BulletHitSound = pygame.mixer.Sound(
    os.path.join("PyGameProject", "Assets", "Grenade+1.mp3")
)
BulletFireSound = pygame.mixer.Sound(
    os.path.join("PyGameProject", "Assets", "Gun+Silencer.mp3")
)
HealthFont = pygame.font.SysFont("comiscans", 40)
YellowHit = pygame.USEREVENT + 1
RedHit = pygame.USEREVENT + 2
pygame.display.set_caption("First Game Project")
SpaceShipWidth, SpaceshipHeight = 45, 35
Space = pygame.transform.scale(
    pygame.image.load(
        os.path.join("PyGameProject", "Assets", "space.png")
    ),
    (Width, Height),
)

YellowSpaceshipImage = pygame.image.load(
    os.path.join( "PyGameProject", "Assets", "Yellow.png")
)
YellowSpaceship = pygame.transform.rotate(
    pygame.transform.scale(YellowSpaceshipImage, (SpaceShipWidth, SpaceshipHeight)), 90
)

RedSpaceshipImage = pygame.image.load(
    os.path.join("PyGameProject", "Assets", "Red.png")
)
RedSpaceship = pygame.transform.rotate(
    pygame.transform.scale(RedSpaceshipImage, (SpaceShipWidth, SpaceshipHeight)), -90
)


def Handle_bullets(YellowBullets, RedBullets, yellow, red):
    for bullet in YellowBullets:
        bullet.x += Velocity
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RedHit))
            YellowBullets.remove(bullet)
        elif bullet.x > Width:
            YellowBullets.remove(bullet)
    for bullet in RedBullets:
        bullet.x -= Velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YellowHit))
            RedBullets.remove(bullet)
        elif bullet.x < 0:
            RedBullets.remove(bullet)


def RedMovement(keysPressed, red):
    if keysPressed[pygame.K_LEFT] and red.x - Velocity > Border.x + Border.width:
        red.x -= Velocity
    if keysPressed[pygame.K_RIGHT] and red.x + Velocity + SpaceShipWidth < Width - 10:
        red.x += Velocity
    if keysPressed[pygame.K_UP] and red.y - Velocity > 0:
        red.y -= Velocity
    if keysPressed[pygame.K_DOWN] and red.y + Velocity + SpaceshipHeight < Height - 10:
        red.y += Velocity


def YellowMovement(keysPressed, yellow):
    if keysPressed[pygame.K_a] and yellow.x - Velocity > 0:
        yellow.x -= Velocity
    if keysPressed[pygame.K_d] and yellow.x + Velocity + SpaceShipWidth < Border.x:
        yellow.x += Velocity
    if keysPressed[pygame.K_w] and yellow.y - Velocity > 0:
        yellow.y -= Velocity
    if keysPressed[pygame.K_s] and yellow.y + Velocity + SpaceshipHeight < Height - 10:
        yellow.y += Velocity


def draw_window(red, yellow, RedBullets, YellowBullets, RedHealth, YellowHealth):
    Win.blit(Space, (0, 0))
    pygame.draw.rect(Win, Black, Border)
    redHealthText = HealthFont.render("Health:" + str(RedHealth), 1, White)
    YellowHealtText = HealthFont.render("Health:" + str(YellowHealth), 1, White)
    Win.blit(YellowSpaceship, (yellow.x, yellow.y))
    Win.blit(RedSpaceship, (red.x, red.y))
    Win.blit(redHealthText, (Width - redHealthText.get_width() - 10, 10))
    Win.blit(YellowHealtText, (10, 10))
    for bullet in YellowBullets:
        pygame.draw.rect(Win, Yellow, bullet)
    for bullet in RedBullets:
        pygame.draw.rect(Win, RED, bullet)

    pygame.display.update()


def Winner_Draw(text):
    drawText = WinnerFont.render(text, 1, White)
    Win.blit(
        drawText,
        (Width / 2 - drawText.get_width() / 2, Height / 2 - drawText.get_height()),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    YellowHealth = 10
    RedHealth = 10
    yellow = pygame.Rect(30, 225, SpaceShipWidth, SpaceshipHeight)
    red = pygame.Rect(850, 225, SpaceShipWidth, SpaceshipHeight)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(YellowBullets) < MaxBullets:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2, 10, 5
                    )
                    YellowBullets.append(bullet)
                    BulletFireSound.play()

                if event.key == pygame.K_RCTRL and len(RedBullets) < MaxBullets:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2, 10, 5)
                    RedBullets.append(bullet)
                    BulletFireSound.play()
            if event.type == RedHit:
                RedHealth -= 1
                BulletHitSound.play()

            if event.type == YellowHit:
                YellowHealth -= 1
                BulletHitSound.play()

        winnerText = ""
        if RedHealth <= 0:
            winnerText = "Yellow Win"

        if YellowHealth <= 0:
            winnerText = "Red Win   "

        if winnerText != "":
            Winner_Draw(winnerText)
            break

        keysPressed = pygame.key.get_pressed()
        YellowMovement(keysPressed, yellow)
        RedMovement(keysPressed, red)
        Handle_bullets(YellowBullets, RedBullets, yellow, red)
        draw_window(red, yellow, RedBullets, YellowBullets, RedHealth, YellowHealth)
    main()


if __name__ == "__main__":
    main()
