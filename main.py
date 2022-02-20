from tkinter import *
from utils.board import Board, Color
from utils.lichess_opening import getmove

class Gui:
    
    def __init__(self):
        
        self.root = Tk()
        
        self.hw = 800
        
        # board canvas
        self.c = Canvas(self.root, height=self.hw, width=self.hw)
        self.c.bind("<Button-1>", self.player_move)
        self.c.pack()
        
        self.b = Board()
        
        self.images = {}
        self.load_images()
        
        self.moves = []
        self.pmove = ""
        self.url = "https://explorer.lichess.ovh/lichess?play={0}&speeds=bullet,blitz,rapid,classical&ratings=1800,2000,2200,2500&moves=500&topGames=0&recentGames=0"
        
        self.flip = False
        
        self.promotion = "q"
        
        self.move_button = Button(self.root, text = "Get Move", command = self.opponent_move)
        self.flip_button = Button(self.root, text = "Flip Board", command = self.flip_board)
        self.restart_button = Button(self.root, text = "Restart", command = self.restart_game)
        self.move_button.pack()
        self.flip_button.pack()
        self.restart_button.pack()
        
        self.draw_board()
        self.draw_pieces()
        
        # main loop
        self.root.mainloop()
    
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
                    self.c.create_rectangle(i*(self.hw/8), j*(self.hw/8), (self.hw/8)*(i+1), (self.hw/8)*(j+1), fill="snow", tags="square")
                else:
                    self.c.create_rectangle(i*(self.hw/8), j*(self.hw/8), (self.hw/8)*(i+1), (self.hw/8)*(j+1), fill="snow3", tags="square")
    
    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.b.board[i][j]
                if piece != '*':
                    if not self.flip:
                        self.c.create_image(j*(self.hw/8)+(self.hw/16), (7-i)*(self.hw/8)+(self.hw/16), image=self.images[piece], tags="piece")
                    else:
                        self.c.create_image((7-j)*(self.hw/8)+(self.hw/16), i*(self.hw/8)+(self.hw/16), image=self.images[piece], tags="piece")
    
    def refresh(self):
        self.c.delete("piece")
        self.c.delete("square")
        self.draw_board()
        self.draw_pieces()
    
    def flip_board(self):
        self.flip = not self.flip
        self.refresh()
    
    def restart_game(self):
        print(self.url.format(','.join(self.moves)))
        self.moves = []
        self.pmove = ""
        self.b.initialize()
        self.refresh()
    
    def opponent_move(self):
        move = getmove(self.url.format(','.join(self.moves)))
        self.pmove = ""
        if move != "end":
            self.moves.append(move)
            if len(move) == 5:
                self.b.set_promotion(move[4])
            self.b.select_square(int(move[1])-1, ord(move[0])-ord('a'))
            self.b.select_square(int(move[3])-1, ord(move[2])-ord('a'))
            self.refresh()
        else:
            self.restart_game()
    
    def get_coordinates(self, x, y):
        i = int(x/100)
        j = int(y/100)
        if self.flip:
            return chr(ord('a')+7-i) + str(j+1)
        return chr(ord('a')+i) + str(7-j+1)
    
    def player_move(self, event):
        self.pmove = self.pmove + self.get_coordinates(event.x, event.y)
        move = self.pmove
        if len(move) == 4:
            piecetype = self.b.board[int(move[1])-1][ord(move[0])-ord('a')].upper()
            if piecetype == 'P' and (move[3] == '1' or move[3] == '8'):
                move = move + self.promotion
            if getmove(self.url.format(','.join(self.moves+[move]))) != "error":
                self.moves.append(move)
                if len(move) == 5:
                    self.b.set_promotion(move[4])
                self.b.select_square(int(move[1])-1, ord(move[0])-ord('a'))
                self.b.select_square(int(move[3])-1, ord(move[2])-ord('a'))
                self.refresh()
            else:
                print("illegal move")
            self.pmove = ""

if __name__ == '__main__':
    Gui()
