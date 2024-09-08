import torch
import numpy as np
import random
from game import AIgame
from model import Linear_QNet


# games to complete
ROUNDS = 10

class Agent:
    def __init__(self):
        self.n_games = 0

    def get_state(self, game):

        # gets agent coordinates
        y = game.player.ycor()
        x = game.player.xcor()

        # gets agent direction 
        dir = game.player.heading() 
        # RIGHT = 0, LEFT = 180, UP = 90, DOWN = 270

        dir_l = dir == 180
        dir_r = dir == 0
        dir_u = dir == 90
        dir_d = dir == 270

        state = [
            # Danger straight
            (dir_r and game.out_of_bounds(x+40, y)) or 
            (dir_l and game.out_of_bounds(x-40, y)) or 
            (dir_u and game.out_of_bounds(x, y+40)) or 
            (dir_d and game.out_of_bounds(x, y-40)),

            # Danger right
            (dir_u and game.out_of_bounds(x+40, y)) or 
            (dir_d and game.out_of_bounds(x-40, y)) or 
            (dir_l and game.out_of_bounds(x, y+40)) or 
            (dir_r and game.out_of_bounds(x, y-40)),

            # Danger left
            (dir_d and game.out_of_bounds(x+40, y)) or 
            (dir_u and game.out_of_bounds(x-40, y)) or 
            (dir_r and game.out_of_bounds(x, y+40)) or 
            (dir_l and game.out_of_bounds(x, y-40)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.xcor() < x,  # food left
            game.food.xcor() > x,  # food right
            game.food.ycor() > y,  # food up
            game.food.ycor() < y,  # food down
            game.food.xcor() == x, # food on same x axis
            game.food.ycor() == y  # food on same y axis
            ]

        return np.array(state, dtype=int)

    def get_action(self, state, model):
        final_move = [0, 0, 0]

        # converts the agent state into a tensor
        state0 = torch.tensor(state, dtype=torch.float)

        # predicts the agent next move
        prediction = model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

        return final_move


def play():
    # initiate a model, then load the best model weights in it
    model = Linear_QNet(13, 256, 3)
    model.load_state_dict(torch.load(f='../model/ft3_0.pth'))
    agent = Agent()
    game = AIgame()

    # initialise game loop
    while ROUNDS != agent.n_games:
        # set screen title
        game.screen.title(f'Score: {game.score}  Game: {agent.n_games}')

        # get current state
        state_old = agent.get_state(game)

        # get next move
        final_move = agent.get_action(state_old, model)

        # perform move and get new state
        done, score = game.play_step(final_move)

        if done:
            agent.n_games += 1
            print(f"Game {agent.n_games:02}/{ROUNDS}: score - {game.score}/5000")
            game.reset()


if __name__ == '__main__':
    play()
