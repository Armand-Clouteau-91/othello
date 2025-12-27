import pygame
import sys
from game import Game
from player import Player

class Interface:
    """Manages UI and user interactions"""

    # Pygame and interface attributes initialisation
    def __init__(self, screen_size=600, grid_size=8):
        pygame.init()
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.cell_size = screen_size // grid_size
        self.screen = pygame.display.set_mode((screen_size + 250, screen_size))
        pygame.display.set_caption("Othello")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.timer_started = False
        self.start_time = 0
        self.elapsed_time = 0
        self.game_over = False
        self.state = "MENU" # 'MENU' or 'GAME'
        self.game_mode = None # 'PvP' or 'PvBot'
        self.bot_color = 'W'  # Bot plays White by default
        self.bot = Player(self.bot_color)
        self.bot_delay_start = None

        # colors
        self.GREEN = (34, 139, 34)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.LIGHT_GRAY = (220, 220, 220)
        self.DARK_GREEN = (0, 100, 0)

        # Buttons
        self.buttons = self.create_buttons()
        self.menu_buttons = self.create_menu_buttons()

        # historic for undoing things
        self.move_history = []

        # feedback messages
        self.feedback_message = ""

    def create_buttons(self):
        """creates buttons Undo, Restart, Pass Turn and Menu"""
        return {
            "undo": pygame.Rect(620, 330, 100, 40),
            "restart": pygame.Rect(730, 330, 100, 40),
            "pass": pygame.Rect(620, 390, 100, 40),
            "menu" : pygame.Rect(730, 390, 100, 40),
        }

    def create_menu_buttons(self):
            """Creates the main menu selection buttons."""
            center_x = (self.screen_size + 250) // 2
            return {
                "pvp": pygame.Rect(center_x - 150, 250, 300, 60),
                "pvbot": pygame.Rect(center_x - 150, 350, 300, 60)
            }


    def handle_click(self, pos):
        """Processes mouse clicks during the active game phase."""
        
        x, y = pos

        # Check if click is within the game board
        if x < self.screen_size and y < self.screen_size:
            col = x // self.cell_size
            row = y // self.cell_size

            # Save state for undo functionality
            self.move_history.append(
                (self.game.board.board.copy(), self.game.color, self.game.score.copy())
            )

            # Validate and apply move
            if self.game.board.valid_move(row, col, self.game.color):
                self.game.turn(row, col)
                # Start timer on first move
                if not self.timer_started :
                    self.start_time = pygame.time.get_ticks()
                    self.timer_started = True

                # Switch turns
                self.game.color = self.game.opponent[self.game.color]
                self.feedback_message = ""
                return True
            else:
                self.move_history.pop()
                self.feedback_message = "Invalid move!"
                return False

        # Check if click is on a UI button
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.handle_button_click(button_name)

    def handle_menu_click(self, pos):
        """Processes mouse clicks on the main menu."""
        for key, rect in self.menu_buttons.items():
            if rect.collidepoint(pos):
                if key == "pvp":
                    self.game_mode = "PvP"
                elif key == "pvbot":
                    self.game_mode = "PvBot"
                
                # Initialize new game session
                self.state = "GAME"
                self.game = Game()
                self.move_history = []
                self.timer_started = False
                self.game_over = False

    def perform_bot_move(self):
        """Executes the bot's logic and applies the move."""
        move = self.bot.get_greedy_move(self.game)
        if move:
            row, col = move
            self.move_history.append(
                (self.game.board.board.copy(), self.game.color, self.game.score.copy())
            )
            self.game.turn(row, col)
            self.game.color = self.game.opponent[self.game.color]
            self.feedback_message = ""
        else:
            # Bot passes if no moves are available
            self.game.color = self.game.opponent[self.game.color]
            self.feedback_message = "Bot passed!"

    def handle_button_click(self, button_name):
        """Executes actions for specific UI buttons."""
        if button_name == "undo":
            self.undo_move()
        elif button_name == "restart":
            self.game = Game()
            self.move_history = []
            self.feedback_message = "Game restarted!"
            self.game_over = False  # reset game over state
            self.timer_started = False  # reset timer
            self.elapsed_time = 0  
        elif button_name == "pass":
            self.game.color = self.game.opponent[self.game.color]
            self.feedback_message = "Turn passed!"
        elif button_name == "menu":
            self.state = "MENU"

    def undo_move(self):
        """Reverts the game state (1 step for PvP, 2 steps for PvBot)."""
        if len(self.move_history) == 0:
            self.feedback_message = "No moves to undo!"
            return

        # Undo 2 moves in PvBot to return to player's turn
        undo_steps = 2 if self.game_mode == "PvBot" and len(self.move_history) >= 2 else 1

        for step in range(undo_steps):
                
            # gets the last state
            previous_board, previous_color, previous_score = self.move_history.pop()

            # restore the state
            self.game.board.board = previous_board.copy()
            self.game.color = previous_color
            self.game.score = previous_score.copy()
        
        self.feedback_message = "Move undone!"

    def draw_buttons(self):
        """Renders the side panel buttons with hover effects."""
        mouse_pos = pygame.mouse.get_pos()

        for button_name, button_rect in self.buttons.items():
            # highlight when hovering
            if button_rect.collidepoint(mouse_pos):
                color = (100, 100, 100)
            else:
                color = self.GRAY

            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, self.BLACK, button_rect, 2)  # border

            # adds the text on the buttons
            font = pygame.font.Font(None, 30)
            text = font.render(button_name.capitalize(), True, self.WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def show_feedback(self, message):
        """Displays temporary feedback messages to the user."""
        if message:
            font = pygame.font.Font(None, 24)
            text = font.render(message, True, self.RED)
            self.screen.blit(text, (620, 560))

    def draw_board(self):
        """Draws the 8x8 game grid."""
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
        """Renders the pieces (black and white discs) on the board."""
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
        """Highlights valid move positions for the current player."""
        
        # Hide hints during bot's turn
        if self.game_mode == "PvBot" and self.game.color == self.bot_color:
            return
        
        valid_moves = self.game.board.remaining_moves(self.game.color)

        for row, col in valid_moves:
            center = (
                col * self.cell_size + self.cell_size // 2,
                row * self.cell_size + self.cell_size // 2,
            )
            pygame.draw.circle(self.screen, self.YELLOW, center, 10, 3)

    def draw_game_info(self):
        """Draws status panels (turn, score) and the game timer."""
        
        # turn Panel
        turn_panel = pygame.Rect(615, 20, 220, 100)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, turn_panel)
        pygame.draw.rect(self.screen, self.BLACK, turn_panel, 3)
    
        # title
        font_title = pygame.font.Font(None, 28)
        title = font_title.render("Current Turn", True, self.BLACK)
        self.screen.blit(title, (660, 30))
    
        # player name and visual indicator
        current_player = "Black" if self.game.color == "B" else "White"
        font_player = pygame.font.Font(None, 36)
        player_text = font_player.render(current_player, True, self.BLACK)
        self.screen.blit(player_text, (680, 65))
    
        # indicative circle
        indicator_color = self.BLACK if self.game.color == "B" else self.WHITE
        pygame.draw.circle(self.screen, indicator_color, (645, 80), 15)
        pygame.draw.circle(self.screen, self.BLACK, (645, 80), 15, 2)
    
        # score panel
        # background panel
        score_panel = pygame.Rect(615, 140, 220, 180)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, score_panel)
        pygame.draw.rect(self.screen, self.BLACK, score_panel, 3)
    
        # title
        score_title = font_title.render("Scores", True, self.BLACK)
        self.screen.blit(score_title, (695, 150))
    
        # score font
        font_score = pygame.font.Font(None, 32)
    
        # ind and text for Black
        pygame.draw.circle(self.screen, self.BLACK, (640, 195), 12)
        pygame.draw.circle(self.screen, self.BLACK, (640, 195), 12, 2)
        black_text = font_score.render(f"Black: {self.game.score['B']}", True, self.BLACK)
        self.screen.blit(black_text, (660, 183))
    
        # ind and text for White
        pygame.draw.circle(self.screen, self.WHITE, (640, 235), 12)
        pygame.draw.circle(self.screen, self.BLACK, (640, 235), 12, 2)
        white_text = font_score.render(f"White: {self.game.score['W']}", True, self.BLACK)
        self.screen.blit(white_text, (660, 223))
    
        # allowed moves
        valid_moves_count = len(self.game.board.remaining_moves(self.game.color))
        font_moves = pygame.font.Font(None, 24)
        moves_text = font_moves.render(f"Valid moves: {valid_moves_count}", True, self.DARK_GREEN)
        self.screen.blit(moves_text, (630, 280))

        # timer display
        if self.timer_started and not self.game_over:
            current_time = (pygame.time.get_ticks() - self.start_time) / 1000 # converts from milliseconds to seconds
        else:
            current_time = self.elapsed_time # Will be 0 if restarted, or final time if game over

        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        time_str = f"{minutes:02}:{seconds:02}"

        font = pygame.font.Font(None, 36)
        timer_text = font.render(time_str, True, self.BLACK)
        timer_rect = timer_text.get_rect(topright=(757, 475))  
        self.screen.blit(timer_text, timer_rect)
    
    def check_game_over(self):
        """Checks if the game has ended (no moves left or board full)."""
        no_moves_black = len(self.game.board.remaining_moves('B')) == 0
        no_moves_white = len(self.game.board.remaining_moves('W')) == 0
        board_full = not any('.' in row for row in self.game.board.board)

        if (no_moves_black and no_moves_white) or board_full:
            self.game_over = True
            return True
        return False

    def draw_ending_screen(self):
        """Draws the game over overlay with final scores and winner."""

        # shadow overlay
        overlay = pygame.Surface((self.screen_size, self.screen_size), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha for shadow effect
        self.screen.blit(overlay, (0, 0))

        # display final scores and game duration
        font_title = pygame.font.Font(None, 48)
        font_info = pygame.font.Font(None, 36)

        # title
        title_text = font_title.render("Game Over", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_size // 2, 100))
        self.screen.blit(title_text, title_rect)

        # scores
        black_score = self.game.score['B']
        white_score = self.game.score['W']
        winner = self.game.winner()
        score_text = font_info.render(f"Black: {black_score} - White: {white_score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.screen_size // 2, 180))
        winner_text = font_info.render(f"{winner}", True, self.WHITE)
        winner_rect = winner_text.get_rect(center=(self.screen_size // 2, 240))
        self.screen.blit(score_text, score_rect)
        self.screen.blit(winner_text, winner_rect)
        
        # timer
        timer_text = font_info.render(f"Time: {self.elapsed_time:.2f} s", True, self.WHITE)
        timer_rect = timer_text.get_rect(center=(self.screen_size // 2, 300))
        self.screen.blit(timer_text, timer_rect)


    def run(self):
        """Main game loop handling events, logic updates, and rendering."""
        running = True

        while running:
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "MENU":
                        self.handle_menu_click(event.pos)
                    else:
                        self.handle_click(event.pos)
                            
            # game Logic Updates
            if self.state == "GAME":
                if self.check_game_over():
                    self.game_over = True
                
                # timer Logic
                if self.timer_started and not self.game_over:
                    self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

                # bot turn logic
                # if mode is PvBot, game isn't over, and it's the bot's color
                if (self.game_mode == "PvBot" and 
                    not self.game_over and 
                    self.game.color == self.bot_color):
                    
                    if self.bot_delay_start is None:
                        self.bot_delay_start = pygame.time.get_ticks()
                    
                    # Check if 1 second (1000ms) has passed before the bot makes a move
                    current_ticks = pygame.time.get_ticks()
                    if current_ticks - self.bot_delay_start >= 1000:
                        self.perform_bot_move()
                        self.bot_delay_start = None # Reset the timer for the next turn
                    
                
            # rendering
            self.screen.fill(self.WHITE)
            if self.state == "MENU":
                self.draw_menu()
            else:
                self.draw_game_interface()
                if self.game_over:
                    self.draw_ending_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def draw_menu(self):
            """Renders the main interface"""
            # overlay
            overlay = pygame.Surface((self.screen_size + 250, self.screen_size))
            overlay.fill(self.DARK_GREEN)
            self.screen.blit(overlay, (0, 0))

            # title
            font_title = pygame.font.Font(None, 80)
            text_title = font_title.render("OTHELLO", True, self.WHITE)
            rect_title = text_title.get_rect(center=((self.screen_size + 250) // 2, 150))
            self.screen.blit(text_title, rect_title)

            mouse_pos = pygame.mouse.get_pos()
            for key, rect in self.menu_buttons.items():
                color = self.LIGHT_GRAY if rect.collidepoint(mouse_pos) else self.WHITE
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 3)

                label = "Player vs Player" if key == "pvp" else "Player vs Bot"
                font_btn = pygame.font.Font(None, 40)
                text_btn = font_btn.render(label, True, self.BLACK)
                text_rect = text_btn.get_rect(center=rect.center)
                self.screen.blit(text_btn, text_rect)

    def draw_game_interface(self):
        """Helper to draw all game components."""
        self.draw_board()
        self.draw_discs()
        self.highlight_valid_moves()
        self.draw_buttons()
        self.draw_game_info()
        self.show_feedback(self.feedback_message)

if __name__ == "__main__":
    interface = Interface()
    interface.run()
