import numpy as np
import board
import pygame


class Game:
    """Manages the game logic, score, turns and end of the game"""

    def __init__(self, score=None, time=0):
        self.running = True
        self.color = "B"
        self.score = score if score is not None else {"W": 2, "B": 2}
        self.clock = pygame.time.Clock()
        self.opponent = {"W": "B", "B": "W"}
        self.board = board.Board(8)

    pass

    def run(self):
        """
        Handles the game running end to end 
        
        """
        while self.running == True:
            if self.move_available():
                print(f"It's {self.color}'s turn")
                print(self.board.board)
                while True:
                    row, col = self.player_move()
                    if self.turn(row, col):
                        self.color = self.opponent[self.color]
                        break
            else:
                break
        return self.winner()

    def move_available(self):
        """
        checks there still are moves available to play, changes player or ends the game if needed
        
        """
        if self.board.remaining_moves(self.color) == []:
            print(f"{self.color} cannot play.")
            if self.board.remaining_moves(self.opponent[self.color]) == []:
                print(f"{self.opponent[self.color]} cannot play.")
                self.running = False
                play_on = False
            else:
                print(f"However {self.opponent[self.color]} can play.")
                self.color = self.opponent[self.color]
                play_on = True
        else:
            play_on = True
        return play_on

    def player_move(self):
        """
        Player input
        
        """
        while True:
            try:
                row = int(input("Enter the row you want to put your piece in")) - 1
                col = int(input("Enter the column you want to put your piece in")) - 1
                return row, col
            except ValueError:
                print("\nInvalid input. Please enter numbers only. Try again.\n")

    
    def turn(self, x, y):
        """
        main turn logic calling valid_move(), apply_move(), get_score() and updates the score
        
        :param x: row
        :param y: column
        """
        check = self.board.valid_move(x, y, self.color)
        if check == False:
            print(f"the move {x}, {y} is not valid, please try another one.")
            return False
        else:
            self.board.apply_move(x, y, self.color)
        score_black, score_white = self.get_score()
        self.score[self.color] = score_black if self.color == "B" else score_white
        self.score[self.opponent[self.color]] = (
            score_white if self.color == "B" else score_black
        )
        return True

    def get_score(self):
        """
        Returns the current score by counting each player's discs
        
        """
        # Creates a boolean array and then counts the number of 'True' values.
        black_score = np.count_nonzero(self.board.board == "B")
        white_score = np.count_nonzero(self.board.board == "W")
        return black_score, white_score


    def winner(self):
        """
        Determines the winner based on the score
        
        """
        if self.score["B"] > self.score["W"]:
            winner = "Black"
        elif self.score["B"] < self.score["W"]:
            winner = "White"
        else:
            winner = "nobody, that's a draw"
        return f"The winner is {winner}"

    def __getstate__(self):
        """
        Remove uncopyable objects to prevent any error we deepcopying
        
        """
        state = self.__dict__.copy()
        if "clock" in state:
            del state["clock"]
        return state

    def __setstate__(self, state):
        """
        Reattach the clock to the state
        
        :param state: State we deepcopied
        """
        self.__dict__.update(state)
        self.clock = pygame.time.Clock()



if __name__ == "__main__":
    test_game = Game()
    test_game.run()
