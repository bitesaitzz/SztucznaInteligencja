from copy import deepcopy


class AlphaBetaAgent:
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


    def decide(self, connect4) -> int:

        action = self.alphabeta(connect4, self.max_depth, self.my_token)

        return action


    def alphabeta(self, connect4, depth, player) -> int:
        if depth == 0 or connect4.game_over:
            return
        if connect4.who_moves == player:
            return self.alpha_value(connect4, depth, player, alpha=-10000, beta=10000)[1]
        else:
            return self.beta_value(connect4, depth, player,alpha=-10000, beta=10000)[1]

    def alpha_value(self,connect4, depth, player, alpha, beta):
        if depth == 0 or connect4.game_over:
            return self.static(connect4, player), None
        best_value = -1000000
        best_action = None

        for action in connect4.possible_drops():
            next_state = deepcopy(connect4)
            next_state.drop_token(action)
            value = self.beta_value(next_state, depth-1, player, alpha, beta)[0]
            if (value > best_value):
                best_value = value
                best_action = action
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_value, best_action

    def beta_value(self, connect4, depth, player, alpha, beta):
        if depth == 0 or connect4.game_over:
            return self.static(connect4, player), None
        best_value = 100000
        best_action = None
        for action in connect4.possible_drops():
            next_state = deepcopy(connect4)
            next_state.drop_token(action)
            value = self.alpha_value(next_state, depth-1, player, alpha, beta)[0]
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, value)
            if alpha >= beta:
                break




        return best_value, best_action


