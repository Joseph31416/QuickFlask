from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board, Pawn, BasePiece
from MoveHistory import MoveHistory

app = Flask(__name__)
ui = WebInterface()
game = Board()
movehistory = MoveHistory(10)

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

    if not game.new and not game.promote: 
        #Check that game is not in a new state, undo state, or promotion state
        move = request.form['move']

    elif game.promote:
        #Check if game is in promotion state
        move = None
        game.promotion = request.form['promote']

    else:
        #Assumes game is in new or undo state
        move = None
        game.new = False

    if move is None and game.promotion is None:
        #Check if game is in new or undo state
        ui.board = game.display()
        ui.inputlabel = f'{game.turn} player: '
        return render_template('chess.html', ui=ui)  
        
    elif game.promotion is not None:
        #check if game is in promotion state
        if game.promotion.lower() in 'kbrq':
            game.promotepawns(game.promotion.lower()) 
            game.next_turn()
            ui.inputlabel = f'{game.turn} player: '
            ui.board = game.display()
            game.promote = False
            game.promotion = None
            return render_template('chess.html', ui=ui) 
        else:
            return redirect('/play')

    
    else:
        #Assusmes game in standard play state
        game.inputmove = move
        v_move = game.prompt()
        
        if type(v_move) == tuple and len(v_move) == 2:
            start, end = v_move
            start_piece = game.get_piece(start)
            end_piece = game.get_piece(end)
            tuplee = (start,start_piece),(end,end_piece)
            movehistory.push((tuplee))
            movetype = game.movetype(start, end)
            # print(f'movetype: {movetype}')
            game.update(start, end)
            if game.winner is None:
                piece = game.get_piece(end)
                # print(f'MoveHistory: {movehistory.data}')
                if game.checkforpromotion():
                    return redirect('/promote')
                else:
                    game.next_turn()
                    ui.inputlabel = f'{game.turn} player: '
                    ui.board = game.display()
                    return render_template('chess.html', ui=ui)  
            else:
                game.reset()
                return render_template('winner.html')
        else:
            ui.errmsg = 'Invalid move. Please enter your move in the following format: __ __, _ represents a digit from 0-7.'
            return render_template('chess.html', ui=ui)

    # TODO: get player move from GET request object (Done)
    # TODO: if there is no player move, render the page template (Done)
    # TODO: Validate move, redirect player back to /play again if move is invalid (Done)
    # If move is valid, check for pawns to promote (Done)
    # Redirect to /promote if there are pawns to promote, otherwise (Done)

@app.route('/promote', methods=['POST', 'GET'])
def promote():
    '''
    if the pawn is at the end of the board
    can chose to promote the piece to a desired one
    '''
    ui.board = game.display()
    game.promote = True
    return render_template('promotion.html', ui=ui)

@app.route('/undo', methods=['POST', 'GET'])
def undo():
    if movehistory.head is not None:
        coord = movehistory.pop()
        # print(coord)
        start =coord[0][0]
        end = coord[1][0]
        start_piece = coord[0][1]
        end_piece = coord[1][1]

        # print(f'start_coord: {start}')
        # print(f'end_coord: {end}')
        # print(f'start_piece: {start_piece}')
        # print(f'end_piece: {end_piece}')
        # print(f'piece_at_end: {game.get_piece(end)}')

        if end_piece is None:
            # print(f'end_coord_in_if: {end}')
            game.remove(end)
            game.add(start, start_piece)

        else:
            game.add(start,end_piece)
            game.remove(end)
            game.add(end,start_piece)
        
        game.next_turn()

    game.new = True
    return  redirect('/play')

app.run('0.0.0.0')