from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        """Initialize the Tic-Tac-Toe game."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.current_player = 0

    def reset(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = 0

    def check_winner(self):
        """Checks if there is a winner or a draw."""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]  # Row winner
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]  # Column winner

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        for row in self.board:
            if " " in row:
                return None  # Game is still ongoing

        return "Draw"  # No spaces left and no winner

    def make_move(self, row, col):
        """Handles a player's move."""
        if self.board[row][col] != " ":
            raise ValueError("Cell is already occupied!")

        self.board[row][col] = self.players[self.current_player]

    def switch_player(self):
        """Switches to the next player."""
        self.current_player = 1 - self.current_player

    def find_best_move(self):
        """Finds the best move for the AI using Minimax."""
        def minimax(board, is_maximizing):
            winner = self.check_winner()
            if winner == self.players[1]:
                return 1
            elif winner == self.players[0]:
                return -1
            elif winner == "Draw":
                return 0

            if is_maximizing:
                best_score = float('-inf')
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == " ":
                            board[i][j] = self.players[1]
                            score = minimax(board, False)
                            board[i][j] = " "
                            best_score = max(best_score, score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == " ":
                            board[i][j] = self.players[0]
                            score = minimax(board, True)
                            board[i][j] = " "
                            best_score = min(best_score, score)
                return best_score

        best_score = float('-inf')
        best_move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = self.players[1]
                    score = minimax(self.board, False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

# Initialize game
game = TicTacToe()

@app.route('/')
@app.route('/')
def index():
    # Prepare the board with indices
    board_with_indices = [
        [{"value": cell, "row": i, "col": j} for j, cell in enumerate(row)]
        for i, row in enumerate(game.board)
    ]
    return render_template(
        'index.html',
        board=board_with_indices,
        current_player=game.players[game.current_player]
    )

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    row, col = data['row'], data['col']

    try:
        game.make_move(row, col)
        winner = game.check_winner()
        if not winner:
            game.switch_player()
            if game.current_player == 1:  # AI's turn
                ai_move = game.find_best_move()
                game.make_move(ai_move[0], ai_move[1])
                winner = game.check_winner()
                if not winner:
                    game.switch_player()

        return jsonify({
            'board': game.board,
            'winner': winner,
            'current_player': game.players[game.current_player]
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/restart', methods=['POST'])
def restart():
    # Reset the game board and state
    global game
    game.reset()  # Assuming there's a reset method in your game class
    return '', 204  # Respond with no content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)