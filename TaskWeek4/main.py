import time


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves_count = 0
        self.result = None
        self.time_played = 0

    def make_move(self, board, start, end):
        if board.is_valid_move(start, end, self.color):
            if board.move_checker(start, end):
                self.moves_count += 1
                return True

        return False

    def get_info(self):
        return {
            "Name": self.name,
            "Color": self.color,
            "Moves": self.moves_count,
            "Result": self.result,
            "Time Played": self.time_played
        }

    def update_result(self, result):
        self.result = result

    def add_time(self, seconds):
        self.time_played += seconds


class Checker:
    def __init__(self, color, row, column):
        self.color = color
        self.row = row
        self.column = column
        self.is_king = False
        self.is_captured = False

    def get_position(self):
        return (self.row, self.column)

    def get_possible_moves(self):
        if self.is_captured:
            return []

        if self.is_king:
            directions = [
                (-1, -1), (-1, 1),
                (1, -1), (1, 1)
            ]
        elif self.color == "Black":
            directions = [(1, -1), (1, 1)]
        else:
            directions = [(-1, -1), (-1, 1)]

        possible_moves = []

        for row_change, col_change in directions:
            new_row = self.row + row_change
            new_col = self.column + col_change

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                possible_moves.append((new_row, new_col))

        return possible_moves

    def move(self, new_row, new_column):
        if self.is_captured:
            return False

        self.row = new_row
        self.column = new_column

        if self.color == "Black" and self.row == 7:
            self.promote_to_king()

        elif self.color == "Red" and self.row == 0:
            self.promote_to_king()

        return True

    def promote_to_king(self):
        self.is_king = True

    def capture(self):
        self.is_captured = True

    def get_info(self):
        return {
            "Color": self.color,
            "Position": self.get_position(),
            "Is King": self.is_king,
            "Is Captured": self.is_captured
        }


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.status = "Playing"
        self.initialize_board()

    def initialize_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grid[row][col] = Checker("Black", row, col)

                    elif row > 4:
                        self.grid[row][col] = Checker("Red", row, col)

    def display_board(self):
        print("\n    0 1 2 3 4 5 6 7")
        print("   -----------------")

        for row in range(8):
            print(row, " |", end=" ")

            for col in range(8):
                checker = self.grid[row][col]

                if checker is None:
                    symbol = "."
                elif checker.color == "Black":
                    symbol = "B" if not checker.is_king else "K"
                else:
                    symbol = "R" if not checker.is_king else "Q"

                print(symbol, end=" ")

            print()

        print()

    def get_checker(self, position):
        row, col = position

        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]

        return None

    def is_valid_move(self, start, end, color):
        start_row, start_col = start
        end_row, end_col = end

        if not all(0 <= value < 8 for value in
                   (start_row, start_col, end_row, end_col)):
            return False

        checker = self.get_checker(start)

        if checker is None or checker.color != color:
            return False

        if self.get_checker(end) is not None:
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if abs(row_diff) != abs(col_diff):
            return False

        if abs(row_diff) not in (1, 2):
            return False

        if not checker.is_king:
            direction = 1 if checker.color == "Black" else -1

            if row_diff * direction <= 0:
                return False

        if abs(row_diff) == 1:
            if self.has_available_capture(color):
                return False

            return True

        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        middle_checker = self.grid[middle_row][middle_col]

        if middle_checker is None:
            return False

        if middle_checker.color == checker.color:
            return False

        return True

    def get_available_moves(self, color, only_captures=False):
        capture_moves = []
        regular_moves = []

        for row in range(8):
            for col in range(8):
                checker = self.grid[row][col]

                if checker is None or checker.color != color:
                    continue

                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

                if not checker.is_king:
                    direction = 1 if color == "Black" else -1
                    directions = [(direction, -1), (direction, 1)]

                for row_change, col_change in directions:
                    next_row = row + row_change
                    next_col = col + col_change

                    if 0 <= next_row < 8 and 0 <= next_col < 8:
                        if self.grid[next_row][next_col] is None:
                            regular_moves.append(
                                ((row, col), (next_row, next_col))
                            )

                    jump_row = row + 2 * row_change
                    jump_col = col + 2 * col_change

                    if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                        middle = self.grid[next_row][next_col]

                        if (middle is not None
                                and middle.color != color
                                and self.grid[jump_row][jump_col] is None):
                            capture_moves.append(
                                ((row, col), (jump_row, jump_col))
                            )

        if capture_moves:
            return capture_moves

        if only_captures:
            return []

        return regular_moves

    def has_available_capture(self, color):
        return bool(self.get_available_moves(color, only_captures=True))

    def move_checker(self, start, end):
        checker = self.get_checker(start)

        if checker is None:
            return False

        if not self.is_valid_move(start, end, checker.color):
            return False

        start_row, start_col = start
        end_row, end_col = end

        captured_checker = None

        if abs(end_row - start_row) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2

            captured_checker = self.grid[middle_row][middle_col]
            captured_checker.capture()
            self.grid[middle_row][middle_col] = None

        self.grid[start_row][start_col] = None
        self.grid[end_row][end_col] = checker

        was_king = checker.is_king
        checker.move(end_row, end_col)

        must_continue = False

        if captured_checker is not None and not (
                checker.is_king and not was_king
        ):
            must_continue = bool(
                self.get_captures_for_checker(end)
            )

        return {
            "captured": captured_checker is not None,
            "must_continue": must_continue,
            "promoted": checker.is_king and not was_king
        }

    def get_captures_for_checker(self, position):
        checker = self.get_checker(position)

        if checker is None:
            return []

        row, col = position
        captures = []

        if checker.is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            direction = 1 if checker.color == "Black" else -1
            directions = [(direction, -1), (direction, 1)]

        for dr, dc in directions:
            middle_row = row + dr
            middle_col = col + dc
            end_row = row + 2 * dr
            end_col = col + 2 * dc

            if not (0 <= end_row < 8 and 0 <= end_col < 8):
                continue

            middle = self.grid[middle_row][middle_col]

            if (middle is not None
                    and middle.color != checker.color
                    and self.grid[end_row][end_col] is None):
                captures.append((end_row, end_col))

        return captures

    def remove_checker(self, position):
        checker = self.get_checker(position)

        if checker is None:
            return False

        checker.capture()
        row, col = position
        self.grid[row][col] = None

        return True

    def count_checkers(self, color):
        count = 0

        for row in self.grid:
            for checker in row:
                if checker is not None and checker.color == color:
                    count += 1

        return count

    def get_status(self):
        return {
            "Status": self.status,
            "Black Checkers": self.count_checkers("Black"),
            "Red Checkers": self.count_checkers("Red")
        }


class Game:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name, "Black")
        self.player2 = Player(player2_name, "Red")

        self.board = Board()
        self.current_player = self.player1

        self.total_moves = 0
        self.move_history = []

        self.start_time = None
        self.end_time = None
        self.status = "Not Started"
        self.winner = None

    def start_game(self):
        self.start_time = time.time()
        self.status = "Playing"

        print("\n===== CHECKERS GAME =====")
        print(f"Player 1: {self.player1.name} (Black)")
        print(f"Player 2: {self.player2.name} (Red)")

        while self.status == "Playing":
            self.board.display_board()

            if self.check_game_over():
                break

            self.play_turn()

        self.show_summary()

    def play_turn(self):
        player = self.current_player

        print(f"\nCurrent Player: {player.name}")
        print("1. Make a move")
        print("2. Finish game")

        choice = input("Choose an option: ").strip()

        if choice == "2":
            self.end_game(reason="Resignation")
            return

        if choice != "1":
            print("Invalid option. Please try again.")
            return

        available_moves = self.board.get_available_moves(
            player.color
        )

        print("\nAvailable moves:")
        for start, end in available_moves:
            print(f"{start} -> {end}")

        try:
            start_row = int(input("Start row: "))
            start_col = int(input("Start column: "))

            end_row = int(input("End row: "))
            end_col = int(input("End column: "))

        except ValueError:
            print("Please enter valid numbers.")
            return

        start = (start_row, start_col)
        end = (end_row, end_col)

        if (start, end) not in available_moves:
            print("Invalid move. Try again.")
            return

        turn_start = time.time()

        result = self.board.move_checker(start, end)

        if not result:
            print("Move failed.")
            return

        player.moves_count += 1
        self.total_moves += 1

        self.move_history.append(
            f"{player.name}: {start} -> {end}"
        )

        print(f"\n{player.name} moved {start} -> {end}")

        if result["captured"]:
            print("Opponent checker captured!")

        if result["promoted"]:
            print("Checker promoted to King!")

        # Handle additional captures in the same turn
        while result["must_continue"]:
            self.board.display_board()

            captures = self.board.get_captures_for_checker(end)

            print("\nYou must continue capturing!")
            print("Available destinations:", captures)

            try:
                new_row = int(input("Capture destination row: "))
                new_col = int(input("Capture destination column: "))

            except ValueError:
                print("Invalid input. Try again.")
                continue

            new_end = (new_row, new_col)

            if new_end not in captures:
                print("Invalid capture destination.")
                continue

            next_result = self.board.move_checker(end, new_end)

            if not next_result:
                print("Capture failed. Try again.")
                continue

            self.total_moves += 1
            self.move_history.append(
                f"{player.name}: {end} -> {new_end}"
            )

            end = new_end
            result = next_result

        player.add_time(time.time() - turn_start)

        self.board.display_board()

        print(f"Total moves: {self.total_moves}")

        if not self.check_game_over():
            self.switch_player()

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def check_game_over(self):
        black_count = self.board.count_checkers("Black")
        red_count = self.board.count_checkers("Red")

        if black_count == 0:
            self.winner = self.player2
            self.end_game(reason="All black checkers captured")
            return True

        if red_count == 0:
            self.winner = self.player1
            self.end_game(reason="All red checkers captured")
            return True

        moves = self.board.get_available_moves(
            self.current_player.color
        )

        if not moves:
            if self.current_player == self.player1:
                self.winner = self.player2
            else:
                self.winner = self.player1

            self.end_game(reason="No legal moves available")
            return True

        return False

    def end_game(self, reason="Finished"):
        if self.status == "Finished":
            return

        self.status = "Finished"
        self.board.status = "Finished"
        self.end_time = time.time()

        if reason == "Resignation":
            if self.current_player == self.player1:
                self.winner = self.player2
            else:
                self.winner = self.player1

        if self.winner:
            self.winner.update_result("Winner")

            loser = (
                self.player2
                if self.winner == self.player1
                else self.player1
            )
            loser.update_result("Loser")

        print(f"\nGame finished: {reason}")

    def show_summary(self):
        duration = 0

        if self.start_time is not None:
            end = self.end_time or time.time()
            duration = end - self.start_time

        print("\n========== GAME SUMMARY ==========")

        if self.winner:
            print(f"Winner: {self.winner.name}")
        else:
            print("Result: Draw / Unfinished")

        print(f"Total moves: {self.total_moves}")
        print(f"Game duration: {duration:.2f} seconds")

        print("\nPlayer statistics:")

        for player in (self.player1, self.player2):
            print(f"\nName: {player.name}")
            print(f"Color: {player.color}")
            print(f"Moves: {player.moves_count}")
            print(f"Result: {player.result}")
            print(f"Time played: {player.time_played:.2f} seconds")

        print("\nMove history:")
        for index, move in enumerate(self.move_history, 1):
            print(f"{index}. {move}")

        print("\n==================================")


def main():
    print("===== Welcome to Checkers =====")

    player1_name = input("Enter Player 1 name: ")
    player2_name = input("Enter Player 2 name: ")

    game = Game(player1_name, player2_name)

    game.start_game()


if __name__ == "__main__":
    main()
