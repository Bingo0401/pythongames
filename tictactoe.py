import pygame
import sys
import math
import random

WIDTH, HEIGHT = 600, 680
LINE_WIDTH     = 6
BOARD_ROWS     = 3
BOARD_COLS     = 3
CELL_SIZE      = WIDTH // 3
CIRCLE_RADIUS  = CELL_SIZE // 3
CIRCLE_WIDTH   = 10
CROSS_WIDTH    = 12
CROSS_SPACE    = 40


BG_COLOR        = (28,  28,  40)
LINE_COLOR      = (70,  70, 100)
CIRCLE_COLOR    = (239, 116, 116)  
CROSS_COLOR     = (100, 200, 240)   
WIN_LINE_COLOR  = (255, 215,   0)  
TEXT_COLOR      = (220, 220, 240)
ACCENT_COLOR    = (120, 100, 220)
BTN_COLOR       = (50,  50,  80)
BTN_HOVER       = (80,  70, 130)
BTN_BORDER      = (120, 100, 220)

BOARD_TOP = 80          

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock  = pygame.time.Clock()

font_large  = pygame.font.SysFont("segoeui", 52, bold=True)
font_medium = pygame.font.SysFont("segoeui", 30, bold=True)
font_small  = pygame.font.SysFont("segoeui", 22)

def new_board():
    return [[None]*3 for _ in range(3)]

def available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]

def check_winner(board):
    lines = [
        [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],
    ]
    for line in lines:
        vals = [board[r][c] for r,c in line]
        if vals[0] and vals[0] == vals[1] == vals[2]:
            return vals[0], line
    return None, None

def is_draw(board):
    return all(board[r][c] for r in range(3) for c in range(3))

def minimax(board, is_max, alpha=-math.inf, beta=math.inf):
    winner, _ = check_winner(board)
    if winner == 'O': return 10
    if winner == 'X': return -10
    if is_draw(board):  return 0

    if is_max:
        best = -math.inf
        for r, c in available_moves(board):
            board[r][c] = 'O'
            best = max(best, minimax(board, False, alpha, beta))
            board[r][c] = None
            alpha = max(alpha, best)
            if beta <= alpha: break
        return best
    else:
        best = math.inf
        for r, c in available_moves(board):
            board[r][c] = 'X'
            best = min(best, minimax(board, True, alpha, beta))
            board[r][c] = None
            beta = min(beta, best)
            if beta <= alpha: break
        return best

def ai_move(board):
    best_score = -math.inf
    best_cell  = None
    for r, c in available_moves(board):
        board[r][c] = 'O'
        score = minimax(board, False)
        board[r][c] = None
        if score > best_score:
            best_score = score
            best_cell  = (r, c)
    return best_cell

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * CELL_SIZE, BOARD_TOP),
                         (i * CELL_SIZE, BOARD_TOP + WIDTH), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR,
                         (0, BOARD_TOP + i * CELL_SIZE),
                         (WIDTH, BOARD_TOP + i * CELL_SIZE), LINE_WIDTH)

def draw_marks(board):
    for r in range(3):
        for c in range(3):
            mark = board[r][c]
            cx = c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
            if mark == 'X':
                # Draw X as two lines
                s = CROSS_SPACE
                pygame.draw.line(screen, CIRCLE_COLOR,
                                 (cx - CELL_SIZE//2 + s, cy - CELL_SIZE//2 + s),
                                 (cx + CELL_SIZE//2 - s, cy + CELL_SIZE//2 - s), CROSS_WIDTH)
                pygame.draw.line(screen, CIRCLE_COLOR,
                                 (cx + CELL_SIZE//2 - s, cy - CELL_SIZE//2 + s),
                                 (cx - CELL_SIZE//2 + s, cy + CELL_SIZE//2 - s), CROSS_WIDTH)
            elif mark == 'O':
                pygame.draw.circle(screen, CROSS_COLOR, (cx, cy), CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_win_line(line):
    (r1, c1), _, (r2, c2) = line[0], line[1], line[2]
    x1 = c1 * CELL_SIZE + CELL_SIZE // 2
    y1 = BOARD_TOP + r1 * CELL_SIZE + CELL_SIZE // 2
    x2 = c2 * CELL_SIZE + CELL_SIZE // 2
    y2 = BOARD_TOP + r2 * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, WIN_LINE_COLOR, (x1, y1), (x2, y2), 8)

def draw_status(text):
    pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, BOARD_TOP))
    surf = font_medium.render(text, True, TEXT_COLOR)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, BOARD_TOP//2 - surf.get_height()//2))

def draw_button(rect, text, hovered):
    color = BTN_HOVER if hovered else BTN_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, BTN_BORDER, rect, 2, border_radius=12)
    surf = font_medium.render(text, True, TEXT_COLOR)
    screen.blit(surf, (rect.centerx - surf.get_width()//2,
                       rect.centery - surf.get_height()//2))

def menu_screen():
    btn_friend = pygame.Rect(WIDTH//2 - 160, 300, 320, 60)
    btn_ai     = pygame.Rect(WIDTH//2 - 160, 390, 320, 60)

    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)

        title = font_large.render("Tic Tac Toe", True, ACCENT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 140))

        sub = font_small.render("Choose a game mode", True, (150, 150, 180))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 230))

        draw_button(btn_friend, "👥  Play with Friend", btn_friend.collidepoint(mx, my))
        draw_button(btn_ai,     "🤖  Play vs AI",       btn_ai.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_friend.collidepoint(mx, my):
                    return "friend"
                if btn_ai.collidepoint(mx, my):
                    return "ai"

        pygame.display.flip()
        clock.tick(60)

def end_screen(message):
    """Show result and ask to play again or go to menu."""
    btn_again = pygame.Rect(WIDTH//2 - 200, 420, 180, 55)
    btn_menu  = pygame.Rect(WIDTH//2 + 20,  420, 180, 55)

    while True:
        mx, my = pygame.mouse.get_pos()
        # keep game board visible in background (already drawn)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((28, 28, 40, 200))
        screen.blit(overlay, (0, 0))

        msg_surf = font_large.render(message, True, WIN_LINE_COLOR)
        screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 300))

        draw_button(btn_again, "Play Again", btn_again.collidepoint(mx, my))
        draw_button(btn_menu,  "Main Menu",  btn_menu.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_again.collidepoint(mx, my): return "again"
                if btn_menu.collidepoint(mx, my):  return "menu"

        pygame.display.flip()
        clock.tick(60)

def game_loop(mode):
    board   = new_board()
    current = 'X'          
    game_over = False
    winner_line = None
    winner_mark = None
    ai_thinking = False     

    player_labels = {
        'friend': {'X': 'Player 1 (X)', 'O': 'Player 2 (O)'},
        'ai':     {'X': 'Your turn (X)', 'O': 'AI thinking…'},
    }

    def status_text():
        if winner_mark:
            if mode == 'ai':
                return "You win! 🎉" if winner_mark == 'X' else "AI wins! 🤖"
            return f"{player_labels[mode][winner_mark]} wins! 🎉"
        if is_draw(board):
            return "It's a draw! 🤝"
        return player_labels[mode][current]

    while True:
        screen.fill(BG_COLOR)
        draw_grid()
        draw_marks(board)
        if winner_line:
            draw_win_line(winner_line)
        draw_status(status_text())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if mode == 'friend' or (mode == 'ai' and current == 'X'):
                    mx, my = pygame.mouse.get_pos()
                    if my > BOARD_TOP:
                        col = mx // CELL_SIZE
                        row = (my - BOARD_TOP) // CELL_SIZE
                        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None:
                            board[row][col] = current
                            winner_mark, winner_line = check_winner(board)
                            if winner_mark or is_draw(board):
                                game_over = True
                            else:
                                current = 'O' if current == 'X' else 'X'

 
        if mode == 'ai' and current == 'O' and not game_over:
            pygame.display.flip()
            pygame.time.delay(350)          
            r, c = ai_move(board)
            board[r][c] = 'O'
            winner_mark, winner_line = check_winner(board)
            if winner_mark or is_draw(board):
                game_over = True
            else:
                current = 'X'

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            pygame.time.delay(400)
           
            screen.fill(BG_COLOR)
            draw_grid()
            draw_marks(board)
            if winner_line:
                draw_win_line(winner_line)
            draw_status(status_text())
            pygame.display.flip()

            result = end_screen(status_text())
            return result

def main():
    mode = menu_screen()
    while True:
        result = game_loop(mode)
        if result == "menu":
            mode = menu_screen()
    

if __name__ == "__main__":
    main()
