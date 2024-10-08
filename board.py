import os
import pawn


class Board:
    BOARD_WIDTH = 8
    BOARD_HEIGHT = 8

    pawns_alive = {
        "White": {
            "King": 1,
            "Queen": 1,
            "Rook": 2,
            "Bishop": 2,
            "Knight": 2,
            "Pawn": 8
        },
        "Black": {
            "King": 1,
            "Queen": 1,
            "Rook": 2,
            "Bishop": 2,
            "Knight": 2,
            "Pawn": 8
        }
    }

    def __init__(self):
        self.board = [[pawn.Pawn() for i in range(self.BOARD_WIDTH)] for i in range(self.BOARD_HEIGHT)]

    def print_board(self):
        print("\n\t    a    b    c    d    e    f    g    h  ")
        print("\t   ____ ____ ____ ____ ____ ____ ____ ____")
        for i in range(len(self.board) - 1, -1, -1):
            print(f"\t{i+1} | ", end='')

            for j in range(len(self.board[i])):
                print(self.board[i][j].color_text + self.board[i][j].get_short_name() + "\033[0m", end=f" | ")
            print(f"{i+1}")
            print("\t  |____|____|____|____|____|____|____|____|")
        print("\n\t    a    b    c    d    e    f    g    h  ")

    def print_pawns(self):
        print("\nWhite:\t\t\tBlack:")
        for key in self.pawns_alive["White"].keys():
            print(f'{key}:\t{self.pawns_alive["White"][key]}\t\t{key}:\t{self.pawns_alive["Black"][key]}')

    def fresh_fill(self):
        for i in range(self.BOARD_WIDTH):
            self.board[1][i] = pawn.Pawn("Pawn", "White")
        self.board[0][0] = pawn.Pawn("Rook", "White")
        self.board[0][7] = pawn.Pawn("Rook", "White")
        self.board[0][1] = pawn.Pawn("Knight", "White")
        self.board[0][6] = pawn.Pawn("Knight", "White")
        self.board[0][2] = pawn.Pawn("Bishop", "White")
        self.board[0][5] = pawn.Pawn("Bishop", "White")
        self.board[0][3] = pawn.Pawn("Queen", "White")
        self.board[0][4] = pawn.Pawn("King", "White")

        for i in range(self.BOARD_WIDTH):
            self.board[6][i] = pawn.Pawn("Pawn", "Black")
        self.board[7][0] = pawn.Pawn("Rook", "Black")
        self.board[7][7] = pawn.Pawn("Rook", "Black")
        self.board[7][1] = pawn.Pawn("Knight", "Black")
        self.board[7][6] = pawn.Pawn("Knight", "Black")
        self.board[7][2] = pawn.Pawn("Bishop", "Black")
        self.board[7][5] = pawn.Pawn("Bishop", "Black")
        self.board[7][3] = pawn.Pawn("Queen", "Black")
        self.board[7][4] = pawn.Pawn("King", "Black")

    def move_pawn(self, source, destination):
        if self.board[destination[0]][destination[1]].get_name() is not None:
            self.sub_pawn(destination)
        self.board[source[0]][source[1]].set_moved(True)
        self.board[destination[0]][destination[1]] = self.board[source[0]][source[1]]
        self.board[source[0]][source[1]] = pawn.Pawn()

    def sub_pawn(self, position):
        target_pawn = self.board[position[0]][position[1]]
        self.pawns_alive[target_pawn.get_color()][target_pawn.get_name()] -= 1

    def get_pawn(self, position):
        return self.board[position[0]][position[1]]

    def evolve(self, pawn_to_evolve, name):
        pawn_to_evolve.set_name(name)
        color = pawn_to_evolve.get_color()
        self.pawns_alive[color]["Pawn"] -= 1
        self.pawns_alive[color][name] += 1

