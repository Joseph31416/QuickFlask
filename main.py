from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board

app = Flask(__name__)
ui = WebInterface()
game = Board()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    game.start()
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    ui.btnlabel = 'Move'
    return redirect('/play')

@app.route('/play', methods=['POST', 'GET'])
def play():
    ui.errmsg = None
    if not game.new:
        move = request.form['move']
    else:
        move = None
        game.new = False
    if move is None:
        return render_template('chess.html', ui=ui)  
    else:
        game.inputmove = move
        v_move = game.prompt()
        
        if type(v_move) == tuple and len(v_move) == 2:
            start, end = v_move
            game.update(start, end)
            piece = game.get_piece(end)
            
            if game.checkforpromotion():
                return redirect('/promote')
                
                
            else:
                game.next_turn()
                ui.inputlabel = f'{game.turn} player: '
                ui.board = game.display()
                return render_template('chess.html', ui=ui)  
        else:
            ui.errmsg = 'Invalid move. Please enter your move in the following format: __ __, _ represents a digit from 0-7.'
            return render_template('chess.html', ui=ui)

    # TODO: get player move from GET request object (Done)
    # TODO: if there is no player move, render the page template (Done)
    # TODO: Validate move, redirect player back to /play again if move is invalid (Done)
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    '''
    if the pawn is at the end of the board
    can chose to promote the piece to a desired one
    '''
    ui.errmsg = 'It works i guess'
    return render_template('chess.html', ui=ui)

app.run('0.0.0.0')