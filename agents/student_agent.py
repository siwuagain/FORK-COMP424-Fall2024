# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
import copy
import time
from helpers import execute_move, check_endgame, get_valid_moves
from custom_utils import logger

BLUE = '\033[34m'
DEFAULT = '\033[0m'

logger = logger.Logger()
@register_agent("student_agent")
class StudentAgent(Agent):
  """
  A class for your implementation. Feel free to use this class to
  add any helper functionalities needed for your agent.
  """

  def __init__(self):
    super(StudentAgent, self).__init__()
    self.name = "StudentAgent"

  def step(self, chess_board, player, opponent):
    """
    Implement the step function of your agent here.
    You can use the following variables to access the chess board:
    - chess_board: a numpy array of shape (board_size, board_size)
      where 0 represents an empty spot, 1 represents Player 1's discs (Blue),
      and 2 represents Player 2's discs (Brown).
    - player: 1 if this agent is playing as Player 1 (Blue), or 2 if playing as Player 2 (Brown).
    - opponent: 1 if the opponent is Player 1 (Blue), or 2 if the opponent is Player 2 (Brown).

    You should return a tuple (r,c), where (r,c) is the position where your agent
    wants to place the next disc. Use functions in helpers to determine valid moves
    and more helpful tools.

    Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
    """
    logger.info(f"STUDENT AGENT STEP {DEFAULT}{BLUE}<< START >>{DEFAULT}")

    start_time = time.time()

    if chess_board.shape[0] == 6 or chess_board.shape[0] == 8:
      max_depth = 4
    else:
      max_depth = 3
    
    val, move = self.minimax(0, max_depth, chess_board, True, player, opponent, float("-inf"), float("inf"), start_time)
   
    
    time_taken = time.time() - start_time
    print("My AI's turn took ", time_taken, "seconds.")


    logger.debug("MOVE: " + str(move))
    logger.info(f"STUDENT AGENT STEP {DEFAULT}{BLUE}<< END >>{DEFAULT}")
    return move
  



  def evaluate_board(self, board, player, opponent):

#checking if this is the last move
    is_endgame, s1, s2 = check_endgame(board, player, opponent)

    if player == 1:
      score1 = s1
      score2 = s2
    else:
      score1 = s2
      score2 = s1

    if is_endgame:
      if (score1 > score2):
        return float("inf"), None
      elif (score1 == score2):
        return 0, None
      else:
        return float("-inf"), None
      
    rows, cols = board.shape

    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
    adjacent_to_corners = [(1, 0), (0, 1), (rows - 2, 0), (rows - 1, 1), (0, cols - 2), (1, cols - 1), (rows - 2, cols - 1), (rows - 1, cols - 2)]
    corner_gifters = [(1, 1), (1, cols - 2), (rows - 2, 1), (rows - 2, cols - 2)]
    step_to_corners = [(0, 2), (2, 0), (rows - 3, 0), (rows - 1, 2), (0, cols - 3), (2, cols - 1), (rows - 1, cols - 3), (rows - 3, cols - 1)]
    inner_corners = [(2,2), (2, cols - 3), (rows - 3, 2), (rows - 3, cols - 3)]
    
#mobility score
    player_moves = len(get_valid_moves(board, player))
    opponent_moves = len(get_valid_moves(board, opponent))

    mobility_score = 100 * (player_moves - opponent_moves)/ (player_moves + opponent_moves)

#point score
    if score1 == score2:
      point_score = 0
    else:
      point_score = 100* (score1 - score2) / (score1 + score2)

#corner score
    player_corner_score = 0
    opponent_corner_score = 0

    count = 0
    for corner in corners:
      if board[corner] == player:
        player_corner_score += 1
      elif board[corner] == opponent:
        opponent_corner_score += 1
      count+=1
    
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
          player_adj_score += 2
    
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

#total
    if rows == 8:
      step_to_corners_score = 0.7*step_to_corners_score
      inner_corner_score = 1.6*inner_corner_score
      mobility_score = 0.25*mobility_score
      if score1 + score2 >= (rows * cols) - 10:
        point_score = 3*point_score
    
    elif rows == 10:
      step_to_corners_score = 1.6*step_to_corners_score
      inner_corner_score = 0.7*inner_corner_score
      point_score = 0.8*point_score
      cg_score = 0.8*cg_score
      adj_score = 1.9*adj_score
      mobility_score = 0.2*mobility_score
      if score1 + score2 >= (rows * cols) - 12:
        point_score = 3*point_score

    elif rows == 12:
      step_to_corners_score = 1.2*step_to_corners_score
      mobility_score = 0.2*mobility_score
      inner_corner_score = 0.4*inner_corner_score
      point_score = 1.1*point_score
      cg_score = 1.2*cg_score
      adj_score = 1.6*adj_score
      corner_score = 1.1*corner_score
      if score1 + score2 >= (rows * cols) - 14:
        point_score = 4*point_score

    else:
      mobility_score = 0.1*mobility_score
      step_to_corners_score = 0.1*step_to_corners_score
      inner_corner_score = 0*inner_corner_score
      adj_score = 1.2*adj_score
      cg_score = 0*cg_score
      point_score = 1.2*point_score
      corner_score = 1.2*corner_score

    board_value = 3*corner_score + mobility_score + 0.2*adj_score + 0.3*cg_score + point_score + step_to_corners_score + 0.1*inner_corner_score
    return board_value, None
  
  

  def minimax(self,
              depth, 
              max_depth,
              board, 
              is_maximizing,
              player,
              opponent,
              alpha, 
              beta,
              start_time):
        
    is_endgame, _, _ = check_endgame(board, player, opponent)
    #basecase
    if is_endgame or depth == max_depth or time.time() - start_time >= 1.85 or (depth == max_depth -1 and time.time() - start_time >= 1.72):
      return self.evaluate_board(board, player, opponent)
    
    

    #MAXIMIZING PLAYER
    if is_maximizing:
      best_val = float('-inf')
      best_move = None
      legal_moves = get_valid_moves(board, player)

      for cur_move in legal_moves:
        simulated_board = copy.deepcopy(board)
        execute_move(simulated_board, cur_move, player)

        val, _ = self.minimax(depth+1, max_depth, simulated_board, False, player, opponent, alpha, beta, start_time)
        if val >= best_val:
          best_val = val
          best_move = cur_move

        alpha = max(alpha, best_val)
        if beta <= alpha:
          break

      if len(legal_moves) == 0:
        best_val = -5000
        best_move = None

      return best_val, best_move

    #MINIMIZING PLAYER
    else:
      best_val = float("inf")
      best_move = None
      legal_moves = get_valid_moves(board, opponent)

      for cur_move in legal_moves:
        simulated_board = copy.deepcopy(board)
        execute_move(simulated_board, cur_move, opponent)

        val, _ = self.minimax(depth+1, max_depth, simulated_board, True, player, opponent, alpha, beta, start_time)
        
        if val <= best_val:
          best_val = val
          best_move = cur_move

        beta = min(beta, best_val)
        if beta <= alpha:
          break
      
      if len(legal_moves) == 0:
        best_val = 5000
        best_move = None

      return best_val, best_move
    