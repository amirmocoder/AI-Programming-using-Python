class NycharanXOGame:
    def __init__(self):
        self.game_dim = 3
        self.game_space = [[" " for _ in range(self.game_dim)] for _ in range(self.game_dim)]
        self.players= ["X", "O"]
        self.player_turn = 0
        self.players_score = {self.players[0] : 0, self.players[1] : 0}

    def show_game(self):
        for row in self.game_space:
            print(" | ".join(row))
            print("-" * (self.game_dim * 3 - 1))

    def reset(self):
        self.game_space = [[" " for _ in range(self.game_dim)] for _ in range(self.game_dim)]
        self.players_score = {self.players[0] : 0, self.players[1] : 0}
        self.player_turn = 0

    def switch_player(self):
        self.player_turn = 1 - self.player_turn

    def calc_score(self):
        self.players_score = {self.players[0] : 0, self.players[1] : 0}

        def count_score(line):
            for player in self.players:
                score = 0
                counter = 0

                for i in range(len(line) - 1):
                    if line[i] == line[i + 1] == player:
                        counter += 1
                    else:
                        if counter > 2:
                            score += (counter - 2) + (counter - 3)
                            counter = 0
                self.players_score[player] += score

        for i in range(self.game_dim):
            count_score(self.game_space[i])
            count_score([j[i] for j in self.game_space])

        for k in range(2*self.game_dim -1):
            count_score([self.game_space[i][j] for i in range(self.game_dim) if 0 <= (j := k - i) < self.game_dim])
            count_score([self.game_space[i][j] for i in range(self.game_dim) if 0 <= (j := i + k - self.game_dim + 1) < self.game_dim])

    def make_move(self, row, col):
        def check_validation():
            return 0 <= row < self.game_dim and 0 <= col < self.game_dim and self.game_space[row][col] == " "
        if check_validation():
            self.game_space[row][col] = self.players[self.player_turn]
            self.calc_score()
            return True
        return 'Invalid input Try again!'

    def best_approach(self):
        def minimax(maximize = True, alpha = float('-inf'), beta = float('inf'), depth = 6):
            for row in self.game_space:
                if " " not in row:
                    return self.players_score[self.players[0]] - self.players_score[self.players[1]] 
                
            if maximize:
                max_score = float('-inf')
                for i in range(self.game_dim):
                    for j in range(self.game_dim):
                        if self.game_space[i][j] == " ":
                            self.game_space[i][j] = self.players[1]
                            self.calc_score()
                            score = minimax(False, alpha, beta, depth + 1)
                            self.game_space[i][j] = " "
                            self.calc_score()
                            max_score = max(max_score, score)
                            alpha = max(alpha, score)
                            if beta <= alpha:
                                break
                return max_score
            else:
                max_score = float('inf')
                for i in range(self.game_dim):
                    for j in range(self.game_dim):
                        if self.game_space[i][j] == " ":
                            self.game_space[i][j] = self.players[0]
                            self.calc_score()
                            score = minimax(True, alpha, beta, depth + 1)
                            self.game_space[i][j] = " "
                            self.calc_score()
                            max_score = min(max_score, score)
                            beta = min(beta, score)
                            if beta <= alpha:
                                break
                return max_score

        max_score = float('-inf')
        best_move = (-1, -1)
        for i in range(self.game_dim):
            for j in range(self.game_dim):
                if self.game_space[i][j] == " ":
                    self.game_space[i][j] = self.players[1]
                    self.calc_score()
                    score = minimax(False, float('-inf'), float('inf'), 0)
                    self.game_space[i][j] = " "
                    self.calc_score()
                    if score > max_score:
                        max_score = score
                        best_move = (i, j)
        return best_move

# Game
if __name__ == "__main__":
    game = NycharanXOGame()

    while True:
        game.show_game()
        print(f"Scores: X = {game.players_score["X"]}, O = {game.players_score["O"]}")

        if game.player_turn == 0:
            print("X's turn.")
            row, col = map(int, input(f"Enter row and column (0-{game.game_dim - 1}, space-separated): ").split())
            game.make_move(row, col)
            game.switch_player()
        else:
            print("O's turn.")
            row, col = game.best_approach()
            game.make_move(row, col)
            print(f"Machine chooses: {row}, {col}")
            game.switch_player()

        if " " not in [cell for row in game.game_space for cell in row]:
            print("Game is over!")
            game.show_game()
            print(f"Final Scores: X = {game.players_score["X"]}, O = {game.players_score["O"]}")
            winner = "Tie" if game.players_score["X"] == game.players_score["O"] else "X" if game.players_score["X"] > game.players_score["O"] else "O"
            print(f"Winner is: {winner}")
            break