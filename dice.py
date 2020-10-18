import random

DICE_MAX_SCORE = 6

class DiceGame:
    # Constructor
    # players: int: to store number of players
    # score_limit: int: required score for player to win the game
    # prev_roll_score: int list: player score in previous dice roll
    # turn skipped: list: if player's turn to be skipped this round.
    # player_scores: int list: sum  of player scores till this round.
    # rank_list: int list: contains players in order of their game completion time
    # current_player: int: current player elected for current dice roll move.
    # two_consecutive_roll: boolean: denotes if player scored 2 consecutive ones.
    def __init__(self, N, M):
        self.players = int(N)
        self.score_limit = int(M)
        self.prev_roll_score = [0] * (int(N)+1)
        self.turn_skipped = [False] * (int(N)+1)
        self.player_scores = [0] * (int(N)+1)
        self.rank_list = []
        self.current_player = 1
        self.two_consecutive_ones = False
    
    # Setter Method
    # sets current player
    def set_current_player(self, player):
        self.current_player = player
    
    # method to print game innstructions
    def display_instructions(self, startingPlayer):
        print(f"""
           - Every Player will get chance to roll a dice
           - Game will start from Player {startingPlayer} and continue in circle
           - For consecutive 6's, player will get to continue his turn
           - For each 2 consecutive 1's, player's turn will be skipped.
        """)
    
    # Game Init method
    def start_init(self):
        # set random player for first move.
        self.set_current_player(random.randint(0, self.players))
        self.display_instructions(self.current_player)
        self.start_game()

if __name__ == "__main__":
    # Getting user input
    while True:
        try:
            N = int(input("Enter number of players "))
            M = int(input("Enter points to accumulate "))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
            continue
        else:
            DiceGame(N,M).start_init()
            break