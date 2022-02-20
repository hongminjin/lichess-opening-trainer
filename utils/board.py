from enum import Enum

class Color(Enum):
    W = 0 # white
    B = 1 # black
    E = 2 # empty

# chess board
class Board:
    
    def __init__(self):
        self.initialize()
    
    # get color of a piece
    @staticmethod
    def get_color(p):
        if p == '*':
            return Color.E
        if p.isupper():
            return Color.W
        return Color.B
    
    # check if a pawn in (px, py) controls (x, y)
    @staticmethod
    def p_control(px, py, x, y, white):
        if white:
            return x-px == 1 and abs(y-py) == 1
        return px-x == 1 and abs(y-py) == 1
    
    # check if a knight in (px, py) controls (x, y)
    @staticmethod
    def k_control(px, py, x, y):
        return abs(x-px)+abs(y-py) == 3 and abs(x-px) > 0 and abs(y-py) > 0
    
    # check if a bishop in (px, py) controls (x, y)
    @staticmethod
    def b_control(px, py, x, y):
        return abs(x-px) == abs(y-py) and abs(x-px) > 0
    
    # check if a rook in (px, py) controls (x, y)
    @staticmethod
    def r_control(px, py, x, y):
        return x == px ^ y == py
    
    # check if a queen in (px, py) controls (x, y)
    @staticmethod
    def q_control(px, py, x, y):
        return b_control(px, py, x, y) or r_control(px, py, x, y)
    
    # check if a king in (px, py) controls (x, y)
    @staticmethod
    def k_control(px, py, x, y):
        return abs(x-px) <= 1 and abs(y-py) <= 1 and (x != px or y != py)
    
    # initialize board
    def initialize(self):
        
        self.turn = Color.W # white to play
        
        # castle for white and black
        self.w00 = True
        self.w000 = True
        self.b00 = True
        self.b000 = True
        
        self.moves = 1
        self.enpassant = -1 # en passant file
        
        # initial configuration of 8x8 board
        self.board = [['*' for j in range(8)] for i in range(8)]
        self.board[0] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for i in range(8):
            self.board[1][i] = 'P'
        self.board[7] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        for i in range(8):
            self.board[6][i] = 'p'
        
        # current selected square
        self.selectedx = -1
        self.selectedy = -1
        
        # coordinates of the king
        self.whitekingx = 0
        self.whitekingy = 4
        self.blackkingx = 7
        self.blackkingy = 4
        
        # type of promoted piece
        self.promotion = 'Q'
    
    # set the type of promoted piece
    def set_promotion(self, p):
        self.promotion = p.upper()
    
    # select initial square or destination square of a move
    def select_square(self, x, y):
        if self.selectedx == -1 and self.selectedy == -1:
            self.selectedx = x
            self.selectedy = y
        else:
            if self.make_move(self.selectedx, self.selectedy, x, y):
                if self.turn == Color.W:
                    self.turn = Color.B
                else:
                    self.turn = Color.W
                    self.moves = self.moves + 1
            self.selectedx = -1
            self.selectedy = -1
    
    # update the board
    def update_board(self, piecetype, px, py, x, y):
        self.board[x][y] = self.board[px][py]
        self.board[px][py] = '*'
        if piecetype == 'K': # castle
            if px == 0:
                if y - py >= 2:
                    self.board[0][5] = 'R'
                    self.board[0][6] = 'K'
                    self.board[0][7] = '*'
                elif py - y >= 2:
                    self.board[0][0] = '*'
                    self.board[0][2] = 'K'
                    self.board[0][3] = 'R'
            elif px == 7:
                if y - py >= 2:
                    self.board[7][5] = 'r'
                    self.board[7][6] = 'k'
                    self.board[7][7] = '*'
                elif py - y >= 2:
                    self.board[7][0] = '*'
                    self.board[7][2] = 'k'
                    self.board[7][3] = 'r'
        elif piecetype == 'P': # promotion and en passant
            if x == 0:
                self.board[x][y] = self.promotion.lower()
            elif x == 7:
                self.board[x][y] = self.promotion.upper()
            elif px == 4 and x == 5 and y == self.enpassant:
                self.board[4][y] = '*'
            elif px == 3 and x == 2 and y == self.enpassant:
                self.board[3][y] = '*'
        return
    
    # make the move (px, py) to (x, y) and update the board if it is legal
    def make_move(self, px, py, x, y):
        
        if Board.get_color(self.board[px][py]) != self.turn:
            return False
        
        if px == x and py == y:
            return False
        
        piecetype = self.board[px][py].upper()
        
        self.update_board(piecetype, px, py, x, y)
        
        # update board information after a successful move
        if piecetype == 'P':
            if (abs(px-x)) == 2:
                self.enpassant = py
            else:
                self.enpassant = -1
        else:
            self.enpassant = -1
            if piecetype == 'K':
                if self.turn == Color.W:
                    self.w00 = False
                    self.w000 = False
                    self.whitekingx = x
                    self.whitekingy = y
                else:
                    self.b00 = False
                    self.b000 = False
                    self.blackkingx = x
                    self.blackkingy = y
        
        if self.board[0][0] != 'R':
            self.w000 = False
        if self.board[0][7] != 'R':
            self.w00 = False
        if self.board[7][0] != 'r':
            self.b000 = False
        if self.board[7][7] != 'r':
            self.b00 = False
        
        return True
