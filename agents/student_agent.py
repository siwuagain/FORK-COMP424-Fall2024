# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
from helpers import random_move, count_capture, execute_move, check_endgame, get_valid_moves
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

    
    move = random_move(chess_board, player)

    logger.debug("MOVE: " + str(move))
    logger.info(f"STUDENT AGENT STEP {DEFAULT}{BLUE}<< END >>{DEFAULT}")
    return move
