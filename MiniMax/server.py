from source import TicTacToe
from flask import Flask, render_template, request, jsonify

# Initialize game
game = TicTacToe()

app = Flask(__name__)

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
        player_turn=game.players[game.player_turn]
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
            if game.player_turn == 1:  # AI's turn
                ai_move = game.find_best_move()
                game.make_move(ai_move[0], ai_move[1])
                winner = game.check_winner()
                if not winner:
                    game.switch_player()

        return jsonify({
            'board': game.board,
            'winner': winner,
            'player_turn': game.players[game.player_turn]
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