class Board:
    """
    Represents the chessboard and handles its display and updates.
    """
    def __init__(self):
        self.grid = self._initialize_board()

    def _initialize_board(self):
        """Sets up the initial positions of the chess pieces on the board."""
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],  # Black pieces
            ["p", "p", "p", "p", "p", "p", "p", "p"],  # Black pawns
            ["."] * 8,  # Empty squares
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["P", "P", "P", "P", "P", "P", "P", "P"],  # White pawns
            ["R", "N", "B", "Q", "K", "B", "N", "R"]   # White pieces
        ]

    def display_board(self):
        """Prints the current state of the board with column and row labels."""
        # Print column labels (A-H)
        print("  a b c d e f g h")
        
        # Print each row with row labels (1-8)
        for i, row in enumerate(self.grid, start=1):
            print(f"{9 - i} {' '.join(row)}")
        print("  a b c d e f g h")


    def update_board(self, start, end):
        """
        Moves a piece from the start position to the end position.

        Args:
            start (tuple): Coordinates of the starting square (row, col).
            end (tuple): Coordinates of the destination square (row, col).
        """
        piece = self.grid[start[0]][start[1]]
        self.grid[start[0]][start[1]] = "."
        self.grid[end[0]][end[1]] = piece
    


class Piece:
    """
    Handles validation of chess piece movements.
    """
    @staticmethod
    def is_valid_move(piece, start, end, board):
        """
        Validates the movement of a piece based on its type.

        Args:
            piece (str): The piece to move (e.g., 'P' for white pawn).
            start (tuple): Starting coordinates (row, col).
            end (tuple): Destination coordinates (row, col).
            board (list of list): Current state of the chessboard.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if not (0 <= end[0] < 8 and 0 <= end[1] < 8):  # Ensure within bounds
            return False
        
        start_row, start_col = start
        end_row, end_col = end
        delta_row = end_row - start_row
        delta_col = end_col - start_col

        # Pawn logic
        if piece.lower() == "p":
            direction = 1 if piece.islower() else -1  # Black moves down, White moves up
            if end_col == start_col:
                #one step up
                if delta_row ==direction and board[end_row][end_col] == ".":
                    return True
                #function for only 2 steps foward(starting position)
                if delta_row == 2* direction and board[start_row + direction][start_col] == "." and board[end_row][end_col] == ".":
                    if (piece.islower() and start_row ==1) or (piece.isupper() and start_row ==6):
                        return True
            return False

        # Rook logic
        if piece.lower() == "r":
            return (delta_row == 0 or delta_col == 0) and Piece.is_path_clear(start, end, board)

        # Bishop logic
        if piece.lower() == "b":
            return abs(delta_row) == abs(delta_col) and Piece.is_path_clear(start, end, board)

        # Queen logic (combines rook and bishop)
        if piece.lower() == "q":
            return (delta_row == 0 or delta_col == 0 or abs(delta_row) == abs(delta_col)) and Piece.is_path_clear(start, end, board)

        # Knight logic
        if piece.lower() == "n":
            if (abs(delta_row), abs(delta_col)) in [(2, 1), (1, 2)]:
                #check if desitnation is empty.
                destination_piece=board[end_row][end_col]
                if destination_piece == "." or(piece.islower() and destination_piece.isupper()) or (piece.isupper() and destination_piece.islower()):
                    return True
                    
                    

        # King logic
        if piece.lower() == "k":
            return max(abs(delta_row), abs(delta_col)) == 1

        return False  # Default for unrecognized pieces

    @staticmethod
    def is_path_clear(start, end, board):
        """
        Checks if the path between start and end is clear for sliding pieces (rook, bishop, queen).

        Args:
            start (tuple): Starting coordinates (row, col).
            end (tuple): Destination coordinates (row, col).
            board (list of list): Current state of the chessboard.

        Returns:
            bool: True if the path is clear, False otherwise.
        """
        start_row, start_col = start
        end_row, end_col = end
        step_row = (end_row - start_row) // max(1, abs(end_row - start_row)) if end_row != start_row else 0
        step_col = (end_col - start_col) // max(1, abs(end_col - start_col)) if end_col != start_col else 0

        current_row, current_col = start_row + step_row, start_col + step_col
        while (current_row, current_col) != (end_row, end_col):
            if board[current_row][current_col] != ".":
                return False
            current_row += step_row
            current_col += step_col

        return True



class Game:
    """
    Manages the chessboard and user interactions.
    """
    def __init__(self):
        self.board = Board()
        self.turn = "white"  # Tracks whose turn it is

    def _parse_input(self, move):
        """
        Converts user input into board coordinates.

        Args:
            move (str): Chess notation input (e.g., 'e2 to e4').

        Returns:
            tuple: Start and end coordinates ((row1, col1), (row2, col2)).
        """
        try:
            start, end = move.split(" to ")
            start_row, start_col = 8 - int(start[1]), ord(start[0].lower()) - ord("a")
            end_row, end_col = 8 - int(end[1]), ord(end[0].lower()) - ord("a")
            # Validate input coordinates
            if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
                raise ValueError("Coordinates out of bounds.")
            return (start_row, start_col), (end_row, end_col)
        except (ValueError, IndexError):
            print("Invalid input. Please use the format 'e2 to e4'.")
            return None, None

    def play_turn(self):
        """Handles a single turn in the game."""
        self.board.display_board()
        print(f"{self.turn.capitalize()}'s turn.")

        while True:
            try:
                move = input("Enter your move (e.g., e2 to e4): ")
                start, end = self._parse_input(move)

                if start is None or end is None:
                    continue
                
                piece = self.board.grid[start[0]][start[1]]

                if piece == ".":
                    print("There's no piece at the starting position. Try again.")
                    continue

                if (self.turn == "white" and piece.islower()) or (self.turn == "black" and piece.isupper()):
                    print("You can't move the opponent's piece. Try again.")
                    continue

                if not Piece.is_valid_move(piece, start, end, self.board.grid):
                    print("That's an invalid move. Please select another square or piece.")
                    continue

                self.board.update_board(start, end)
                self.turn = "black" if self.turn == "white" else "white"
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

    def start_game(self):
        """Starts the chess simulation."""
        print("Welcome to Chess 101! Let's play.")
        print("Rules for Chess Pieces:")
        print("1. Pawns move forward one square, with the option to move two squares on their first move.")
        print("2. Rooks move horizontally or vertically any number of squares.")
        print("3. Knights move in an L-shape: two squares in one direction and then one square perpendicular.")
        print("4. Bishops move diagonally any number of squares.")
        print("5. The Queen moves horizontally, vertically, or diagonally any number of squares.")
        print("6. The King moves one square in any direction.")
        print()
        while True:
            try:
                self.play_turn()
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please restart the game.")
                break


if __name__ == "__main__":
    game = Game()
    game.start_game()