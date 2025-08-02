
import random
from typing import Callable, List, Tuple


# global variables --- not good to use in production code   
Board = Tuple[Tuple[str, ...], ...]
Player = str
Move = Tuple[int, int]

#################################################################################
def create_board() -> Board:
    """Create a 3x3 Tic Tac Toe board."""
    return ((" ", " ", " "),
            (" ", " ", " "),
            (" ", " ", " "))
#################################################################################


def get_cell(board: Board, row: int, col: int) -> str:
    """Get the value of a cell in the board."""
    return board[row][col]

#################################################################################    
def set_cell(board: Board, row: int, col: int, player: Player) -> Board:
    """return a new board with the value set in the specified cell.
    Does not modify the original board."""
    #convert the board to a list of lists from a tuple of tuples to modify it
    new_board_list = [list(row) for row in board]
    if 0 <= row < 3 and 0 <= col < 3 and  new_board_list[row][col] == ' ':
        new_board_list[row][col] = player
        return tuple(tuple(row) for row in new_board_list)
    return board  # Return the original board if the move is invalid

#################################################################################
def check_line(line: Tuple[str, ...], player: Player) -> bool:
    """Check if a line (row, column, or diagonal) has the same player's symbol."""
    return all(cell == player for cell in line)

#################################################################################
def is_valid_move(board: Board, row: int, col: int) -> bool:
    """Check if a move is valid (i.e., the cell is empty)."""
    return 0<= row < 3 and 0 <= col < 3 and get_cell(board, row, col) == " "

#################################################################################
def get_available_moves(board: Board) -> List[Move]:
    """Get a list of available moves on the board."""
    return [(row, col) for row in range(3) for col in range(3) if get_cell(board, row, col) == ' ']
#################################################################################
def check_win(board: Board, player: Player) -> bool:  
    """Check if a player has won the game."""
    # Check rows
    for row_idx in range(3):
        if check_line(board[row_idx], player):
            return True
    # Check columns
    for col_idx in range(3):
        if check_line(tuple(board[row_idx][col_idx] for row_idx in range(3)), player):  
            return True
        
    # Check diagonals
    diagonal1 = tuple(board[i][i] for i in range(3))
    diagonal2 = tuple(board[i][2 - i] for i in range(3))
    
    if check_line(diagonal1, player) or check_line(diagonal2, player):
        return True
    return False
    
    # for col_idx in range(3):
    #     for row_idx in range(3):
    #         check_line(board[row_idx][col_idx], player)
#################################################################################
 
def is_draw(board: Board) -> bool:
    """Check if the game is a draw."""
    return not check_win(board, 'X') and not check_win(board, 'O') and all(cell != ' ' for row in board for cell in row)  
#################################################################################
def display_board_cli(board: Board) -> None:
    """Display the Tic Tac Toe board in the CLI."""
    print("\n\t 0 \t 1 \t 2")
    for i, row in enumerate(board):
        print(f"{i} \t {'| \t'.join(row)}")
        if i < 2:
            print("  -------------------------- ")
    print("\n")
#################################################################################
def get_human_move(board: Board, player_symbol: Player) -> Move:
    """ Get a move from the human player."""
    while True:
        try:
            print(f"Player {player_symbol}, enter your move (row and column, e.g '0 1'): ")
            move_str = input().strip()
            row, col = int (move_str[0]), int(move_str[1])
            if is_valid_move(board, row, col):
                return (row, col)
            else:
                print("Invalid move. Cell is already occupied or out of bounds. Try again.")        
            
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column numbers separated by a space. Try again.")
#################################################################################
def get_computer_move_simple(board: Board, computer_symbol: Player) -> Move:
    """ 
    A simple 'percepton-like' using if-else statements to choose a move.
    1. win if possible
    2. block opponent if they are about to win
    3. take centre position if available
    4. take any corner position if available
    5. take any other available position
    """
    
    opponent_symbol = 'O' if computer_symbol == 'X' else 'X'
    available_moves = get_available_moves(board)
    
    # 1. Check if the computer can win in the next move
    for move in available_moves:
        temp_board = set_cell(board, move[0], move[1], computer_symbol)
        if check_win(temp_board, computer_symbol):
            print(f"Computer chooses to win at {move}")
            return move
        
    # 2. Check if the opponent can win in the next move and block them
    for move in available_moves:
        temp_board = set_cell(board, move[0], move[1], opponent_symbol)
        if check_win(temp_board, opponent_symbol):
            print(f"Computer blocks at {move}")
            return move
    
    # 3. Take the center position if available  
    if is_valid_move(board, 1, 1):
        print("Computer takes center position")
        return (1, 1)
    # 4. Take any corner position if available
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)  # Shuffle corners to add randomness
    for move in corners:
        if is_valid_move(board, move[0], move[1]):
            print(f"Computer takes corner position at {move}")
            return move 
    # 5. Take any other available position
    
    return random.choice(available_moves) if available_moves else (0,0) # fallback to (0,0) if no moves available
#################################################################################
    

def game_loop(board: Board, 
              current_player_symbol: Player, 
              player_x_turn: Callable[[Board, Player], Move], 
              player_o_turn: Callable[[Board, Player], Move]
              ) -> None:
    """Main game loop for Tic Tac Toe."""
    
    display_board_cli(board)
    
    if check_win(board, 'X'):
        print("Player X wins!")
        return
    
    if check_win(board, 'O'):
        print("Player O wins!")
        return
    
    if is_draw(board):
        print("It's a draw!")
        return
    
    if current_player_symbol == 'X':
        move = player_x_turn(board, 'X')
    else:
        move = player_o_turn(board, 'O')
        
    if move:
        row, col = move 
        if is_valid_move(board, row, col):
            new_board= set_cell(board, row, col, current_player_symbol)
            next_player_symbol = 'O' if current_player_symbol == 'X' else 'X'
            game_loop(new_board, next_player_symbol, player_x_turn, player_o_turn)
        else:
            print("Invalid move. Try again.")
    else:
        print("No move made. This indicates an issue in a player strategy.")
        
            
    
def main():
    """Main function to run the Tic Tac Toe game."""
    print("Welcome to Tic Tac Toe!")
    
    while True: # Loop until a valid mode is chosen
        mode = input ("Choose a mode (1: Player vs Computer(AI)\n  or 2: Player vs Player): ")
        if mode in ["1", "2"]:
            break
        print("Invalid mode. Please choose 1 or 2.")
        
    init_board = create_board()

    if mode == "1":
        human_first = input("Do you want to play first? ie Do you want to play as 'X' (y/n): ").strip().lower()
        
        if human_first == "y":
            print("You are 'X' and the computer is 'O'.")
            player_x_strategy = get_human_move
            player_o_strategy = get_computer_move_simple
            
        else:
            print("You are 'O' and the computer is 'X'.")
            player_x_strategy = get_computer_move_simple
            player_o_strategy = get_human_move
        game_loop(init_board, 'X', player_x_strategy, player_o_strategy)
    else: #mode == "2"
        print("player X vs player O")
        game_loop(init_board, 'X', get_human_move, get_human_move)
    print("Game Over!, thanks for playing!")            
            
            
if __name__ == "__main__":
    main()