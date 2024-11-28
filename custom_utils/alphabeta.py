from helpers import get_valid_moves, count_capture, execute_move, check_endgame
from custom_utils import logger
import copy

BLUE = '\033[34m'
DEFAULT = '\033[0m'

logger = logger.Logger()
class Minimax:
  def __init__(self, max_depth = 3):
    self.name = "Minimax"
    self.max_depth = max_depth
  
  def minimax(self, 
              depth, 
              board, 
              player,
              opponent,
              alpha = float('-inf'), 
              beta = float('inf')):
    
    #basecase
    is_endgame, player_score, opponent_score = check_endgame(board, player, player_score)
    if is_endgame or depth == self.max_depth:
      return self.evaluate_board(board, color, player_score, opponent_score) #only a placeholder, what should be the score?
    
    legal_moves = get_valid_moves(board, player)
    
    #MAXIMIZING PLAYER
    if player == 1:
      best_val = float('-inf')
      best_move = None

      for move in legal_moves:
        simulated_board = copy.deepcopy(board)
        execute_move(simulated_board, move, player)

        val = self.minimax(depth+1, simulated_board, opponent, player, opponent_score, player_score, alpha, beta)
        if val > best_val:
          best_val = val
          best_move = move

        alpha= max(alpha, best_val)
        if beta <= alpha:
          break

      return best_val, best_move

    #MINIMIZING PLAYER
    else:
      best_val = float("inf")
      best_move = None
      for move in legal_moves:
        simulated_board = copy.deepcopy(board)
        execute_move(simulated_board, move, player)

        val = self.minimax(depth+1, simulated_board, opponent, player, alpha, beta)
        
        if val < best_val:
          best_val = val
          best_move = move

        beta = min(beta, best_val)
        if beta <= alpha:
          break

      return best_val, best_move


  def evaluate_board(self, board, color, player_score, opponent_score):
    """
    Evaluate the board state based on multiple factors.

    Parameters:
    - board: 2D numpy array representing the game board.
    - color: Integer representing the agent's color (1 for Player 1/Blue, 2 for Player 2/Brown).
    - player_score: Score of the current player.
    - opponent_score: Score of the opponent.

    Returns:
    - int: The evaluated score of the board.
    """
    # Corner positions are highly valuable
    corners = [(0, 0), (0, board.shape[1] - 1), (board.shape[0] - 1, 0), (board.shape[0] - 1, board.shape[1] - 1)]
    corner_score = sum(1 for corner in corners if board[corner] == color) * 10
    corner_penalty = sum(1 for corner in corners if board[corner] == 3 - color) * -10

    # Mobility: the number of moves the opponent can make
    opponent_moves = len(get_valid_moves(board, 3 - color))
    mobility_score = -opponent_moves

    # Combine scores
    total_score = player_score - opponent_score + corner_score + corner_penalty + mobility_score
    return total_score


