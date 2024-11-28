# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves, count_capture_dir
from custom_utils import logger, alphabeta

BLUE = '\033[34m'
DEFAULT = '\033[0m'

logger = logger.Logger()
alphabeta = alphabeta.Minimax()
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

    _, player_score, opponent_score = check_endgame(chess_board, player, 3 - player)
    moves = get_valid_moves(chess_board, player)

    if not moves:
      return None
    
    best_value = -99999
    best_move = None

    if player_score + opponent_score >= (chess_board.shape[0] * chess_board.shape[1]) - 10:
      for move in moves:
        value = self.evaluate_end_move(chess_board, player, move, opponent)
        if value >= best_value:
          best_value = value
          best_move = move

    else:
      for move in moves:
        value = self.evaluate_move(chess_board, player, move, opponent)
        if value >= best_value:
          best_value = value
          best_move = move
      
    if best_move == None:
      return random_move(chess_board,player)


    # val = alphabeta.minimax(2, chess_board, player, player_score, opponent_score )

    # logger.info("VALUE: " + str(val))
    # moves = get_valid_moves(chess_board, player)
    # logger.debug("VALID MOVES: " + str(moves))
    # Some simple code to help you with timing. Consider checking 
    # time_taken during your search and breaking with the best answer
    # so far when it nears 2 seconds.
    start_time = time.time()
    time_taken = time.time() - start_time
    print("My AI's turn took ", time_taken, "seconds.")

    # Dummy return (you should replace this with your actual logic)
    # Returning a random valid move as an example

    logger.debug("MOVE: " + str(move))
    logger.info(f"STUDENT AGENT STEP {DEFAULT}{BLUE}<< END >>{DEFAULT}")
    return best_move
  


  def evaluate_move(self, board, player, move, opponent):

    move_value = 0
    r, c = move

    #move_value += 0.30 * count_capture(board, move, player)

    #memo: board.shape[0]=number of rows, board.shape[1]=number of columns

    corners = [(0, 0), (0, board.shape[1] - 1), (board.shape[0] - 1, 0), (board.shape[0] - 1, board.shape[1] - 1)]
    adjacent_to_corners = [(1, 1), (1, 0), (0, 1), (board.shape[0] - 2, 0), (board.shape[0] - 2, 1), (board.shape[0] - 1, 1), (0, board.shape[1] - 2), (1, board.shape[1] - 2), (1, board.shape[1] - 1), (board.shape[0] - 2, board.shape[1] - 1), (board.shape[0] - 2, board.shape[1] - 2), (board.shape[0] - 1, board.shape[1] - 2)]
    corner_gifters = [(1, 1), (1, board.shape[1] - 2), (board.shape[0] - 2, 1), (board.shape[0] - 2, board.shape[1] - 2)]
    step_to_corners = [(0, 2), (2, 0), (board.shape[0] - 3, 0), (board.shape[0] - 1, 2), (0, board.shape[1] - 3), (2, board.shape[1] - 1), (board.shape[0] - 1, board.shape[1] - 3), (board.shape[0] - 3, board.shape[1] - 1)]
    inner_corners = [(2,2), (2, board.shape[1] - 3), (board.shape[0] - 3, 2), (board.shape[0] - 3, board.shape[1] - 3)]

    if move in corners:
      move_value += 5000

    count = -1
    for adj in adjacent_to_corners:
      count += 1
      if move == adj:
        if (count in (0, 1, 2)) and (board[corners[0]]==player):
          move_value += 100
          break
        elif (count in (3, 4, 5)) and (board[corners[2]]==player):
          move_value += 100
          break
        elif (count in (6, 7, 8)) and (board[corners[1]]==player):
          move_value += 100
          break
        elif (count in (9, 10, 11)) and (board[corners[3]]==player):
          move_value += 100
          break
        else:
          move_value -= 30
          break

    count = -1
    for gifter in corner_gifters:
      count +=1
      if board[gifter] == opponent and (board[corners[count]] != opponent and board[corners[count]] != player):
        x, y = gifter

        if count == 3:

          i = 1
          while (x-i > 0):
            
            if board[x-i, y-i] != opponent:
              break
            if x-i == r and c<y-i:
              if count_capture_dir(board, move, player, (0,1)) >= (y-i)-c:
                move_value += 19
                break
              break
            if x-i == r and c>y-i:
              if count_capture_dir(board, move, player, (0,-1)) >= c-(y-i):
                move_value += 19
                break
              break
            if r<x-i and y-i == c:
              if count_capture_dir(board, move, player, (1,0)) >= (x-i)-r:
                move_value += 19
                break
              break
            if r>x-i and y-i == c:
              if count_capture_dir(board, move, player, (-1,0)) >= r-(x-i):
                move_value += 19
                break
              break
            i+=1
          break

        if count == 0:

          i = 1
          while (x+i < board.shape[0] - 1):

            if board[x+i, y+i] != opponent:
              break
            if x+i == r and c<y+i:
              if count_capture_dir(board, move, player, (0,1)) >= (y+i)-c:
                move_value += 19
                break
              break
            if x+i == r and c>y+i:
              if count_capture_dir(board, move, player, (0,-1)) >= c-(y+i):
                move_value += 19
                break
              break
            if r<x+i and y+i == c:
              if count_capture_dir(board, move, player, (1,0)) >= (x+i)-r:
                move_value += 19
                break
              break
            if r>x+i and y+i == c:
              if count_capture_dir(board, move, player, (-1,0)) >= r-(x+i):
                move_value += 19
                break
              break
            i+=1
          break

        if count == 1:

          i = 1
          while (x+i < board.shape[0] - 1):

            if board[x+i, y-i] != opponent:
              break
            if x+i == r and c<y-i:
              if count_capture_dir(board, move, player, (0,1)) >= (y-i)-c:
                move_value += 19
                break
              break
            if x+i == r and c>y-i:
              if count_capture_dir(board, move, player, (0,-1)) >= c-(y-i):
                move_value += 19
                break
              break
            if r<x+i and y-i == c:
              if count_capture_dir(board, move, player, (1,0)) >= (x+i)-r:
                move_value += 19
                break
              break
            if r>x+i and y-i == c:
              if count_capture_dir(board, move, player, (-1,0)) >= r-(x+i):
                move_value += 19
                break
              break
            i+=1
          break

        if count == 2:

          i = 1
          while (x-i >0):

            if board[x-i, y+i] != opponent:
              break
            if x-i == r and c<y+i:
              if count_capture_dir(board, move, player, (0,1)) >= (y+i)-c:
                move_value += 19
                break
              break
            if x-i == r and c>y+i:
              if count_capture_dir(board, move, player, (0,-1)) >= c-(y+i):
                move_value += 19
                break
              break
            if r<x-i and y+i == c:
              if count_capture_dir(board, move, player, (1,0)) >= (x-i)-r:
                move_value += 19
                break
              break
            if r>x-i and y+i == c:
              if count_capture_dir(board, move, player, (-1,0)) >= r-(x-i):
                move_value += 19
                break
              break
            i+=1
          break
        break

  
    
    if (1 <= r <= board.shape[0] - 2 and 1 <= c <= board.shape[1] - 2):

      if move in inner_corners:
        move_value += 1

      if (r == 2 and 2 <= c <= board.shape[1] - 3):
        move_value += 5
      elif (r == board.shape[0] - 3 and 2 <= c <= board.shape[1] - 3):
        move_value += 5
      elif (2 <= r <= board.shape[0] - 3 and c == 2):
        move_value += 5
      elif (2 <= r <= board.shape[0] - 3 and c == board.shape[1] - 3):
        move_value += 5
      
      elif (r == 1 and 1 <= c <= board.shape[1] - 2):
        move_value -= 3
      elif (r == board.shape[0] - 2 and 1 <= c <= board.shape[1] - 2):
        move_value -= 3
      elif (1 <= r <= board.shape[0] - 2 and c == 1):
        move_value -= 3
      elif (1 <= r <= board.shape[0] - 2 and c == board.shape[1] - 2):
        move_value -= 3
    
    else: #on a border

      if move in step_to_corners:
      # have to check whether or not placing here would give the opportunity for the opponent to take the corner

        if ((r == 0 and c == 2) or (r == 2 and c == 0)):
          if board[1,1] == opponent and (board[0,0] != player and board[0,0] != opponent):
            if ((board[0, 2] == player) or (board[2,0] == player)):
              move_value -= 15
          else:
            if ((board[0,0] == player and (move == (0,2) or move == (2,0))) or (board[corners[1]] == player and (move == step_to_corners[4] or move == step_to_corners[5])) or (board[corners[2]] == player and (move == step_to_corners[2] or move == step_to_corners[3])) or (board[corners[3]] == player and (move == step_to_corners[6] or move == step_to_corners[7]))):
              move_value -= 12
            else:
              move_value += 5
         
        elif ((r == 0 and c == board.shape[1] - 3) or (r == 2 and c == board.shape[1] - 1)):
          if board[1, board.shape[1] - 2] == opponent and (board[0, board.shape[1] - 1] != opponent and board[0, board.shape[1] - 1] != player):
            if ((board[0, board.shape[1] - 3] == player) or (board[2, board.shape[1] - 1] == player)):
              move_value -= 15
          else:
            if ((board[0,0] == player and (move == (0,2) or move == (2,0))) or (board[corners[1]] == player and (move == step_to_corners[4] or move == step_to_corners[5])) or (board[corners[2]] == player and (move == step_to_corners[2] or move == step_to_corners[3])) or (board[corners[3]] == player and (move == step_to_corners[6] or move == step_to_corners[7]))):
              move_value -= 12
            else:
              move_value += 5

        elif ((r == board.shape[1] - 3 and c == 0) or (r == board.shape[1] - 1 and c == 2)):
          if board[board.shape[1] - 2, 1] == opponent and (board[board.shape[0] - 1, 0] != player and board[board.shape[0] - 1, 0] != opponent):
            if ((board[board.shape[1] - 3, 0] == player) or (board[board.shape[1] - 1, 2] == player)):
              move_value -= 15
          else: 
            if ((board[0,0] == player and (move == (0,2) or move == (2,0))) or (board[corners[1]] == player and (move == step_to_corners[4] or move == step_to_corners[5])) or (board[corners[2]] == player and (move == step_to_corners[2] or move == step_to_corners[3])) or (board[corners[3]] == player and (move == step_to_corners[6] or move == step_to_corners[7]))):
              move_value -= 12
            else:
              move_value += 5

        else:
          if board[board.shape[0] - 2, board.shape[1] - 2] == opponent and (board[board.shape[0] - 1, board.shape[1] -1] != opponent and board[board.shape[0] - 1, board.shape[1] -1] != player):
            if ((board[board.shape[0] - 1, board.shape[1] - 3] == player) or (board[board.shape[0] - 3, board.shape[1] - 1] == player)):
              move_value -= 15
          else: 
            if ((board[0,0] == player and (move == (0,2) or move == (2,0))) or (board[corners[1]] == player and (move == step_to_corners[4] or move == step_to_corners[5])) or (board[corners[2]] == player and (move == step_to_corners[2] or move == step_to_corners[3])) or (board[corners[3]] == player and (move == step_to_corners[6] or move == step_to_corners[7]))):
              move_value -= 12
            else:
              move_value += 5


      if (r == 0 or r == board.shape[0] - 1):
        if c < board.shape[1]/2:
          if c%2 == 0:
            move_value+=1
        else:
          if c%2 == 1:
            move_value+=1

      if (c == 0 or c == board.shape[1] - 1):
        if r < board.shape[0]/2:
          if r%2 == 0:
            move_value+=1
        else:
          if r%2 == 1:
            move_value+=1


      if ((r == 0 or r == board.shape[0] - 1) and 1 <= c <= board.shape[1] - 2):

        if board[r, c-1] == opponent:
          i = 2
          while c-i >= 0:
            if board[r, c-i] == player:
              move_value += 32
              if (r,c) in adjacent_to_corners:
                move_value -= 32
                while c-i>=0:
                  if board[r, c-i] != player and board[r, c-i] != opponent:
                    break
                  if c-i == 0 and board[r, c-i] == player:
                    move_value += 32
                    break
                  i+=1
              break
            elif board[r, c-i] == opponent:
              i+=1
            else:
              move_value -= 11
              break

        if board[r, c+1] == opponent:
          i = 2
          while c+i <= board.shape[0] - 1:
            if board[r, c+i] == player:
              move_value += 32
              if (r,c) in adjacent_to_corners:
                move_value -= 32
                while c+i <= board.shape[0] - 1:
                  if board[r, c+i] != player and board[r, c+i] != opponent:
                    break
                  if c+i == board.shape[0] -1 and board[r, c+i] == player:
                    move_value += 32
                    break
                  i+=1
              break
            elif board[r, c+i] == opponent:
              i+=1
            else:
              move_value -= 11
              break

        if board[r, c-1] == player:
          i = 2
          while c-i >= 0:
            if board[r, c-i] == opponent:
              break
            if board[r, c-i] != player:
              move_value += 5
              break
            if c-i == 0:
              move_value += 31
            i+=1

        if board[r, c+1] == player:
          i = 2
          while c+i <= board.shape[1]-1:
            if board[r, c+i] == opponent:
              break
            if board[r, c+i] != player:
              move_value += 5
              break
            if c+i == board.shape[1]-1:
              move_value += 31
            i+=1

      
      if (1 <= r <= board.shape[0] - 2 and (c == 0 or c == board.shape[1] - 1)):

        if board[r-1, c] == opponent:
          i = 2
          while r-i >= 0:
            if board[r-i, c] == player:
              move_value += 32
              if (r,c) in adjacent_to_corners:
                move_value -= 32
                while r-i>=0:
                  if board[r-i, c] != player and board[r-i, c] != opponent:
                    break
                  if r-i == 0 and board[r-i, c] == player:
                    move_value += 32
                    break
                  i+=1
              break
            elif board[r-i, c] == opponent:
              i+=1
            else:
              move_value -= 11
              break

        if board[r+1, c] == opponent:
          i = 2
          while r+i <= board.shape[0] - 1:
            if board[r+i, c] == player:
              move_value += 32
              if (r,c) in adjacent_to_corners:
                move_value -= 32
                while r+i <= board.shape[0] - 1:
                  if board[r+i, c] != player and board[r+i, c] != opponent:
                    break
                  if r+i == board.shape[0] - 1 and board[r+i, c] == player:
                    move_value += 32
                    break
                  i+=1
              break
            elif board[r+i, c] == opponent:
              i+=1
            else:
              move_value -= 11
              break

        if board[r-1, c] == player:
          i = 2
          while r-i >= 0:
            if board[r-i, c] == opponent:
              break
            if board[r-i, c] != player:
              move_value += 5
              break
            if r-i == 0:
              move_value += 31
              break
            i+=1

        if board[r+1, c] == player:
          i = 2
          while r+i <= board.shape[0]-1:
            if board[r+i, c] == opponent:
              break
            if board[r+i, c] != player:
              move_value += 5
              break
            if r+i == board.shape[0]-1:
              move_value += 31
              break
            i+=1
              
      move_value += 7
    
    _, player_score, opponent_score = check_endgame(board, player, opponent)
    if board.shape[0] == 12 and player_score + opponent_score <= 10:
      move_value += count_capture(board, move, player)

    return move_value


  def evaluate_end_move(self, board, player, move, opponent):

    value = self.evaluate_move(board, player, move, opponent) + 5 * count_capture(board, move, player)

    return value

