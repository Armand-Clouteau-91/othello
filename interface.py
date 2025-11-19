import pygame
import sys
from game import Game


class Interface:
    """Gère l'interface utilisateur et les interactions."""

    # Initialisation de pygame et des attributs de l'interface
    def __init__(self, screen_size=600, grid_size=8):
        pygame.init()
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.cell_size = screen_size // grid_size
        self.screen = pygame.display.set_mode((screen_size + 200, screen_size))
        pygame.display.set_caption("Othello")
        self.clock = pygame.time.Clock()
        self.game = Game()

        # Couleurs
        self.GREEN = (34, 139, 34)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)

        # Boutons
        self.buttons = self.create_buttons()

        # Historique pour undo
        self.move_history = []

        # Message de feedback
        self.feedback_message = ""

    def create_buttons(self):
        """Crée les boutons Undo, Restart, Pass Turn"""
        return {
            "undo": pygame.Rect(620, 100, 150, 50),
            "restart": pygame.Rect(620, 170, 150, 50),
            "pass": pygame.Rect(620, 240, 150, 50),
        }

    def handle_click(self, pos):
        """Gère les clics souris"""
        x, y = pos

        # Vérifie si le clic est sur le plateau
        if x < self.screen_size and y < self.screen_size:
            col = x // self.cell_size
            row = y // self.cell_size

            # Sauvegarde l'état avant le coup (pour undo)
            self.move_history.append(
                (self.game.board.board.copy(), self.game.color, self.game.score.copy())
            )

            # Valide et applique le coup
            if self.game.board.valid_move(row, col, self.game.color):
                self.game.turn(row, col)
                # ✓ AJOUTE CETTE LIGNE : Change le joueur
                self.game.color = self.game.opponent[self.game.color]
                self.feedback_message = ""
                return True
            else:
                self.move_history.pop()
                self.feedback_message = "Invalid move!"
                return False

        # Vérifie si le clic est sur un bouton
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.handle_button_click(button_name)

    def handle_button_click(self, button_name):
        """Gère les clics sur les boutons"""
        if button_name == "undo":
            self.undo_move()
        elif button_name == "restart":
            self.game = Game()
            self.move_history = []
            self.feedback_message = "Game restarted!"
        elif button_name == "pass":
            self.game.color = self.game.opponent[self.game.color]
            self.feedback_message = "Turn passed!"

    def undo_move(self):
        """Annule le dernier coup"""
        if len(self.move_history) == 0:
            self.feedback_message = "No moves to undo!"
            return

        # Récupère le dernier état
        previous_board, previous_color, previous_score = self.move_history.pop()

        # Restaure l'état
        self.game.board.board = previous_board.copy()
        self.game.color = previous_color
        self.game.score = previous_score.copy()
        self.feedback_message = "Move undone!"

    def draw_buttons(self):
        """Dessine les boutons avec effet hover"""
        mouse_pos = pygame.mouse.get_pos()

        for button_name, button_rect in self.buttons.items():
            # Change la couleur si la souris survole
            if button_rect.collidepoint(mouse_pos):
                color = (100, 100, 100)
            else:
                color = self.GRAY

            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, self.BLACK, button_rect, 2)  # Bordure

            # Ajoute le texte du bouton
            font = pygame.font.Font(None, 30)
            text = font.render(button_name.capitalize(), True, self.WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def show_feedback(self, message):
        """Affiche des messages à l'utilisateur"""
        if message:
            font = pygame.font.Font(None, 24)
            text = font.render(message, True, self.RED)
            self.screen.blit(text, (620, 350))

    def draw_board(self):
        """Dessine la grille 8x8"""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, self.GREEN, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 2)

    def draw_discs(self):
        """Dessine les pions sur le plateau"""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.game.board.board[row, col]
                if cell != ".":
                    center = (
                        col * self.cell_size + self.cell_size // 2,
                        row * self.cell_size + self.cell_size // 2,
                    )
                    color = self.BLACK if cell == "B" else self.WHITE
                    pygame.draw.circle(
                        self.screen, color, center, self.cell_size // 2 - 5
                    )
                    pygame.draw.circle(
                        self.screen, self.BLACK, center, self.cell_size // 2 - 5, 2
                    )

    def highlight_valid_moves(self):
        """Surligne les cases où le joueur peut jouer"""
        valid_moves = self.game.board.remaining_moves(self.game.color)

        for row, col in valid_moves:
            center = (
                col * self.cell_size + self.cell_size // 2,
                row * self.cell_size + self.cell_size // 2,
            )
            pygame.draw.circle(self.screen, self.YELLOW, center, 10, 3)

    def draw_game_info(self):
        """Affiche les scores et le tour actuel"""
        font = pygame.font.Font(None, 36)

        # Tour actuel
        current_player = "Black" if self.game.color == "B" else "White"
        turn_text = font.render(f"{current_player}'s turn", True, self.BLACK)
        self.screen.blit(turn_text, (620, 30))

        # Scores
        font_score = pygame.font.Font(None, 32)
        black_score = font_score.render(
            f"Black: {self.game.score['B']}", True, self.BLACK
        )
        white_score = font_score.render(
            f"White: {self.game.score['W']}", True, self.BLACK
        )
        self.screen.blit(black_score, (620, 400))
        self.screen.blit(white_score, (620, 440))

    def run(self):
        """Boucle principale du jeu"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # Dessine tout
            self.screen.fill(self.WHITE)
            self.draw_board()
            self.draw_discs()
            self.highlight_valid_moves()
            self.draw_buttons()
            self.draw_game_info()
            self.show_feedback(self.feedback_message)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    interface = Interface()
    interface.run()
