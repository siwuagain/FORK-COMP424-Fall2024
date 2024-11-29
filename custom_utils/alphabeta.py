from helpers import get_valid_moves, count_capture, execute_move, check_endgame, count_capture_dir
from custom_utils import logger
import copy

BLUE = '\033[34m'
DEFAULT = '\033[0m'

logger = logger.Logger()
class Minimax:
  def __init__(self, max_depth = 3):
    self.name = "Minimax"
    self.max_depth = max_depth



  def evaluate_board(self, board, player, opponent):

    is_endgame, score1, score2 = check_endgame(board, player, opponent)
    if is_endgame:
      if (score1 > score2):
        return float("inf")
      else:
        return float("-inf")

    #memo: board.shape[0]=number of rows, board.shape[1]=number of columns
    corners = [(0, 0), (0, board.shape[1] - 1), (board.shape[0] - 1, 0), (board.shape[0] - 1, board.shape[1] - 1)]
    adjacent_to_corners = [(1, 0), (0, 1), (board.shape[0] - 2, 0), (board.shape[0] - 1, 1), (0, board.shape[1] - 2), (1, board.shape[1] - 1), (board.shape[0] - 2, board.shape[1] - 1), (board.shape[0] - 1, board.shape[1] - 2)]
    corner_gifters = [(1, 1), (1, board.shape[1] - 2), (board.shape[0] - 2, 1), (board.shape[0] - 2, board.shape[1] - 2)]
    step_to_corners = [(0, 2), (2, 0), (board.shape[0] - 3, 0), (board.shape[0] - 1, 2), (0, board.shape[1] - 3), (2, board.shape[1] - 1), (board.shape[0] - 1, board.shape[1] - 3), (board.shape[0] - 3, board.shape[1] - 1)]
    inner_corners = [(2,2), (2, board.shape[1] - 3), (board.shape[0] - 3, 2), (board.shape[0] - 3, board.shape[1] - 3)]

#mobility score

    player_moves = len(get_valid_moves(board, player))
    opponent_moves = len(get_valid_moves(board, opponent))

    mobility_score = 100 * (player_moves - opponent_moves)/ (player_moves + opponent_moves)

#corner score
    player_corner_score = 0
    opponent_corner_score = 0

    for corner in corners:
      if board[corner] == player:
        player_corner_score += 1
      elif board[corner] == opponent:
        opponent_corner_score += 1
    
    if (player_corner_score + opponent_corner_score) == 0:
      corner_score = 0
    else:
      corner_score = 100 * (player_corner_score - opponent_corner_score) / (player_corner_score + opponent_corner_score)

#adjacent to corner score
    player_adj_score = 0
    opponent_adj_score = 0

    count = -1
    for adj in adjacent_to_corners:
      count += 1

      if board[adj] == player:
        if (count in (0, 1)) and (board[corners[0]]==player):
          player_adj_score += 1
        elif (count in (2, 3)) and (board[corners[2]]==player):
          player_adj_score += 1
        elif (count in (4, 5)) and (board[corners[1]]==player):
          player_adj_score += 1
        elif (count in (6, 7)) and (board[corners[3]]==player):
          player_adj_score += 1
        else:
          opponent_adj_score += 2

      elif board[adj] == opponent:
        if (count in (0, 1)) and (board[corners[0]]==opponent):
          opponent_adj_score += 1
        elif (count in (2, 3)) and (board[corners[2]]==opponent):
          opponent_adj_score += 1
        elif (count in (4, 5)) and (board[corners[1]]==opponent):
          opponent_adj_score += 1
        elif (count in (6, 7)) and (board[corners[3]]==opponent):
          opponent_adj_score += 1
        else:
          player_adj_score -= 2 #will need to figure out an actual number. Risking giving a corner is worth more than growing the corner line
    
    if (player_adj_score + opponent_adj_score) == 0:
      adj_score = 0
    else:
      adj_score = 100 * (player_adj_score - opponent_adj_score) / (player_adj_score + opponent_adj_score)


#inner corner score
    inner_corner_player_score = 0
    inner_corner_opponent_score = 0

    for inner_corner in inner_corners:
      if board[inner_corner] == player:
        inner_corner_player_score += 1
      elif board[inner_corner] == opponent:
        inner_corner_opponent_score += 1
    
    if (inner_corner_player_score + inner_corner_opponent_score) == 0:
      inner_corner_score = 0
    else:
      inner_corner_score = 100 * (inner_corner_player_score - inner_corner_opponent_score) / (inner_corner_player_score + inner_corner_opponent_score)

#corner gifter score
    player_cg_score = 0
    opponent_cg_score = 0

    count = 0
    for cg in corner_gifters:
      if board[cg] == player and board[corners[count]] != player:
        opponent_cg_score += 1
      elif board[cg] == opponent and board[corners[count]] != opponent:
        player_cg_score += 1
      count += 1
    
    if player_cg_score + opponent_cg_score == 0:
      cg_score = 0
    else:
      cg_score = 100 * (player_cg_score - opponent_cg_score) / (player_cg_score + opponent_cg_score)

#step to corner score
    player_step_score = 0
    opponent_step_score = 0

    count = 0
    for st_corner in step_to_corners: 

      if board[st_corner] == player:
        if count in (0, 1):
          if (board[corners[0]] != player and board[corners[0]] != opponent):
            player_step_score += 1
        elif count in (2, 3):
          if (board[corners[2]] != player and board[corners[2]] != opponent):
            player_step_score += 1
        elif count in (4, 5):
          if (board[corners[1]] != player and board[corners[1]] != opponent):
            player_step_score += 1
        else:
          if (board[corners[3]] != player and board[corners[3]] != opponent):
            player_step_score += 1
      
      elif board[st_corner] == opponent:
        if count in (0, 1):
          if (board[corners[0]] != player and board[corners[0]] != opponent):
            opponent_step_score += 1
        elif count in (2, 3):
          if (board[corners[2]] != player and board[corners[2]] != opponent):
            opponent_step_score += 1
        elif count in (4, 5):
          if (board[corners[1]] != player and board[corners[1]] != opponent):
            opponent_step_score += 1
        else:
          if (board[corners[3]] != player and board[corners[3]] != opponent):
            opponent_step_score += 1

    if (player_step_score + opponent_step_score) == 0:
      step_to_corners_score = 0
    else: step_to_corners_score = 100 * (player_step_score - opponent_step_score) / (player_step_score + opponent_step_score)

    board_value = corner_score + mobility_score + adj_score + inner_corner_score + cg_score + step_to_corners_score

    return board_value, None
  
  

  def minimax(self,
              depth, 
              board, 
              is_maximizing,
              player,
              opponent,
              alpha = float('-inf'), 
              beta = float('inf')):
    
    legal_moves = get_valid_moves(board, player)
    is_endgame, _, _ = check_endgame(board, player, opponent)
    #basecase
    if is_endgame or depth == self.max_depth or len(legal_moves) == 0:
      return self.evaluate_board(board, player, opponent)
    
    
    
    #MAXIMIZING PLAYER
    if is_maximizing:
      best_val = float('-inf')
      best_move = None

      for cur_move in legal_moves:
        simulated_board = copy.deepcopy(board)
        execute_move(simulated_board, cur_move, player)

        val, _ = self.minimax(depth+1, simulated_board, False, player, opponent, alpha, beta)
        if val >= best_val:
          best_val = val
          best_move = cur_move

        alpha = max(alpha, best_val)
        if beta <= alpha:
          break

      return best_val, best_move

    #MINIMIZING PLAYER
    else:
      best_val = float("inf")
      best_move = None
      for cur_move in legal_moves:
        simulated_board = copy.deepcopy(board)
        execute_move(simulated_board, cur_move, opponent)

        val, _ = self.minimax(depth+1, simulated_board, True, player, opponent, alpha, beta)
        
        if val <= best_val:
          best_val = val
          best_move = cur_move

        beta = min(beta, best_val)
        if beta <= alpha:
          break

      return best_val, best_move


  