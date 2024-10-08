import os

import board
import alert


class Game:
    alerts = alert.Alerts()
    player_turn = "White"
    winner = None
    to_evolution = None
    do_swap = False

    def __init__(self):
        self.board = board.Board()
        self.game_is_running = True

    def start(self):
        self.board.fresh_fill()
        self.update()
        while self.game_is_running:
            source, destination = self.get_user_input()
            if self.check_move_correctness(source, destination):
                self.board.move_pawn(source, destination)
                self.do_swap = True

                if self.check_evolution_possibility(destination):
                    self.to_evolution = self.board.get_pawn(destination)
                    self.update()

            if self.board.pawns_alive["White"]["King"] == 0 or self.board.pawns_alive["Black"]["King"] == 0:
                self.game_is_running = False
                self.do_swap = True
                self.winner = self.player_turn

            if self.do_swap:
                self.swap_player()
                self.do_swap = False

            self.update()

    def update(self):
        # TODO: Add statistics (time per player, killed pawns etc.)
        os.system("cls")
        print(self.player_turn)
        # self.board.print_pawns()
        self.board.print_board()
        if self.to_evolution is not None:
            user_input = self.print_evolution_question()
            self.board.evolve(self.to_evolution, user_input)
            self.to_evolution = None
        self.alerts.print()
        if not self.game_is_running:
            print(f"Game over!\nWinner is {self.winner}.")

    def check_evolution_possibility(self, destination):
        condition_1 = True if self.board.get_pawn(destination).get_name() == "Pawn" else False
        condition_2 = True if destination[0] == 0 or destination[0] == 7 else False
        return condition_1 and condition_2

    def swap_player(self):
        self.player_turn = "White" if self.player_turn == "Black" else "Black"

    def print_evolution_question(self):
        print("Your pawn has reached the end of the board. Choose pawn type that is gonna replace normal pawn.")
        print("Queen (Qu), Rook (Ro), Bishop (Bi), Knight (Kn)")
        user_input = input("Change to ")
        while user_input not in ("Queen", "Qu", "Rook", "Ro", "Bishop", "Bi", "Knight", "Kn"):
            print("Wrong input! Try again.")
            user_input = input("Change to ")

        match user_input:
            case "Qu":
                user_input = "Queen"
            case "Ro":
                user_input = "Rook"
            case "Bi":
                user_input = "Bishop"
            case "Kn":
                user_input = "Knight"
        return user_input

    def get_user_input(self):
        source, destination = input("> "), input("> ")
        if not self.check_input_correctness(source) or not self.check_input_correctness(destination):
            return_value = (None, None)
        else:
            return_value = (self.input_to_position(source), self.input_to_position(destination))
        return return_value

    def check_move_correctness(self, source, destination):
        if source is None or destination is None:
            return False
        if self.board.get_pawn(source).get_color() != self.player_turn:
            self.alerts.add(f"As the {self.player_turn} player you can't move "
                            f"a {self.board.get_pawn(source).get_color()} pawn.")
            return False
        elif source == destination:
            self.alerts.add(f"You cannot move the pawn to {self.position_to_input(destination)}.")
            return False

        possible_moves = []
        match self.board.get_pawn(source).get_name():
            case "King":
                possible_moves = self.king_moves(source)
            case "Queen":
                possible_moves = self.queen_moves(source)
            case "Rook":
                possible_moves = self.rook_moves(source)
            case "Bishop":
                possible_moves = self.bishop_moves(source)
            case "Knight":
                possible_moves = self.knight_moves(source)
            case "Pawn":
                possible_moves = self.pawn_moves(source)

        if destination not in possible_moves:
            self.alerts.add(f"You cannot move to {self.position_to_input(destination)}.")
        return True if destination in possible_moves else False

    def king_moves(self, source):
        all_moves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                all_moves.append((source[0] + i, source[1] + j))

        return_list = all_moves.copy()
        for move in all_moves:
            if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0 \
                    or self.board.get_pawn(move).get_color() == self.player_turn:
                return_list.remove(move)
        return return_list

    def queen_moves(self, source):
        all_moves = []
        all_moves += self.rook_moves(source)
        all_moves += self.bishop_moves(source)
        return all_moves

    def rook_moves(self, source):
        all_moves = []

        offsets = {"Up": (0, 1), "Down": (0, -1), "Right": (1, 0), "Left": (-1, 0)}
        all_moves += self.generate_moves(offsets["Up"], source, range(1, 8))
        all_moves += self.generate_moves(offsets["Down"], source, range(1, 8))
        all_moves += self.generate_moves(offsets["Right"], source, range(1, 8))
        all_moves += self.generate_moves(offsets["Left"], source, range(1, 8))

        return all_moves

    def bishop_moves(self, source):
        all_moves = []

        all_moves += self.generate_moves((1, 1), source, range(1, 8))
        all_moves += self.generate_moves((-1, 1), source, range(1, 8))
        all_moves += self.generate_moves((1, -1), source, range(1, 8))
        all_moves += self.generate_moves((-1, -1), source, range(1, 8))

        return all_moves

    def knight_moves(self, source):
        all_moves = []
        for i in (2, -2):
            for j in (1, -1):
                all_moves.append((source[0]+i, source[1]+j))
                all_moves.append((source[0]+j, source[1]+i))

        return_list = all_moves.copy()
        for move in all_moves:
            if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0 \
                    or self.board.get_pawn(move).get_color() == self.player_turn:
                return_list.remove(move)

        return return_list

    def pawn_moves(self, source):
        all_moves = []
        offset = 1 if self.player_turn == "White" else -1

        move = (source[0] + offset, source[1])
        if self.board.get_pawn(move).get_name() is None:
            all_moves.append(move)

        move = (source[0] + 2 * offset, source[1])
        if not self.board.get_pawn(source).get_moved() and self.board.get_pawn(move).get_name() is None:
            all_moves.append(move)

        for i in (-1, 1):
            move = (source[0] + offset, source[1] + i)
            if self.board.get_pawn(move).get_name() is not None:
                all_moves.append(move)
        return all_moves

    def generate_moves(self, offset, source, loop_range):
        all_moves = []
        for i in loop_range:
            move = (source[0] + offset[1] * i, source[1] + offset[0] * i)
            if move == source:
                continue
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                break
            if self.board.get_pawn(move).get_name() is None:
                all_moves.append(move)
                continue
            if self.board.get_pawn(move).get_color() != self.player_turn:
                all_moves.append(move)
            break
        return all_moves

    def check_input_correctness(self, user_input):
        return_value = True
        if len(user_input) > 2:
            self.alerts.add(f"The given input is too long. ({user_input})")
            return False
        elif len(user_input) < 2:
            self.alerts.add(f"The given input is too short. ({user_input})")
            return False

        pos_x, pos_y = self.input_to_position(user_input)
        if 0 > pos_x or pos_x > 7:
            self.alerts.add(f"The first character has to be a letter from 'a' to 'h'. ({user_input})")
            return_value = False
        if 0 > pos_y or pos_y > 7:
            self.alerts.add(f"The second character has to be digit between 1 and 8. ({user_input})")
            return_value = False
        return return_value

    def input_to_position(self, user_input):
        return ord(user_input[1]) - ord('1'), ord(user_input[0]) - ord('a')

    def position_to_input(self, position):
        return chr(position[1] + ord('a')) + chr(position[0] + ord('1'))

    def stop_game(self):
        self.game_is_running = False
