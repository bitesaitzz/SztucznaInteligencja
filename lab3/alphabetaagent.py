from copy import deepcopy


class AlphaBetaAgent:
    def static(self, connect4, player):
        wynik = 0
        all_posible = 0
        opponent = 'o' if player == 'x' else 'x'
        for four in connect4.iter_fours():
            if (four.count(player) == 3):
                wynik += 2
                all_posible += 2
            elif (four.count(player) == 4):
                return 1
            elif (four.count(player) == 2):
                wynik += 1
                all_posible += 1
            if (four.count(opponent) == 3):
                wynik -= 2
                all_posible += 2
            elif (four.count(opponent) == 4):
                return -1
            elif (four.count(opponent) == 2):
                wynik -= 1
                all_posible += 1

        if (all_posible == 0):
            return 0
        return wynik / all_posible


    def __init__(self, my_token ,max_depth=4):
        self.my_token = my_token
        self.max_depth = max_depth

    def result(self, connect4, player):
        opponent = 'o' if player == 'x' else 'x'
        if connect4.wins == player:
            return 1
        elif connect4.wins == opponent:
            return -1
        else:
            return 0
    def decide(self, connect4) -> int:
        if self.max_depth == 0 or connect4.game_over:
            return
        # action = self.alphabeta(connect4, self.max_depth, self.my_token)

        return self.alpha_value(connect4, self.max_depth, self.my_token, alpha=-10000, beta=10000)[1]


    def alpha_value(self,connect4, depth, player, alpha, beta):
        if depth == 0:
            return self.static(connect4, player), None
        if connect4.game_over == True:
            return self.result(connect4, player), None
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
        if depth == 0:
            return self.static(connect4, player), None
        if connect4.game_over == True:
            return self.result(connect4, player), None
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


