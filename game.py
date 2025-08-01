import tkinter as tk
import math

# Initialize board
board = [' ' for _ in range(9)]

# Check win conditions
def is_winner(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in cond) for cond in win_conditions)

def is_draw():
    return all(cell != ' ' for cell in board)

def get_available_moves():
    return [i for i, cell in enumerate(board) if cell == ' ']

# Minimax with alpha-beta pruning
def minimax(depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    if is_winner('O'):
        return 1
    elif is_winner('X'):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in get_available_moves():
            board[move] = 'O'
            eval = minimax(depth + 1, False, alpha, beta)
            board[move] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_available_moves():
            board[move] = 'X'
            eval = minimax(depth + 1, True, alpha, beta)
            board[move] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_move():
    best_score = -math.inf
    best_move = None
    for move in get_available_moves():
        board[move] = 'O'
        score = minimax(0, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move] = 'O'
    update_button(best_move)
    check_game_over()

# GUI setup
root = tk.Tk()
root.title("Tic Tac Toe AI")

buttons = []

def update_button(index):
    buttons[index]['text'] = board[index]
    buttons[index]['state'] = 'disabled'

def on_click(index):
    if board[index] == ' ':
        board[index] = 'X'
        update_button(index)
        check_game_over()
        if not is_winner('X') and not is_draw():
            root.after(500, ai_move)

def set_background_color(color):
    root.configure(bg=color)
    status_label.configure(bg=color)
    for btn in buttons:
        btn.configure(bg=color)

def check_game_over():
    if is_winner('X'):
        status_label.config(text="You win!")
        set_background_color("#90EE90")  # Light green
        disable_all_buttons()
    elif is_winner('O'):
        status_label.config(text="AI wins!")
        set_background_color("#FF6666")  # Soft red
        disable_all_buttons()
    elif is_draw():
        status_label.config(text="It's a draw!")
        set_background_color("#FFD700")  # Gold
        disable_all_buttons()
def disable_all_buttons():
    for btn in buttons:
        btn['state'] = 'disabled'

def reset_game():
    global board
    board = [' ' for _ in range(9)]
    for btn in buttons:
        btn.config(text=' ', state='normal', bg='SystemButtonFace')
    status_label.config(text="Your turn!", bg='SystemButtonFace')
    root.configure(bg='SystemButtonFace')

reset_btn = tk.Button(root, text="Restart", font=('Arial', 14), command=reset_game)
reset_btn.grid(row=4, column=0, columnspan=3, pady=10)

# Create buttons
for i in range(9):
    btn = tk.Button(root, text=' ', font=('Arial', 24), width=5, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

status_label = tk.Label(root, text="Your turn!", font=('Arial', 16))
status_label.grid(row=3, column=0, columnspan=3)

root.mainloop()