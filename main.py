from tkinter import *
from utils.board import Board
from utils.lichess_opening import getmove

class Gui:
    
    def __init__(self):
        
        self.root = Tk()
        
        self.hw = 800 # board size
        
        # board canvas
        self.c = Canvas(self.root, height=self.hw, width=self.hw)
        self.c.bind("<Button-1>", self.player_move)
        self.c.pack()
        
        self.b = Board()
        
        self.images = {}
        self.load_images()
        
        self.moves = [] # list of played moves
        self.pgn = [] # Game PGN
        self.pmove = "" # player's move
        self.lastmove = ""
        
        # lichess API
        self.url = "https://explorer.lichess.ovh/lichess?play={0}&speeds=bullet,blitz,rapid,classical&ratings=1800,2000,2200,2500&moves=500&topGames=0&recentGames=0"
        
        self.flip = False # flip board
        
        # Get move, flip board and restart buttons
        Button(self.root, text = "Get Move", command = self.opponent_move).pack(side=LEFT)
        Button(self.root, text = "Flip Board", command = self.flip_board).pack(side=LEFT)
        Button(self.root, text = "Restart", command = self.restart_game).pack(side=LEFT)
        
        # Promotion radiobutton
        self.promotion = StringVar(self.root, "q")
        values = {"Queen" : "q", "Knight" : "n", "Bishop" : "b", "Rook" : "r"}
        Label(self.root, text = "Type of promoted piece:").pack(side=LEFT)
        for (text, value) in values.items():
            Radiobutton(self.root, text = text, variable = self.promotion, value = value).pack(side=LEFT)
        
        self.draw_board()
        self.draw_pieces()
        
        # main loop
        self.root.mainloop()
    
    # initialize images of pieces
    def load_images(self):
        piecetypes = ['P','N','B','R','Q','K','p','n','b','r','q','k']
        for piece in piecetypes:
            color = 'w'
            if piece.islower():
                color = 'b'
            filename = "pieces/{0}{1}.gif".format(color, piece.upper())
            self.images[piece] = PhotoImage(file=filename)
    
    # highlight square (i, j) of the board if it is selected by player or by the last move
    def highlight(self, i, j):
        
        if self.flip:
            if len(self.pmove) > 0 and i == ord('h')-ord(self.pmove[0]) and j == int(self.pmove[1])-1:
                return True
            if len(self.lastmove) > 0:
                if i == ord('h')-ord(self.lastmove[0]) and j == int(self.lastmove[1])-1:
                    return True
                if i == ord('h')-ord(self.lastmove[2]) and j == int(self.lastmove[3])-1:
                    return True
            return False
        
        if len(self.pmove) > 0 and i == ord(self.pmove[0])-ord('a') and j == 8-int(self.pmove[1]):
            return True
        if len(self.lastmove) > 0:
            if i == ord(self.lastmove[0])-ord('a') and j == 8-int(self.lastmove[1]):
                return True
            if i == ord(self.lastmove[2])-ord('a') and j == 8-int(self.lastmove[3]):
                return True
        return False
    
    # draw the chess board
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 0:
                    fillcolor = "snow"
                    if (self.highlight(i, j)):
                        fillcolor = "palegreen"
                    self.c.create_rectangle(i*(self.hw/8), j*(self.hw/8), (self.hw/8)*(i+1), (self.hw/8)*(j+1), fill=fillcolor, tags="square")
                else:
                    fillcolor = "snow3"
                    if (self.highlight(i, j)):
                        fillcolor = "lime"
                    self.c.create_rectangle(i*(self.hw/8), j*(self.hw/8), (self.hw/8)*(i+1), (self.hw/8)*(j+1), fill=fillcolor, tags="square")
    
    # draw chess pieces
    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.b.board[i][j]
                if piece != '*':
                    if not self.flip:
                        self.c.create_image(j*(self.hw/8)+(self.hw/16), (7-i)*(self.hw/8)+(self.hw/16), image=self.images[piece], tags="piece")
                    else:
                        self.c.create_image((7-j)*(self.hw/8)+(self.hw/16), i*(self.hw/8)+(self.hw/16), image=self.images[piece], tags="piece")
    
    # refresh chess board
    def refresh(self):
        self.c.delete("piece")
        self.c.delete("square")
        self.draw_board()
        self.draw_pieces()
    
    # flip board
    def flip_board(self):
        self.flip = not self.flip
        self.refresh()
    
    # start a new game
    def restart_game(self):
        print(' '.join(self.pgn))
        self.moves = []
        self.pgn = []
        self.pmove = ""
        self.lastmove = ""
        self.b.initialize()
        self.refresh()
    
    # make a move and update chess board
    def make_move(self, move):
        self.moves.append(move)
        piecetype = self.b.board[int(move[1])-1][ord(move[0])-ord('a')].upper()
        if piecetype == 'K':
            if ord(move[2]) - ord(move[0]) >= 2:
                self.pgn.append("O-O")
            elif ord(move[0]) - ord(move[2]) >= 2:
                self.pgn.append("O-O-O")
            else:
                self.pgn.append(piecetype+move)
        else:
            mv = piecetype+move[0:4]
            if len(move) == 5:
                mv = mv + move[4].upper()
            self.pgn.append(mv)
        if len(move) == 5:
            self.b.set_promotion(move[4])
        self.b.select_square(int(move[1])-1, ord(move[0])-ord('a'))
        self.b.select_square(int(move[3])-1, ord(move[2])-ord('a'))
        self.lastmove = move
        self.refresh()
    
    # get a move from lichess opening explorer
    def opponent_move(self):
        move = getmove(self.url.format(','.join(self.moves)))
        self.pmove = ""
        if move != "end" and move != "error":
            self.make_move(move)
        else:
            self.restart_game()
    
    # convert coordinates of click (x, y) to algebraic notation
    def get_coordinates(self, x, y):
        i = int(x/100)
        j = int(y/100)
        if self.flip:
            return chr(ord('a')+7-i) + str(j+1)
        return chr(ord('a')+i) + str(7-j+1)
    
    # get player's move by mouse click
    def player_move(self, event):
        
        self.pmove = self.pmove + self.get_coordinates(event.x, event.y)
        move = self.pmove
        
        if len(move) == 4:
            # add the type of promoted piece if necessary
            piecetype = self.b.board[int(move[1])-1][ord(move[0])-ord('a')].upper()
            if piecetype == 'P' and (move[3] == '1' or move[3] == '8'):
                move = move + self.promotion.get()
            # check if the move is legal
            if getmove(self.url.format(','.join(self.moves+[move]))) != "error":
                self.make_move(move)
            else:
                print("illegal move")
            self.pmove = ""
        
        self.refresh()

if __name__ == '__main__':
    Gui()
