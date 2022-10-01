import sys
import pygame
from pygame.locals import *
from pygame.sprite import Group
import random
import time
from Ball import Ball
from Paddle import Paddle
from BonusBrick import BonusBrick
from Brick import Brick

# screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ball size
BALL_WIDTH = 15
BALL_HEIGHT = 15

# paddle size
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15

# brick size
BRICK_WIDTH = 50
BRICK_HEIGHT = 20

# bonus brick size
BONUS_WIDTH = 20
BONUS_HEIGHT = 20

# number of lives
LIVES = 3

# number of levels
LEVELS = 3

# game speed
SPEED = 5

# ball speed
BALL_SPEED = 5

# bonus speed
BONUS_SPEED = 5

# ball direction
BALL_DIRECTION = (1,1)

# bonus direction
BONUS_DIRECTION = (1,1)

# brick colors
BRICK_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

# bonus colors
BONUS_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]

# bonus types
BONUS_TYPES = ['split', 'enlarge', 'shrink', 'life']

# default font
DEFAULT_FONT = 'freesansbold.ttf'

# font size
FONT_SIZE = 20

# font color
FONT_COLOR = (0,0,0)

# background color
BACKGROUND_COLOR = (255,255,255)

# game over color
GAME_OVER_COLOR = (255,0,0)

# game over font size
GAME_OVER_FONT_SIZE = 50

# game over text
GAME_OVER_TEXT = 'GAME OVER'

# game over text position
GAME_OVER_TEXT_POSITION = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# game class
class Game(object):
    def __init__(self, screen, level, player):
        self.screen = screen
        self.level = level
        self.player = player
        self.lives = LIVES
        self.score = 0
        self.font = pygame.font.Font(DEFAULT_FONT, FONT_SIZE)
        self.font_color = FONT_COLOR
        self.background_color = BACKGROUND_COLOR
        self.game_over_color = GAME_OVER_COLOR
        self.game_over_font_size = GAME_OVER_FONT_SIZE
        self.game_over_text = GAME_OVER_TEXT
        self.game_over_text_position = GAME_OVER_TEXT_POSITION
        self.ball = Ball(self.screen.get_width()/2, self.screen.get_height()/2, BALL_WIDTH, BALL_HEIGHT, (0,0,0), BALL_SPEED, BALL_DIRECTION)
        self.paddle = Paddle(self.screen.get_width()/2, self.screen.get_height() - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, (0,0,0), SPEED)
        self.bricks = Group()
        self.bonus_bricks = Group()
        self.bonus_balls = Group()
        self.bonus_paddles = Group()
        self.bonus_lives = Group()
        self.bonus_balls_number = 0
        self.bonus_paddles_number = 0
        self.bonus_lives_number = 0
        self.bonus_balls_speed = BALL_SPEED
        self.bonus_paddles_speed = SPEED
        self.bonus_lives_speed = SPEED
        self.bonus_balls_direction = BALL_DIRECTION
        self.bonus_paddles_direction = (1,1)
        self.bonus_lives_direction = (1,1)
        self.bonus_balls_width = BALL_WIDTH
        self.bonus_paddles_width = PADDLE_WIDTH
        self.bonus_lives_width = PADDLE_WIDTH
        self.bonus_balls_height = BALL_HEIGHT
        self.bonus_paddles_height = PADDLE_HEIGHT
        self.bonus_lives_height = PADDLE_HEIGHT
        self.bonus_balls_color = (0,0,0)
        self.bonus_paddles_color = (0,0,0)
        self.bonus_lives_color = (0,0,0)
        self.bonus_balls_type = 'ball'
        self.bonus_paddles_type = 'paddle'
        self.bonus_lives_type = 'life'
        self.bonus_balls_number_max = 0
        self.bonus_paddles_number_max = 0
        self.bonus_lives_number_max = 0
        self.bonus_balls_number_min = 0
        self.bonus_paddles_number_min = 0
        self.bonus_lives_number_min = 0

    # function to run the class meethods in the required order
    def run(self):
        # load level
        self.load_level()

        # main loop
        while True:
            # check for quit
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # check for key press
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.paddle.move('left')
            if pressed_keys[K_RIGHT]:
                self.paddle.move('right')

            # check for bonus paddle
            for bonus_paddle in self.bonus_paddles:
                if pressed_keys[K_a]:
                    bonus_paddle.move('left')
                if pressed_keys[K_d]:
                    bonus_paddle.move('right')

            # check for bonus life
            for bonus_life in self.bonus_lives:
                if pressed_keys[K_LEFT]:
                    bonus_life.move('left')
                if pressed_keys[K_RIGHT]:
                    bonus_life.move('right')

            # move ball
            self.ball.move()

            # move bonus balls
            for bonus_ball in self.bonus_balls:
                bonus_ball.move()

            # move bonus paddles
            for bonus_paddle in self.bonus_paddles:
                bonus_paddle.move('right')

            # move bonus lives
            for bonus_life in self.bonus_lives:
                bonus_life.move('right')

            # check for ball collision with paddle
            if pygame.sprite.collide_rect(self.ball, self.paddle):
                self.ball.bounce('y')

            # check for ball collision with bonus paddle
            for bonus_paddle in self.bonus_paddles:
                if pygame.sprite.collide_rect(self.ball, bonus_paddle):
                    self.ball.bounce('y')

            # check for ball collision with bonus life
            for bonus_life in self.bonus_lives:
                if pygame.sprite.collide_rect(self.ball, bonus_life):
                    self.ball.bounce('y')

            # check for bonus ball collision with paddle
            for bonus_ball in self.bonus_balls:
                if pygame.sprite.collide_rect(bonus_ball, self.paddle):
                    bonus_ball.bounce('y')

            # check for bonus ball collision with bonus paddle
            for bonus_ball in self.bonus_balls:
                for bonus_paddle in self.bonus_paddles:
                    if pygame.sprite.collide_rect(bonus_ball, bonus_paddle):
                        bonus_ball.bounce('y')

            # check for bonus ball collision with bonus life
            for bonus_ball in self.bonus_balls:
                for bonus_life in self.bonus_lives:
                    if pygame.sprite.collide_rect(bonus_ball, bonus_life):
                        bonus_ball.bounce('y')

            # check for ball collision with bricks
            for brick in self.bricks:
                if pygame.sprite.collide_rect(self.ball, brick):
                    self.ball.bounce('y')
                    self.bricks.remove(brick)
                    self.score += 10

            # check for ball collision with bonus bricks
            for bonus_brick in self.bonus_bricks:
                if pygame.sprite.collide_rect(self.ball, bonus_brick):
                    self.ball.bounce('y')
                    self.bonus_bricks.remove(bonus_brick)
                    self.score += 10

                    # check for bonus brick type
                    if bonus_brick.type == 'split':
                        self.bonus_balls_number = 1
                        self.bonus_balls_speed = self.ball.speed
                        self.bonus_balls_direction = self.ball.direction
                        self.bonus_balls_width = self.ball.rect.width
                        self.bonus_balls_height = self.ball.rect.height
                        self.bonus_balls_color = self.ball.image.get_at((0,0))
                        self.bonus_balls_type = 'ball'
                        self.bonus_balls_number_max = 1
                        self.bonus_balls_number_min = 1
                    elif bonus_brick.type == 'enlarge':
                        self.bonus_paddles_number = 1
                        self.bonus_paddles_speed = self.paddle.speed
                        self.bonus_paddles_direction = (1,1)
                        self.bonus_paddles_width = self.paddle.rect.width * 2
                        self.bonus_paddles_height = self.paddle.rect.height
                        self.bonus_paddles_color = self.paddle.image.get_at((0,0))
                        self.bonus_paddles_type = 'paddle'
                        self.bonus_paddles_number_max = 1
                        self.bonus_paddles_number_min = 1
                    elif bonus_brick.type == 'shrink':
                        self.bonus_paddles_number = 1
                        self.bonus_paddles_speed = self.paddle.speed
                        self.bonus_paddles_direction = (1,1)
                        self.bonus_paddles_width = self.paddle.rect.width / 2
                        self.bonus_paddles_height = self.paddle.rect.height
                        self.bonus_paddles_color = self.paddle.image.get_at((0,0))
                        self.bonus_paddles_type = 'paddle'
                        self.bonus_paddles_number_max = 1
                        self.bonus_paddles_number_min = 1
                    elif bonus_brick.type == 'life':
                        self.bonus_lives_number = 1
                        self.bonus_lives_speed = self.paddle.speed
                        self.bonus_lives_direction = (1,1)
                        self.bonus_lives_width = self.paddle.rect.width
                        self.bonus_lives_height = self.paddle.rect.height
                        self.bonus_lives_color = self.paddle.image.get_at((0,0))
                        self.bonus_lives_type = 'life'
                        self.bonus_lives_number_max = 1
                        self.bonus_lives_number_min = 1

            # check for bonus ball collision with bricks
            for bonus_ball in self.bonus_balls:
                for brick in self.bricks:
                    if pygame.sprite.collide_rect(bonus_ball, brick):
                        bonus_ball.bounce('y')
                        self.bricks.remove(brick)
                        self.score += 10

            # check for bonus ball collision with bonus bricks
            for bonus_ball in self.bonus_balls:
                for bonus_brick in self.bonus_bricks:
                    if pygame.sprite.collide_rect(bonus_ball, bonus_brick):
                        bonus_ball.bounce('y')
                        self.bonus_bricks.remove(bonus_brick)
                        self.score += 10

            # check for brick collision with paddle
            for brick in self.bricks:
                if pygame.sprite.collide_rect(brick, self.paddle):
                    self.paddle.move('left')

            # check for brick collision with bonus paddle
            for brick in self.bricks:
                for bonus_paddle in self.bonus_paddles:
                    if pygame.sprite.collide_rect(brick, bonus_paddle):
                        bonus_paddle.move('left')

            # check for brick collision with bonus life
            for brick in self.bricks:
                for bonus_life in self.bonus_lives:
                    if pygame.sprite.collide_rect(brick, bonus_life):
                        bonus_life.move('left')

            # check for bonus brick collision with paddle
            for bonus_brick in self.bonus_bricks:
                if pygame.sprite.collide_rect(bonus_brick, self.paddle):
                    self.paddle.move('left')

            # check for bonus brick collision with bonus paddle
            for bonus_brick in self.bonus_bricks:
                for bonus_paddle in self.bonus_paddles:
                    if pygame.sprite.collide_rect(bonus_brick, bonus_paddle):
                        bonus_paddle.move('left')

            # check for bonus brick collision with bonus life
            for bonus_brick in self.bonus_bricks:
                for bonus_life in self.bonus_lives:
                    if pygame.sprite.collide_rect(bonus_brick, bonus_life):
                        bonus_life.move('left')

            # check for ball collision with screen edges
            if self.ball.rect.x <= 0:
                self.ball.bounce('x')
            if self.ball.rect.x >= self.screen.get_width() - self.ball.rect.width:
                self.ball.bounce('x')
            if self.ball.rect.y <= 0:
                self.ball.bounce('y')
            if self.ball.rect.y >= self.screen.get_height() - self.ball.rect.height:
                self.lives -= 1
                self.ball.rect.x = self.screen.get_width()/2
                self.ball.rect.y = self.screen.get_height()/2
                self.ball.speed = BALL_SPEED
                self.ball.direction = BALL_DIRECTION

            # check for bonus ball collision with screen edges
            for bonus_ball in self.bonus_balls:
                if bonus_ball.rect.x <= 0:
                    bonus_ball.bounce('x')
                if bonus_ball.rect.x >= self.screen.get_width() - bonus_ball.rect.width:
                    bonus_ball.bounce('x')
                if bonus_ball.rect.y <= 0:
                    bonus_ball.bounce('y')
                if bonus_ball.rect.y >= self.screen.get_height() - bonus_ball.rect.height:
                    self.bonus_balls.remove(bonus_ball)

            # check for bonus paddle collision with screen edges
            for bonus_paddle in self.bonus_paddles:
                if bonus_paddle.rect.x <= 0:
                    bonus_paddle.move('right')
                if bonus_paddle.rect.x >= self.screen.get_width() - bonus_paddle.rect.width:
                    bonus_paddle.move('left')
                if bonus_paddle.rect.y <= 0:
                    bonus_paddle.move('down')
                if bonus_paddle.rect.y >= self.screen.get_height() - bonus_paddle.rect.height:
                    bonus_paddle.move('up')

            # check for bonus life collision with screen edges
            for bonus_life in self.bonus_lives:
                if bonus_life.rect.x <= 0:
                    bonus_life.move('right')
                if bonus_life.rect.x >= self.screen.get_width() - bonus_life.rect.width:
                    bonus_life.move('left')
                if bonus_life.rect.y <= 0:
                    bonus_life.move('down')
                if bonus_life.rect.y >= self.screen.get_height() - bonus_life.rect.height:
                    bonus_life.move('up')

            # check for paddle collision with screen edges
            if self.paddle.rect.x <= 0:
                self.paddle.move('right')
            if self.paddle.rect.x >= self.screen.get_width() - self.paddle.rect.width:
                self.paddle.move('left')

            # check for bonus life collision with screen edges
            for bonus_life in self.bonus_lives:
                if bonus_life.rect.x <= 0:
                    bonus_life.move('right')
                if bonus_life.rect.x >= self.screen.get_width() - bonus_life.rect.width:
                    bonus_life.move('left')

            # check for end of level
            if len(self.bricks) == 0:
                self.level += 1
                self.load_level()

            # check for game over
            if self.lives == 0:
                self.game_over()

            # draw background
            self.screen.fill(self.background_color)

            # draw bricks
            for brick in self.bricks:
                self.screen.blit(brick.image, brick.rect)

            # draw bonus bricks
            for bonus_brick in self.bonus_bricks:
                self.screen.blit(bonus_brick.image, bonus_brick.rect)

            # draw ball
            self.screen.blit(self.ball.image, self.ball.rect)

            # draw bonus balls
            for bonus_ball in self.bonus_balls:
                self.screen.blit(bonus_ball.image, bonus_ball.rect)

            # draw paddle
            self.screen.blit(self.paddle.image, self.paddle.rect)

            # draw bonus paddles
            for bonus_paddle in self.bonus_paddles:
                self.screen.blit(bonus_paddle.image, bonus_paddle.rect)

            # draw bonus lives
            for bonus_life in self.bonus_lives:
                self.screen.blit(bonus_life.image, bonus_life.rect)

            # draw score
            score_text = self.font.render('Score: ' + str(self.score), True, self.font_color)
            score_text_rect = score_text.get_rect()
            score_text_rect.x = 0
            score_text_rect.y = 0
            self.screen.blit(score_text, score_text_rect)

            # draw lives
            lives_text = self.font.render('Lives: ' + str(self.lives), True, self.font_color)
            lives_text_rect = lives_text.get_rect()
            lives_text_rect.x = self.screen.get_width() - lives_text_rect.width
            lives_text_rect.y = 0
            self.screen.blit(lives_text, lives_text_rect)

            # draw level
            level_text = self.font.render('Level: ' + str(self.level), True, self.font_color)
            level_text_rect = level_text.get_rect()
            level_text_rect.x = 0
            
            level_text_rect.y = self.screen.get_height() - level_text_rect.height
            self.screen.blit(level_text, level_text_rect)

            # draw player
            player_text = self.font.render('Player: ' + str(self.player), True, self.font_color)
            player_text_rect = player_text.get_rect()
            player_text_rect.x = self.screen.get_width() - player_text_rect.width
            player_text_rect.y = self.screen.get_height() - player_text_rect.height
            self.screen.blit(player_text, player_text_rect)

            # update screen
            pygame.display.update()

            # wait
            time.sleep(.01)

    #function to load levels
    def load_level(self):
        # check for level
        if self.level > LEVELS:
            self.game_over()
        else:
            # load level
            level_file = open('level' + str(self.level) + '.txt', 'r')
            level_file_lines = level_file.readlines()
            level_file.close()

            # get ball position
            ball_position = level_file_lines[0].split(' ')
            ball_position_x = int(ball_position[0])
            ball_position_y = int(ball_position[1])

            # get ball speed
            ball_speed = int(level_file_lines[1])

            # get ball direction
            ball_direction = level_file_lines[2].split(' ')
            ball_direction_x = int(ball_direction[0])
            ball_direction_y = int(ball_direction[1])

            # get paddle position
            paddle_position = level_file_lines[3].split(' ')
            paddle_position_x = int(paddle_position[0])
            paddle_position_y = int(paddle_position[1])

            # get paddle speed
            paddle_speed = int(level_file_lines[4])

            # get number of bricks
            number_of_bricks = int(level_file_lines[5])

            # get brick positions
            brick_positions = []
            for i in range(number_of_bricks):
                brick_position = level_file_lines[6 + i].split(' ')
                brick_position_x = int(brick_position[0])
                brick_position_y = int(brick_position[1])
                brick_positions.append((brick_position_x, brick_position_y))

            # get number of bonus bricks
            number_of_bonus_bricks = int(level_file_lines[6 + number_of_bricks])

            # get bonus brick positions
            bonus_brick_positions = []
            for i in range(number_of_bonus_bricks):
                bonus_brick_position = level_file_lines[7 + number_of_bricks + i].split(' ')
                bonus_brick_position_x = int(bonus_brick_position[0])
                bonus_brick_position_y = int(bonus_brick_position[1])
                bonus_brick_positions.append((bonus_brick_position_x, bonus_brick_position_y))

            # get bonus brick types
            bonus_brick_types = []
            for i in range(number_of_bonus_bricks):
                bonus_brick_type = level_file_lines[8 + number_of_bricks + number_of_bonus_bricks + i].split(' ')
                bonus_brick_types.append(bonus_brick_type[0])

            # set ball position
            self.ball.rect.x = ball_position_x
            self.ball.rect.y = ball_position_y

            # set ball speed
            self.ball.speed = ball_speed

            # set ball direction
            self.ball.direction = (ball_direction_x, ball_direction_y)

            # set paddle position
            self.paddle.rect.x = paddle_position_x
            self.paddle.rect.y = paddle_position_y

            # set paddle speed
            self.paddle.speed = paddle_speed

            # set bricks
            self.bricks = Group()
            for brick_position in brick_positions:
                brick_color = BRICK_COLORS[random.randint(0, len(BRICK_COLORS) - 1)]
                brick = Brick(brick_position[0], brick_position[1], BRICK_WIDTH, BRICK_HEIGHT, brick_color)
                self.bricks.add(brick)

            # set bonus bricks
            self.bonus_bricks = Group()
            for bonus_brick_position in bonus_brick_positions:
                bonus_brick_color = BONUS_COLORS[random.randint(0, len(BONUS_COLORS) - 1)]
                bonus_brick_type = bonus_brick_types[random.randint(0, len(bonus_brick_types) - 1)]
                bonus_brick = BonusBrick(bonus_brick_position[0], bonus_brick_position[1], BONUS_WIDTH, BONUS_HEIGHT, bonus_brick_color, bonus_brick_type)
                self.bonus_bricks.add(bonus_brick)

    #function to end game
    def game_over(self):
        # main loop
        while True:
            # check for quit
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # draw background
            self.screen.fill(self.background_color)

            # draw game over text
            game_over_font = pygame.font.Font(DEFAULT_FONT, self.game_over_font_size)
            game_over_text = game_over_font.render(self.game_over_text, True, self.game_over_color)
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.x = self.game_over_text_position[0] - game_over_text_rect.width/2
            game_over_text_rect.y = self.game_over_text_position[1] - game_over_text_rect.height/2
            self.screen.blit(game_over_text, game_over_text_rect)

            # update screen
            pygame.display.update()

            # wait
            time.sleep(.01)