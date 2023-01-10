import pygame
from network import Network

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN =(0,255,0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100


clientNumber = 0

class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height, colour):
        self.x = self.origin_x = x
        self.y = self.origin_y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x,y,width,height)

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y - self.VELOCITY - 10 >= 0:
            self.y -= self.VELOCITY
        elif keys[pygame.K_DOWN] and self.y + self.VELOCITY + self.height + 10 <= HEIGHT:
            self.y += self.VELOCITY

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y

def draw(win, lpaddle, rpaddle, ball):
    win.fill(BLACK)
    lpaddle.draw(win)
    rpaddle.draw(win)
    ball.draw(win)
    pygame.draw.rect(win, WHITE, (WIDTH // 2 - 4, 0, 8, HEIGHT))
    pygame.display.update()

class Ball:
    max_vel = 5

    def __init__(self, x, y, radius):
        self.x = self.origin_x = x
        self.y = self.origin_y = y
        self.radius = radius
        self.x_vel = self.max_vel
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
        self.y_vel = 0
        self.x_vel *= -1

def boundscollision(ball):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

def collision(ball, left_paddle, right_paddle):
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                factor(left_paddle, ball)
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                factor(right_paddle, ball)

def factor(paddle, ball):
    middle_y = paddle.y + paddle.height / 2
    y_difference = middle_y - ball.y
    factor = (paddle.height / 2) / ball.max_vel
    y_vel = y_difference / factor
    ball.y_vel = y_vel * -1


def read_pos(str):
    if str is not None:
        str = str.split(",")
        return int(str[0]), int(str[1])

def make_pos(tuple):
    if tuple is not None:
        return str(tuple[0]) + "," + str(tuple[1])

def paddleclientupdate(paddle, n, other_paddle):
    pos = read_pos(n.send(make_pos((other_paddle.x, other_paddle.y))))
    paddle.x = pos[0]
    paddle.y = pos[1]
    paddle.update()


def main():
    run = True
    n = Network()
    startpos = read_pos(n.get_pos())
    clock = pygame.time.Clock()

    right_paddle = Paddle(startpos[0], startpos[1], PADDLE_WIDTH, PADDLE_HEIGHT, GREEN)

    left_paddle = Paddle(10, 200, PADDLE_WIDTH, PADDLE_HEIGHT, RED)

    ball = Ball(WIDTH // 2, HEIGHT // 2, 7)

    while run:
        clock.tick(FPS)

        paddleclientupdate(left_paddle, n, right_paddle)

        draw(WIN, left_paddle, right_paddle, ball)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        boundscollision(ball)
        #collision(ball, left_paddle, right_paddle)
        ball.move()
        right_paddle.move()


    pygame.quit()


if __name__ == '__main__':
    main()
