from copy import deepcopy

from connect4 import Connect4
from exceptions import AgentException


class MinMaxAgent:

    def static(self, connect4, player):
        player_fours = 0
        for four in connect4.iter_fours():
            if four == [player, player, player, player]:
                player_fours += 1

        opponent = 'o' if player == 'x' else 'x'
        opponent_fours = 0
        for four in connect4.iter_fours():
            if four == [opponent, opponent, opponent, opponent]:
                opponent_fours += 1

        return player_fours - opponent_fours


    def __init__(self, my_token ,max_depth=4):
        self.my_token = my_token
        self.max_depth = max_depth


    def decide(self, connect4: Connect4) -> int:

        action = self.minmax(connect4, self.max_depth, self.my_token)

        return action


    def minmax(self, connect4: Connect4, depth, player) -> int:
        if depth == 0 or connect4.game_over:
            return
        if connect4.who_moves == player:
            return self.max_value(connect4, depth, player)[1]
        else:
            return self.min_value(connect4, depth, player)[1]

    def max_value(self,connect4: Connect4, depth, player) -> tuple[float, int]:
        if depth == 0 or connect4.game_over:
            return self.static(connect4, player), None
        best_value = -1000000
        best_action = None

        for action in connect4.possible_drops():
            next_state = deepcopy(connect4)
            next_state.drop_token(action)
            value = self.min_value(next_state, depth-1, player)[0]
            if (value > best_value):
                best_value = value
                best_action = action

        return best_value, best_action

    def min_value(self, connect4, depth, player) -> tuple[float, int]:
        if depth == 0 or connect4.game_over:
            return self.static(connect4, player), None
        best_value = 100000
        best_action = None
        for action in connect4.possible_drops():
            next_state = deepcopy(connect4)
            next_state.drop_token(action)
            value = self.max_value(next_state, depth-1, player)[0]
            if (value < best_value):
                best_value = value
                best_action = action

        return best_value, best_action


