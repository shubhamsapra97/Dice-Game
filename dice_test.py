import pytest
from dice import DiceGame

class TestDiceGame:
    def test_game_starts_correctly(self, mocker):
        #Given
        game_obj = DiceGame(2,10)
        game_obj.set_current_player(1)
        mocker.patch.object(game_obj, 'set_current_player')
        mocker.patch.object(game_obj, 'display_instructions')
        mocker.patch.object(game_obj, 'start_game')
        
        #When
        game_obj.start_init()
        
        #Then
        game_obj.set_current_player.assert_called()
        game_obj.display_instructions.assert_called_with(game_obj.current_player)
        game_obj.start_game.assert_called()

    def test_set_next_player(self, mocker):
        #Given
        game_obj = DiceGame(2,10)
        game_obj.turn_skipped = ["False"] * int(3)
        mocker.patch.object(game_obj, 'set_current_player')
        game_obj.set_current_player.return_value = 1
        
        # When
        game_obj.set_next_player(1)
        
        #Then
        game_obj.set_current_player.assert_called_with(2)
    
    def test_set_next_player_edge_case(self, mocker):
        #Given
        game_obj = DiceGame(3,10)
        game_obj.turn_skipped = ["False"] * int(4)
        game_obj.turn_skipped[3] = "Completed"
        mocker.patch.object(game_obj, 'set_current_player')
        game_obj.set_current_player.return_value = 100
        
        # When
        game_obj.set_next_player(2)
        
        #Then
        game_obj.set_current_player.assert_called_with(1)

    def test_player_move_to_continue_on_consecutive_sixes(self, mocker):
        # Given
        game_obj = DiceGame(3,10)
        game_obj.set_current_player(1)
        game_obj.prev_roll_score = [0] * (int(6)+1)
        game_obj.prev_roll_score[1] = 6
        
        #When
        result = game_obj.decide_next_player(6)
        
        #Then
        assert result
    
    def test_player_move_to_be_skipped_on_consecutive_ones(self, mocker):
        # Given
        game_obj = DiceGame(2,10)
        game_obj.set_current_player(1)
        game_obj.prev_roll_score = [0] * (int(2)+1)
        game_obj.prev_roll_score[1] = 1
        game_obj.turn_skipped = [False] * (int(2)+1)
        
        #When
        result = game_obj.decide_next_player(1)
        
        #Then
        assert not result
    
    def test_game_to_end_if_completed_status_for_all_players(self, mocker):
        # Given
        game_obj = DiceGame(2,10)
        game_obj.turn_skipped = ["Completed"] * int(2)
        
        #When
        result = game_obj.has_game_ended()
        
        #Then
        assert result

    def test_game_to_not_end_if_not_completed_status_for_all_players(self, mocker):
        # Given
        game_obj = DiceGame(2,10)
        game_obj.turn_skipped = ["Completed"] * int(2)
        game_obj.turn_skipped[1] = False
        
        #When
        result = game_obj.has_game_ended()
        
        #Then
        assert not result

    def test_update_player_stats_completed_game(self, mocker):
        #Given
        game_obj = DiceGame(2,10)
        game_obj.player_scores = [8] * 3
        game_obj.set_current_player(1)
        game_obj.score_limit = 10
        game_obj.rank_list = []
        game_obj.turn_skipped = [False] * 3
        
        # When
        game_obj.update_player_stats(3)
        
        # Then
        assert game_obj.player_scores[game_obj.current_player] == 11
        assert game_obj.turn_skipped[game_obj.current_player] == "Completed"
        assert game_obj.rank_list.index(game_obj.current_player) == 0
    
    def test_update_player_stats_not_completed_game(self, mocker):
        #Given
        game_obj = DiceGame(2,10)
        game_obj.player_scores = [8] * 3
        game_obj.set_current_player(1)
        game_obj.score_limit = 10
        game_obj.rank_list = []
        game_obj.turn_skipped = [False] * 3
        
        # When
        game_obj.update_player_stats(1)
        
        # Then
        assert game_obj.player_scores[game_obj.current_player] == 9
        assert game_obj.turn_skipped[game_obj.current_player] == False
    
    def test_get_next_player_before_game_start_if_turn_skipped_true(self, mocker):
        #Given
        game_obj = DiceGame(2,10)
        game_obj.set_current_player(1)
        game_obj.turn_skipped = [False] * int(3)
        game_obj.turn_skipped[game_obj.current_player] = True
        mocker.patch.object(game_obj, 'set_next_player')
        
        # When
        game_obj.validate_player()
        
        #Then
        game_obj.set_next_player.assert_called_with(game_obj.current_player)
    
    def test_continue_with_player_before_game_start_if_turn_skipped_false(self, mocker):
        #Given
        game_obj = DiceGame(2,10)
        game_obj.set_current_player(1)
        game_obj.turn_skipped = [False] * int(3)
        mocker.patch.object(game_obj, 'set_next_player')
        
        # When
        game_obj.validate_player()
        
        #Then
        game_obj.set_next_player.assert_not_called()
