import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")

        self.board = [' ' for _ in range(9)]  # 게임 보드 초기화

        self.buttons = []
        for i in range(9):
            button = tk.Button(master, text='', font=('Helvetica', 20), width=4, height=2,
                               command=lambda idx=i: self.button_click(idx))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

        self.player_mark = 'X'
        self.computer_mark = 'O'
        self.player_turn = True
        self.mode_selection()

    def mode_selection(self):
        mode_frame = tk.Frame(self.master)
        mode_frame.grid(row=3, columnspan=3)
        tk.Label(mode_frame, text="Select mode:").pack()

        self.mode_var = tk.StringVar(value="1")  # 기본값은 유저 대 유저 대결

        tk.Radiobutton(mode_frame, text="Player vs Player", variable=self.mode_var, value="1").pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="Player vs Computer (Easy)", variable=self.mode_var, value="2").pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="Player vs Computer (Hard)", variable=self.mode_var, value="3").pack(anchor=tk.W)

        tk.Button(mode_frame, text="Reset Game", command=self.reset_game).pack()

    def button_click(self, idx):
        if self.board[idx] == ' ':
            self.board[idx] = self.player_mark if self.player_turn else self.computer_mark
            self.buttons[idx].config(text=self.board[idx])
            if self.check_winner(self.board[idx]):
                if self.mode_var.get() == "1":
                    winner = "Player1" if self.board[idx] == self.player_mark else "Player2"
                else:
                    winner = "Player" if self.board[idx] == self.player_mark else "Computer"
                messagebox.showinfo("Winner", f"{winner} wins!")
                self.reset_board()
                return
            elif self.is_board_full():
                messagebox.showinfo("Draw", "Game tie")
                self.reset_board()
                return
            else:
                self.player_turn = not self.player_turn

            if self.mode_var.get() in ["2", "3"] and not self.player_turn:
                difficulty = "hard" if self.mode_var.get() == "3" else "easy"
                self.computer_move(difficulty)

    def computer_move(self, difficulty):
        move = compMove(self.board) if difficulty == "hard" else random.choice([idx for idx, letter in enumerate(self.board) if letter == " "])

        if move != -1:
            self.board[move] = self.computer_mark
            self.buttons[move].config(text=self.computer_mark)
            if self.check_winner(self.computer_mark):
                messagebox.showinfo("Winner", "Computer wins!")
            elif self.is_board_full():
                messagebox.showinfo("Draw", "Game tie")
            else:
                self.player_turn = True
        else:
            messagebox.showinfo("Draw", "Game tie")

    def check_winner(self, mark):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[idx] == mark for idx in combo):
                return True
        return False

    def is_board_full(self):
        return ' ' not in self.board

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.config(text='')
        self.player_turn = True

    def reset_game(self):
        self.reset_board()

def compMove(board):
    possibleMoves = [x for x, letter in enumerate(board) if letter == " "]
    move = -1

    for let in ['O','X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let

            if isWinner(boardCopy, let):
                move = i
                return move

    cornerOpen = [i for i in possibleMoves if i in [0, 2, 6, 8]]

    if cornerOpen:
        move = random.choice(cornerOpen)
        return move

    if 4 in possibleMoves:
        move = 4
        return move

    edgeOpen = [i for i in possibleMoves if i in [1, 3, 5, 7]]

    if edgeOpen:
        move = random.choice(edgeOpen)
        return move

    return move

def isWinner(board, letter):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if all(board[idx] == letter for idx in combo):
            return True
    return False

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
