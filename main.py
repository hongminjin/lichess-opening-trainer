from tkinter import *
from utils.board import Board, Color
from utils.lichess_opening import getmove

class Gui:
    
    def __init__(self):
        
        self.root = Tk()
        
        self.hw = 800
        
        # board canvas
        self.c = Canvas(self.root, height=self.hw, width=self.hw)
        self.c.pack()
        
        self.b = Board()
        
        self.images = {}
        self.load_images()
        
        self.moves = []
        self.url = "https://explorer.lichess.ovh/lichess?play={0}&speeds=bullet,blitz,rapid,classical&ratings=1800,2000,2200,2500&moves=500&topGames=0&recentGames=0"
        
        self.player = Color.W
        print("B/W?")
        if input().upper() != 'W':
            self.player = Color.B
            self.opponent_move()
        
        self.draw_board()
        self.draw_pieces()
        
        # main loop
        self.root.update_idletasks()
        self.root.update()
        fi = False
        while not fi:
            self.player_move()
            self.c.delete("piece")
            self.draw_pieces()
            self.root.update_idletasks()
            self.root.update()
            input()
            self.opponent_move()
            if self.moves[-1] != "end":
                self.c.delete("piece")
                self.draw_pieces()
                self.root.update_idletasks()
                self.root.update()
            else:
                input()
                fi = True
    
    def load_images(self):
        piecetypes = ['P','N','B','R','Q','K','p','n','b','r','q','k']
        for piece in piecetypes:
            color = 'w'
            if piece.islower():
                color = 'b'
            filename = "pieces/{0}{1}.gif".format(color, piece.upper())
            self.images[piece] = PhotoImage(file=filename)
    
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 0:
                    self.c.create_rectangle(i*(self.hw/8), j*(self.hw/8), (self.hw/8)*(i+1), (self.hw/8)*(j+1), fill="snow")
                else:
                    self.c.create_rectangle(i*(self.hw/8), j*(self.hw/8), (self.hw/8)*(i+1), (self.hw/8)*(j+1), fill="snow3")
    
    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.b.board[i][j]
                if piece != '*':
                    if self.player == Color.W:
                        self.c.create_image(j*(self.hw/8)+(self.hw/16), (7-i)*(self.hw/8)+(self.hw/16), image=self.images[piece], tags="piece")
                    else:
                        self.c.create_image((7-j)*(self.hw/8)+(self.hw/16), i*(self.hw/8)+(self.hw/16), image=self.images[piece], tags="piece")
    
    def opponent_move(self):
        move = getmove(self.url.format(','.join(self.moves)))
        self.moves.append(move)
        if move != "end":
            self.b.select_square(int(move[1])-1, ord(move[0])-ord('a'))
            self.b.select_square(int(move[3])-1, ord(move[2])-ord('a'))
            if len(move) == 5:
                self.b.set_promotion(move[4])
    
    def player_move(self):
        legalmove = False
        while not legalmove:
            move = input()
            if getmove(self.url.format(','.join(self.moves+[move]))) != "error":
                legalmove = True
                self.moves.append(move)
                self.b.select_square(int(move[1])-1, ord(move[0])-ord('a'))
                self.b.select_square(int(move[3])-1, ord(move[2])-ord('a'))
                if len(move) == 5:
                    self.b.set_promotion(move[4])
            else:
                print("illegal move")

if __name__ == '__main__':
    Gui()
