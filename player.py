import copy
import random

class Player:
    """Represents an AI player using a Greedy Algorithm."""

    def __init__(self, color):
        self.color = color

    def get_greedy_move(self, game_instance):
        """
        Simulates all valid moves and returns the one that maximizes 
        the AI's score immediately.
        """
        # 1. Get all legal moves for the bot
        valid_moves = game_instance.board.remaining_moves(self.color)
        
        if not valid_moves:
            return None

        # 2. Shuffle moves to handle ties randomly (adds variety)
        random.shuffle(valid_moves)

        best_move = None
        max_score = -1

        # 3. Iterate through every possible move
        for row, col in valid_moves:
            # Create a deep copy of the game to simulate the future
            # This ensures we don't mess up the actual game board
            temp_game = copy.deepcopy(game_instance)
            
            # Execute the move on the temporary board
            # We assume game.turn() handles flipping discs and updating scores
            temp_game.turn(row, col)
            
            # Get the score after the move
            # 'B' or 'W' depending on self.color
            current_score = temp_game.score[self.color]

            # Greedy check: Is this better than what we found before?
            if current_score > max_score:
                max_score = current_score
                best_move = (row, col)

        return best_move