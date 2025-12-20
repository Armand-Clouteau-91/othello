import numpy as np
import board
import pygame


class Game:
    """Orchestre le déroulement du jeu : tours, fin de partie, scores."""

    def __init__(self, score=None, time=0):
        self.running = True
        self.color = "B"
        self.score = score if score is not None else {"W": 2, "B": 2}
        self.clock = pygame.time.Clock()
        self.opponent = {"W": "B", "B": "W"}
        self.board = board.Board(8)

    pass

    # handles the game end to end
    def run(self):
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

    # checks there still are moves available to play, changes player or ends the game if needed
    def move_available(self):
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

    # takes the input of a move
    def player_move(self):
        while True:
            try:
                row = int(input("Enter the row you want to put your piece in")) - 1
                col = int(input("Enter the column you want to put your piece in")) - 1
                return row, col
            except ValueError:
                print("\nInvalid input. Please enter numbers only. Try again.\n")

    # players take turn until all pieces are on the board
    def turn(self, x, y):
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
        print(f"Player {self.color} played a piece at {x}, {y}")
        print(self.board.board)
        print(f"the score is {self.score}")
        return True

    # This creates a boolean array and then counts the number of 'True' values.
    def get_score(self):
        black_score = np.count_nonzero(self.board.board == "B")
        white_score = np.count_nonzero(self.board.board == "W")
        return black_score, white_score

    # determines the winner based on the score
    def winner(self):
        if self.score["B"] > self.score["W"]:
            winner = "B"
        elif self.score["B"] < self.score["W"]:
            winner = "W"
        else:
            winner = "nobody, that's a draw"
        return f"The winner is {winner}"

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove uncopyable objects
        if "clock" in state:
            del state["clock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Recreate the clock if needed
        self.clock = pygame.time.Clock()



if __name__ == "__main__":
    test_game = Game()
    test_game.run()
