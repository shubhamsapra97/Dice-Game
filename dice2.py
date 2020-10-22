import random

DICE_MAX_SCORE = 6

class DiceGame:
    def __init__(self, N, M):
        self.players = N
        self.score_limit = M
        self.player_array = list(range(0,int(N)))
        self.player_data = {}
        self.current_player = 1
        self.rank_list = []
        self.two_consecutive_ones = False
    
    # method to print game instructions
    def display_instructions(self, startingPlayer):
        print(f"""
           - Every Player will get chance to roll a dice
           - Game will start from Player {startingPlayer} and continue in circle
           - For consecutive 6's, player will get to continue his turn
           - For each 2 consecutive 1's, player's turn will be skipped.
        """)
    
    def set_current_player(self, player):
        self.current_player = player
    
    # method to set the player for next move
    def set_next_player(self, player):
        next_user = player+1
        counter = 1
        while True:
            # skip next player if he has already completed the game
            # counter to prevent infinte loop in case all players have completed the game
            next_user = next_user if next_user < self.players else 0
            if counter <= self.players:
                if self.player_data[self.player_array[next_user]]["turn_skipped"]:

                    print(f"""Skipping player {self.player_array[next_user]} \n""")

                    if self.player_data[self.player_array[next_user]]["turn_skipped"] != "Completed":
                        self.player_data[self.player_array[next_user]]["turn_skipped"] = False

                    next_user += 1
                    counter += 1
                    continue
            
            self.set_current_player(next_user)
            break
    
    # method to return player for next move
    # returns True if current player can continue
    # returns False if next player gets the move
    def decide_next_player(self, score):
        # move to next player if it's player's first move or if counter is reset
        # (in case of consecutive 1's).
        if self.player_data[self.player_array[self.current_player]]["prev_score"]:
            
            # return True if consecutive 6's
            if score == 6:
                print("Jackpot!!")
                return True

            # in case of consecutive 1's
            # skip player's move in next round
            if score == 1 and self.player_data[self.player_array[self.current_player]]["prev_score"] == 1:
                self.player_data[self.player_array[self.current_player]]["turn_skipped"] = True
                self.two_consecutive_ones = True
        return False
    
    def setup_player_data(self):
        random.shuffle(self.player_array)
        for player_index in range(0, int(self.players)):
            self.player_data[player_index] = {
                "prev_score": -1,
                "turn_skipped": False,
                "score": 0,
            }
    
    # method to print stat of current player
    def display_stats(self):
        print(" ============================== ")
        print("Player:     Score:     Rank:\n")
        for player_index in range(self.players):
            player_status = "X" if player_index not in self.rank_list else self.rank_list.index(player_index) + 1
            print(f"|  Player {player_index}     {self.player_data[player_index]['score']}        {player_status}   |\n")
        print(" ============================== \n")
    
    # method to update stats of player after dice roll
    def update_player_stats(self, score):
        self.player_data[self.player_array[self.current_player]]["score"] += score

        # if player has achieved required score
        # add the player to rank list
        # set turn_skipped for the player to be "Completed", to ignore player in next rounds.
        if self.player_data[self.player_array[self.current_player]]["score"] >= self.score_limit:
            self.rank_list.append(self.player_array[self.current_player])
            self.player_data[self.player_array[self.current_player]]["turn_skipped"] = "Completed"
    
    # check if player's turn is to be skipped
    # in case of consecutive 1's or if player has completed the game
    def validate_player(self):
        if self.player_data[self.player_array[self.current_player]]["turn_skipped"]:
            
            # if player has not completed the game
            # reset the player skip for next rounds
            if self.player_data[self.player_array[self.current_player]]["turn_skipped"] != "Completed":
                self.player_data[self.player_array[self.current_player]]["turn_skipped"] = False
                print(f"Skipping Player {self.player_array[self.current_player]} turn because of 2 consecutive 1's\n")
            
            # set next player for this move
            self.set_next_player(self.current_player)
            
    # method to check if game has ended
    def has_game_ended(self):
        # find all players in turn_skipped list with "Completed" value
        game_ended = True
        for x in range(self.players):
            if self.player_data[x]["turn_skipped"] != "Completed":
                game_ended = False
        
        return game_ended
    
    # method that contains the main logic of the Game
    def start_game(self):
        
        # run loop until all players have finished Game
        while not self.has_game_ended():
            
            # before rolling the dice
            # validate current player, check if he needs to be skipped
            self.validate_player()

            print(f"Player {self.player_array[self.current_player]} to roll the dice")
            
            # user confirmation to roll dice
            while True:
                user_input = input("Press 'r' to roll ")
                if user_input != "r":
                    continue
                break
            
            # get random score for current dice roll
            roll_score = random.randint(1, DICE_MAX_SCORE)
            print(f"Player {self.player_array[self.current_player]} got {roll_score}\n")
            
            # update the stats of the player
            self.update_player_stats(roll_score)
            
            # display the stats in terminal
            self.display_stats()
            
            # if player has completed the game
            # after updating player stats
            if self.player_data[self.player_array[self.current_player]]["turn_skipped"]:
                self.player_data[self.player_array[self.current_player]]["prev_score"] = roll_score
                self.set_next_player(self.current_player)
            
            # decide whether to get next player for the next move
            elif not self.decide_next_player(roll_score):
                # check if player got 2 consecutive 1's
                # if yes, reset the prev_roll_score of player for this move.
                if not self.two_consecutive_ones:
                    self.player_data[self.player_array[self.current_player]]["prev_score"] = roll_score
                else:
                    self.player_data[self.player_array[self.current_player]]["prev_score"] = 0
                self.set_next_player(self.current_player)
            
            # if player scores consectutive 6's
            # just update the prev score of the player
            # and let him continue with next move
            else:
                self.player_data[self.player_array[self.current_player]]["prev_score"] = roll_score
            
            # resetting the value for this flag
            self.two_consecutive_ones = False
        
        print("Game Ended!")
        print("Final Ranks: \n")
        self.display_stats()

    # Game Init method
    def start_init(self):
        self.setup_player_data()
        print(self.player_array)
        self.set_current_player(random.randint(0, self.players-1))
        self.display_instructions(self.player_array[self.current_player])
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