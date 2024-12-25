class NycharanXOGame:
    def __init__(self):
        self.game_dim = 3
        self.game_space = [[None for _ in range(self.game_dim)] for _ in range(self.game_dim)]
        self.players= [0, 1]
        self.player_turn = 0

    def reset(self):
        self.game_space = [[None for _ in range(self.game_dim)] for _ in range(self.game_dim)]
        self.player_turn = 0

    def fetch_game(self):
        def calc_score(line):
            for i in range(len(line) - 1):
                score = 0
                counter = 0

                if line[i] == line[i + 1] == self.player_turn:
                    counter += 1
                else:
                    if counter > 2:
                        score += (counter - 2) + (counter - 3)
            return score

        for i in range(self.game_dim):
            calc_score(self.game_space[i])
            calc_score([j[i] for j in self.game_space])

        for k in range(2*self.game_dim -1):
            calc_score([self.game_space[i][j] for i in range(self.game_dim) if 0 <= (j := k - i) < self.game_dim])
            calc_score([self.game_space[i][j] for i in range(self.game_dim) if 0 <= (j := i + k - self.game_dim + 1) < self.game_dim])

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
                max_score = float('-inf')
                for i in range(self.game_dim):
                    for j in range(self.game_dim):
                        if game_space[i][j] == None:
                            game_space[i][j] = self.players[1]
                            score = minimax(game_space, False)
                            game_space[i][j] = None
                            max_score = max(max_score, score)
                return max_score
            else:
                max_score = float('-inf')
                for i in range(self.game_dim):
                    for j in range(self.game_dim):
                        if game_space[i][j] == None:
                            game_space[i][j] = self.players[0]
                            score = minimax(game_space, True)
                            game_space[i][j] = None
                            max_score = min(max_score, score)
                return max_score

        max_score = float('-inf')
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