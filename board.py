import numpy as np


class Board:
    """Manages the board and the rules of the game Othello."""

    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, size):
        self.size = size
        self.board = self.create_board()

    def create_board(self):
        """Creates the board and the positions the initial discs."""

        # Create a 8x8 board
        b = np.full((self.size, self.size), fill_value=".", dtype="<U1")
        # Positions the starting discs
        b[3, 3] = "W"
        b[4, 4] = "W"
        b[3, 4] = "B"
        b[4, 3] = "B"
        return b

    def valid_move(self, x, y, color):
        """
        Check the validity of the move a player wants to play
          
        :param x: row coordinate
        :param y: column coordinate
        :param color: the player who is currently playing
        """
        opponent = "W" if color == "B" else "B"
        # Checks the moves is within the bounds of the board and that the position is not already occupied
        if 0 <= x < self.size and 0 <= y < self.size and self.board[x, y] == ".":
            # Checks that an opponent disc is adjacent
            for dx, dy in Board.DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.size
                    and 0 <= ny < self.size
                    and self.board[nx, ny] == opponent
                ):
                    # Checks the alignment with an ally disc
                    nx += dx
                    ny += dy
                    while 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.board[nx, ny] == color:
                            return True
                        elif self.board[nx, ny] == ".":
                            break
                        nx += dx
                        ny += dy
        return False

    def remaining_moves(self, color):
        """
        Checks whether a player still has moves to play 
        
        :param color: the player who is currently playing
        """
        # gather the coordinates of the empty positions on the board
        empty_rows, empty_cols = np.where(self.board == ".")
        empty_squares = zip(empty_rows, empty_cols)
        
        # loops through the coordinates and checks whether they are valid moves for the current player 
        valid_moves =[]
        for r,c in empty_squares:
            if self.valid_move(r,c,color):
                valid_moves.append((r,c))
        return valid_moves

    def apply_move(self, x, y, color):
        """
        Apply move

        :param x: row coordinate
        :param y: column coordinate
        :param color: the player who is currently playing
        """

        opponent = "W" if color == "B" else "B"
        self.board[x, y] = color
        # flips the opponent's discs by scanning in all directions within the bound of the board
        for dx, dy in Board.DIRECTIONS:
            nx, ny = x + dx, y + dy
            flip = []
            if (
                0 <= nx < self.size
                and 0 <= ny < self.size
                and self.board[nx, ny] == opponent
            ):
                flip.append((nx, ny))
                nx += dx
                ny += dy
                # we initialise the looping in the direction we scanned up until we hit the boudn of the board or reach an ally disc,
                # then flip everything in this direction 
                while 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx, ny] == opponent:
                        flip.append((nx, ny))
                    elif self.board[nx, ny] == color:
                        for fx, fy in flip:
                            self.board[fx, fy] = color
                        break
                    else:
                        break
                    nx += dx
                    ny += dy
        


if __name__ == "__main__":
    board_start = Board(8)
    print(board_start.board)
    # test
    board_start.apply_move(2, 3, "B")
    print(board_start.board)
    board_start.apply_move(2, 2, "W")
    print(board_start.board)
    board_start.apply_move(5, 4, "B")
    print(board_start.board)
