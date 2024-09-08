from turtle import Turtle, Screen
import random
import numpy as np

class AIgame:
    def __init__(self, w=700, h=700):
        # initialise screen
        self.screen = Screen()
        self.screen.setup(w, h)

        # initialise player turtle
        self.player = Turtle()
        self.player.speed(0)
        self.player.pu()
        self.player.shape('square')
        self.player.shapesize(2, 2)
        self.player.color('blue')

        # initialise food turtle
        self.food = Turtle()
        self.food.shape('square')
        self.food.shapesize(2, 2)
        self.food.color('red')

        # resets game
        self.reset()

    def reset(self):
        self.player.teleport(0, 0)
        self.move_food()
        self.game_iter = 0
        self.score = 0

    def out_of_bounds(self, x, y):
        if x > 325 or x < -325 or y > 325 or y < -325:
            return True
        else:
            return False

    def move_food(self):
        case = random.randint(0, 4)
        if case == 0:
            x = random.randrange(160, 321, 40)
            y = random.randrange(-320, 321, 40)
        elif case == 1:
            x = random.randrange(-320, -159, 40)
            y = random.randrange(-320, 321, 40)
        elif case == 2:
            x = random.randrange(-320, 321, 40)
            y = random.randrange(160, 321, 40)
        else:
            x = random.randrange(-320, 321, 40)
            y = random.randrange(-320, -159, 40)
        self.food.teleport(x, y)

    def play_step(self, action):
        self.game_iter += 1
        
        # moves player body
        self.move(action) 
        
        # player coordinates
        x = round(self.player.xcor())
        y = round(self.player.ycor())

        # food coordinates
        X = round(self.food.xcor())
        Y = round(self.food.ycor())

        game_over = False
        if self.out_of_bounds(x, y) or self.game_iter > 800: 
            game_over = True
            return game_over, self.score

        # checks if player connects with food
        if X-10<x<X+10 and Y-10<y<Y+10:
            self.score += 1
            self.game_iter = 0
            self.move_food()

        # high score cap
        if self.score == 5000:
            game_over = True

        return game_over, self.score

    def move(self, action):
        if np.array_equal(action, [0, 1, 0]): # turn right
            self.player.right(90)
            self.player.fd(40)
        elif np.array_equal(action, [0, 0, 1]): # turn left
            self.player.left(90)
            self.player.fd(40)
        elif np.array_equal(action, [1, 0, 0]): # go straight
            self.player.fd(40)