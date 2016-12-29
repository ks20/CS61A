    """The Game of Hog."""
 
from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from math import sqrt
 
GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
 
 
 ######################
 # Phase 1: Simulator #
 ######################
 
def roll_dice(num_rolls, dice=six_sided):
     """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
     the outcomes unless any of the outcomes is 1. In that case, return 1.
     """
     # These assert statements ensure that num_rolls is a positive integer.
     assert type(num_rolls) == int, 'num_rolls must be an integer.'
     assert num_rolls > 0, 'Must roll at least once.'
 
     total = 0
     pig_out=False
     for i in range(num_rolls):
         m = dice()
         if m==1:
             pig_out = True          
         total = total + m 
     if pig_out:
         return 1
     return total
 
 
def free_bacon(opponent_score):
     """Return the points scored from rolling 0 dice (Free Bacon)."""
     return max(opponent_score%10,opponent_score//10)+1
 
def is_prime(x):
     if x==2:
         return True 
     if x<=1 or x%2==0:
         return False
     for i in range (3, int(sqrt(x))+1):
         if x%i==0:
             return False
     return True 
 
def next_prime(x):
     score  = x + 1
     while not (is_prime(score)):
         score +=1
     return score
 
def take_turn(num_rolls, opponent_score, dice=six_sided):
     """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
     Return the points scored for the turn by the current player.
 
     num_rolls:       The number of dice rolls that will be made.
     opponent_score:  The total score of the opponent.
     dice:            A function of no args that returns an integer outcome.
     """
     assert type(num_rolls) == int, 'num_rolls must be an integer.'
     assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
     assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
     assert opponent_score < 100, 'The game should be over.'
     sum_score = 0
     if num_rolls==0:
         sum_score = free_bacon(opponent_score)
     else:
         sum_score = roll_dice(num_rolls, dice)
     if is_prime(sum_score):
        sum_score = next_prime(sum_score)
     return sum_score
 
 
 
def select_dice(score, opponent_score):
     """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
     multiple of 7, in which case select four-sided dice (Hog Wild).
     """
     if (score+opponent_score) % 7 == 0:
         return four_sided
     else:
         return six_sided
 
def max_dice(score, opponent_score):
     """Return the maximum number of dice the current player can roll. The
     current player can roll at most 10 dice unless the sum of SCORE and
     OPPONENT_SCORE ends in a 7, in which case the player can roll at most 1.
     """
     if (score+opponent_score) % 10 == 7:
         return 1
     else:
         return 10
 
 
 
def is_swap(score):
     """Returns whether the SCORE contains only one unique digit, such as 22.
     """
     if score<10 or (score%10 == score//10):
         return True
     elif  score>100:
         if (score%10 == (score//10)%10 == score//100):
             return True
     return False
 
 
 
def other(player):
     """Return the other player, for a player PLAYER numbered 0 or 1.
 
     >>> other(0)
     1
     >>> other(1)
     0
     """
     return 1 - player
 
 
def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
     """Simulate a game and return the final scores of both players, with
     Player 0's score first, and Player 1's score second.
 
     A strategy is a function that takes two total scores as arguments
     (the current player's score, and the opponent's score), and returns a
     number of dice that the current player will roll this turn.
 
     strategy0:  The strategy function for Player 0, who plays first
     strategy1:  The strategy function for Player 1, who plays second
     score0   :  The starting score for Player 0
     score1   :  The starting score for Player 1
     """
     player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
     while score0<goal and score1<goal:
         if player==0:
             num_rolls = min(strategy0(score0, score1), max_dice(score0, score1))
             current = take_turn(num_rolls, score1, select_dice(score0, score1))
             score0 = score0 + current
             if is_swap(score0):
                 score0, score1 = score1, score0
         else:
             num_rolls = min(strategy1(score1, score0), max_dice(score0, score1))
             current1 = take_turn(num_rolls, score0, select_dice(score1, score0))
             score1 = current1 + score1
             if is_swap(score1):
                 score0, score1 = score1, score0
         player = other(player)
     return score0, score1
 
 #######################
 # Phase 2: Strategies #
 #######################
 
def always_roll(n):
     """Return a strategy that always rolls N dice.
 
     A strategy is a function that takes two total scores as arguments
     (the current player's score, and the opponent's score), and returns a
     number of dice that the current player will roll this turn.
 
     >>> strategy = always_roll(5)
     >>> strategy(0, 0)
     5
     >>> strategy(99, 99)
     5
     """
     @check_strategy
     def strategy(score, opponent_score):
         return n
 
     return strategy
 
def check_strategy_roll(score, opponent_score, num_rolls):
     """Raises an error with a helpful message if NUM_ROLLS is an invalid strategy
     output. All strategy outputs must be non-negative integers less than or
     equal to 10.
 
     >>> check_strategy_roll(10, 20, num_rolls=100)
     Traceback (most recent call last):
      ...
     AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)
 
     >>> check_strategy_roll(20, 10, num_rolls=0.1)
     Traceback (most recent call last):
      ...
     AssertionError: strategy(20, 10) returned 0.1 (not an integer)
 
     >>> check_strategy_roll(0, 0, num_rolls=None)
     Traceback (most recent call last):
      ...
     AssertionError: strategy(0, 0) returned None (not an integer)
     """
     msg = 'strategy({}, {}) returned {}'.format(
         score, opponent_score, num_rolls)
     assert type(num_rolls) == int, msg + ' (not an integer)'
     assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'

def check_strategy(strategy, goal=GOAL_SCORE):
     """Checks the strategy with all valid inputs and verifies that the 
     strategy returns a valid input. Use `check_strategy_roll` to raise 
     an error with a helpful message if the strategy retuns an invalid 
     output.
 
     >>> always_roll_5 = always_roll(5)
     >>> always_roll_5 == check_strategy(always_roll_5)
     True
     >>> def fail_15_20(score, opponent_score):
     ...     if score != 15 or opponent_score != 20:
     ...         return 5
     ...
     >>> fail_15_20 == check_strategy(fail_15_20)
     Traceback (most recent call last):
      ...
     AssertionError: strategy(15, 20) returned None (invalid number of rolls)
     >>> def fail_102_115(score, opponent_score):
     ...     if score == 102 and opponent_score == 115:
     ...         return 100
     ...     return 5
     ...
     >>> fail_102_115 == check_strategy(fail_102_115)
     True
     >>> fail_102_115 == check_strategy(fail_102_115, 120)
     Traceback (most recent call last):
      ...
     AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
     """
     #score = 0 
     #opponent_score = 0
     #play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE)
 
     for item in range(0, goal):
         for item2 in range(0, goal):
             check_strategy_roll(item, item2, strategy(item, item2))
     return strategy
 
 
def make_averaged(fn, num_samples=1000):
     """Return a function that returns the average_value of FN when called.
 
     To implement this function, you will have to use *args syntax, a new Python
     feature introduced in this project.  See the project description.
 
     >>> dice = make_test_dice(3, 1, 5, 6)
     >>> averaged_dice = make_averaged(dice, 1000)
     >>> averaged_dice()
     3.75
     """
     def average_out(*args): 
         i=1
         total = 0
         while i<=num_samples:
             total+= fn(*args)
             i+=1
         return total/num_samples
     return average_out 
 
 
def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
     """Return the number of dice (1 to 10) that gives the highest average turn
     score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
     Assume that the dice always return positive outcomes.
 
     >>> dice = make_test_dice(3)
     >>> max_scoring_num_rolls(dice)
     10
     """
     average = 0
     num = 1 
     highest = 0
     while num<=10:
         averaged_roll_dice = make_averaged(roll_dice, 1000)
         i = averaged_roll_dice(num, dice)
         if i > average:
             average = i 
             highest = num
             num+=1
         else:
             num+=1
     return highest

 
def winner(strategy0, strategy1):
     """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
     score0, score1 = play(strategy0, strategy1)
     if score0 > score1:
         return 0
     else:
         return 1
 
def average_win_rate(strategy, baseline=always_roll(6)):
     """Return the average win rate of STRATEGY against BASELINE. Averages the
     winrate when starting the game as player 0 and as player 1.
     """
     win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
     win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
 
     return (win_rate_as_player_0 + win_rate_as_player_1) / 2
 
def run_experiments():
     """Run a series of strategy experiments and report results."""
     if True:  # Change to False when done finding max_scoring_num_rolls
         six_sided_max = max_scoring_num_rolls(six_sided)
         print('Max scoring num rolls for six-sided dice:', six_sided_max)
         four_sided_max = max_scoring_num_rolls(four_sided)
         print('Max scoring num rolls for four-sided dice:', four_sided_max)
 
     if False:  # Change to True to test always_roll(8)
         print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
 
     if False:  # Change to True to test bacon_strategy
         print('bacon_strategy win rate:', average_win_rate(bacon_strategy))
 
     if False:  # Change to True to test swap_strategy
         print('swap_strategy win rate:', average_win_rate(swap_strategy))
 
     "*** You may add additional experiments as you wish ***"
 
 
 # Strategies
 
@check_strategy
def bacon_strategy(score, opponent_score, margin=8, num_rolls=6):
     """This strategy rolls 0 dice if that gives at least MARGIN points,
     and rolls NUM_ROLLS otherwise.
     """
     score = free_bacon(opponent_score)
     if is_prime(score):
         score = next_prime(score)
     if score >= margin:
         return 0 
     else:
         return num_rolls
 
 
@check_strategy
def swap_strategy(score, opponent_score, margin=5, num_rolls=6):
     """This strategy rolls 0 dice when it triggers a beneficial swap. It also
     rolls 0 dice if it gives at least MARGIN points and doesn't trigger a
     swap. Otherwise, it rolls NUM_ROLLS.
     """
     i = free_bacon(opponent_score)
     if is_prime(i):
         i = next_prime(i)
     new_score = score + i
     boolean = is_swap(new_score)
     if boolean and new_score>opponent_score:
         return num_rolls
     if boolean and new_score<opponent_score:
         return 0
     elif (not boolean) and bacon_strategy(score, opponent_score, margin, num_rolls)==0:
         return 0
     else:
         return num_rolls
 
@check_strategy
def prime_strategy(score, opponent_score, margin=8, num_rolls=5):
 
     while is_prime(score + opponent_score + max(opponent_score//10, opponent_score%10) + 1):
         if opponent_score < score + max(opponent_score // 10, opponent_score % 10) + 1:
             return 0
         elif opponent_score > score + max(opponent_score // 10, opponent_score % 10) + 1:
             return num_rolls
         else:
             return bacon_strategy(score, opponent_score, margin, num_rolls)
     else:
         return bacon_strategy(score, opponent_score, margin, num_rolls)
 
 
@check_strategy
def final_strategy(score, opponent_score):
     if score<=67:
         if score<opponent_score-5:
             return swap_strategy(score, opponent_score, 12, 10)
         else: 
             return swap_strategy(score, opponent_score, 8, 8)

     elif max_dice(score, opponent_score) == 1: #Hog Tied
        if select_dice(score, opponent_score): #Hog Wild
            return swap_strategy(score, opponent_score, 4, 3)

     elif score>67:
         if score>80:
            return swap_strategy(score, opponent_score, 2, 3)
         return swap_strategy(score, opponent_score, 6, 5)

     if is_prime(score + 3) == True:
        return prime_strategy(score, opponent_score, 2, 10)

 
 
 ##########################
 # Command Line Interface #
 ##########################
 
 
 # Note: Functions in this section do not need to be changed. They use features
 #       of Python not yet covered in the course.
 
 
@main
def run(*args):
     """Read in the command-line argument and calls corresponding functions.
 
     This function uses Python syntax/techniques not yet covered in this course.
     """
     import argparse
     parser = argparse.ArgumentParser(description="Play Hog")
     parser.add_argument('--run_experiments', '-r', action='store_true',
                         help='Runs strategy experiments')
 
     args = parser.parse_args()
 
     if args.run_experiments:
         run_experiments()