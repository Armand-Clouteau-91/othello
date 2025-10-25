import numpy as np


class Board:
    """Gère le plateau et les règles du jeu Othello."""

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
        # 1. Vérifie que le coup est dans le plateau
        # 2. Vérifie que ma case n'est pas déjà occupée
        # 3. Vérifie qu'un pion adverse est adjacent
        # 4. Vérifie qu'il y ai un pion allié sur une ligne ou une diagonale
        # 5. Vérifie qu'il n'y ai que des pions adverses entre les deux pions (pas de cases vides) 
        
    def apply_move:
        """Applique le coup"""
        pass


board_start = Board(8)
print(board_start.board)
