class NycharanXOGame:
    def __init__(self):
        self.game_dim = 3
        self.game_space = [[None for _ in range(self.game_dim)] for _ in range(self.game_dim)]
        self.players= [0, 1]
        self.player_turn = 0

    def reset(self):
        self.game_space = [[None for _ in range(self.game_dim)] for _ in range(self.game_dim)]
        self.player_turn = 0
        
    # turn this into calc_score function coz in 'NycharanXOGame' winner gets the more score than other player
    
    def check_winner(self):
        for i in range(self.game_dim):
            if all(self.game_space[i][j] == self.game_space[i][0] for j in range(1,self.game_dim)) and self.game_space[i][0] != None:
                return self.game_space[i][0]
            if all(self.game_space[j][i] == self.game_space[0][i] for j in range(1,self.game_dim)) and self.game_space[0][i] != None:
                return self.game_space[0][i]

        if all(self.game_space[j][j] == self.game_space[0][0] for j in range(1,self.game_dim)) and self.game_space[0][0] != None:
            return self.game_space[0][0]
        if all(self.game_space[j][i] if i+j == (self.game_dim - 1) else -1 == self.game_space[0][(self.game_dim - 1)] for j in range(1,self.game_dim)) and self.game_space[0][(self.game_dim - 1)] != None:
            return self.game_space[0][(self.game_dim - 1)]

        for row in self.game_space:
            if None in row:
                return None

        return "Tie"

    def apply_move(self, row, col):
        if self.game_space[row][col] != None:
            raise ValueError("square is taken before make another move!")

        self.game_space[row][col] = self.players[self.player_turn]

    def switch_player(self):
        self.player_turn = 1 - self.player_turn

    def best_approach(self):
        def minimax(game_space, maximize):
            winner = self.check_winner()
            if winner == self.players[1]:
                return 1
            elif winner == self.players[0]:
                return -1
            elif winner == "Tie":
                return 0

            if maximize:
                max_score = -1
                for i in range(self.game_dim):
                    for j in range(self.game_dim):
                        if game_space[i][j] == None:
                            game_space[i][j] = self.players[1]
                            score = minimax(game_space, False)
                            game_space[i][j] = None
                            max_score = max(max_score, score)
                return max_score
            else:
                max_score = -1
                for i in range(self.game_dim):
                    for j in range(self.game_dim):
                        if game_space[i][j] == None:
                            game_space[i][j] = self.players[0]
                            score = minimax(game_space, True)
                            game_space[i][j] = None
                            max_score = min(max_score, score)
                return max_score

        max_score = -1
        max_move = (-1, -1)
        for i in range(self.game_dim):
            for j in range(self.game_dim):
                if self.game_space[i][j] == None:
                    self.game_space[i][j] = self.players[1]
                    score = minimax(self.game_space, False)
                    self.game_space[i][j] = None
                    if score > max_score:
                        max_score = score
                        max_move = (i, j)
        return max_move

game = NycharanXOGame()