import numpy as np


class Board:
    """Gère le plateau et les règles du jeu Othello."""

    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, size):
        self.size = size
        self.board = self.create_board()

    def create_board(self):
        """Crée le plateau avec positon de départ"""
        # 1. Créer Matrice 8x8 représentant le plateau
        b = np.full((self.size, self.size), fill_value=".", dtype="<U1")
        # 2. Placer les pions de départ
        b[3, 3] = "W"
        b[4, 4] = "W"
        b[3, 4] = "B"
        b[4, 3] = "B"
        return b

    def valid_move(self, x, y, color):
        """Vérifie que le coup soit valide"""
        opponent = "W" if color == "B" else "B"
        # 1. Vérifie que le coup est dans le plateau et que la case n'est pas déjà occupée
        if 0 <= x < self.size and 0 <= y < self.size and self.board[x, y] == ".":
            # 3. Vérifie qu'un pion adverse est adjacent (intégrer une boucle)
            for dx, dy in Board.DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.size
                    and 0 <= ny < self.size
                    and self.board[nx, ny] == opponent
                ):
                    # 4. Vérifie qu'il y ai un pion allié sur une ligne ou une diagonale
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

    def apply_move(self, x, y, color):
        """Applique le coup"""
        opponent = "W" if color == "B" else "B"
        self.board[x, y] = color
        # Retourne les pions adverses
        for dx, dy in Board.DIRECTIONS:
            nx, ny = x + dx, y + dy
            flip = []
            if (
                0 <= nx < self.size
                and 0 <= ny < self.size
                and self.board[nx, ny] == opponent
            ):
                nx += dx
                ny += dy
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
