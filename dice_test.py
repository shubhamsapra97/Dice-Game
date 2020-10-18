import pytest
from dice import DiceGame

class TestNamesCase:
    def test_game_starts_correctly(self, mocker):
        #Given
        DiceGame.players = 2
        DiceGame.current_player = 1
        mocker.patch.object(DiceGame, 'set_current_player')
        mocker.patch.object(DiceGame, 'display_instructions')
        mocker.patch.object(DiceGame, 'start_game')
        
        #When
        DiceGame.start_init(DiceGame)
        
        #Then
        DiceGame.set_current_player.assert_called()
        DiceGame.display_instructions.assert_called_with(DiceGame.current_player)
        DiceGame.start_game.assert_called()

    def test_set_next_player(self, mocker):
        #Given
        DiceGame.players = 2
        DiceGame.turn_skipped = ["False"] * int(3)
        mocker.patch.object(DiceGame, 'set_current_player')
        DiceGame.set_current_player.return_value = 1
        
        # When
        DiceGame.set_next_player(DiceGame, 1)
        
        #Then
        DiceGame.set_current_player.assert_called_with(2)
    
    def test_set_next_player_edge_case(self, mocker):
        #Given
        DiceGame.players = 3
        DiceGame.turn_skipped = ["False"] * int(4)
        DiceGame.turn_skipped[3] = "Completed"
        mocker.patch.object(DiceGame, 'set_current_player')
        DiceGame.set_current_player.return_value = 100
        
        # When
        DiceGame.set_next_player(DiceGame, 2)
        
        #Then
        DiceGame.set_current_player.assert_called_with(1)

    def test_player_move_to_continue_on_consecutive_sixes(self, mocker):
        # Given
        DiceGame.current_player = 1
        DiceGame.prev_roll_score = [0] * (int(6)+1)
        DiceGame.prev_roll_score[1] = 6
        
        #When
        result = DiceGame.decide_next_player(DiceGame, 6)
        
        #Then
        assert result
    
    def test_player_move_to_be_skipped_on_consecutive_ones(self, mocker):
        # Given
        DiceGame.current_player = 1
        DiceGame.prev_roll_score = [0] * (int(2)+1)
        DiceGame.prev_roll_score[1] = 1
        DiceGame.turn_skipped = [False] * (int(2)+1)
        
        #When
        result = DiceGame.decide_next_player(DiceGame, 1)
        
        #Then
        assert not result
    
    def test_game_to_end_if_completed_status_for_all_players(self, mocker):
        # Given
        DiceGame.players = 2
        DiceGame.turn_skipped = ["Completed"] * int(2)
        
        #When
        result = DiceGame.has_game_ended(DiceGame)
        
        #Then
        assert result

    def test_game_to_not_end_if_not_completed_status_for_all_players(self, mocker):
        # Given
        DiceGame.players = 2
        DiceGame.turn_skipped = ["Completed"] * int(2)
        DiceGame.turn_skipped[1] = False
        
        #When
        result = DiceGame.has_game_ended(DiceGame)
        
        #Then
        assert not result

    def test_update_player_stats_completed_game(self, mocker):
        #Given
        DiceGame.player_scores = [8] * 3
        DiceGame.current_player = 1
        DiceGame.score_limit = 10
        DiceGame.rank_list = []
        DiceGame.turn_skipped = [False] * 3
        
        # When
        DiceGame.update_player_stats(DiceGame, 3)
        
        # Then
        assert DiceGame.player_scores[DiceGame.current_player] == 11
        assert DiceGame.turn_skipped[DiceGame.current_player] == "Completed"
        assert DiceGame.rank_list.index(DiceGame.current_player) == 0
    
    def test_update_player_stats_not_completed_game(self, mocker):
        #Given
        DiceGame.player_scores = [8] * 3
        DiceGame.current_player = 1
        DiceGame.score_limit = 10
        DiceGame.rank_list = []
        DiceGame.turn_skipped = [False] * 3
        
        # When
        DiceGame.update_player_stats(DiceGame, 1)
        
        # Then
        assert DiceGame.player_scores[DiceGame.current_player] == 9
        assert DiceGame.turn_skipped[DiceGame.current_player] == False
    
    def test_get_next_player_before_game_start_if_turn_skipped_true(self, mocker):
        #Given
        DiceGame.players = 2
        DiceGame.current_player = 1
        DiceGame.turn_skipped = [False] * int(3)
        DiceGame.turn_skipped[DiceGame.current_player] = True
        mocker.patch.object(DiceGame, 'set_next_player')
        DiceGame.set_current_player.return_value = 1
        
        # When
        DiceGame.validate_player(DiceGame)
        
        #Then
        DiceGame.set_next_player.assert_called_with(DiceGame.current_player)
    
    def test_continue_with_player_before_game_start_if_turn_skipped_false(self, mocker):
        #Given
        DiceGame.players = 2
        DiceGame.current_player = 1
        DiceGame.turn_skipped = [False] * int(3)
        mocker.patch.object(DiceGame, 'set_next_player')
        
        # When
        DiceGame.validate_player(DiceGame)
        
        #Then
        DiceGame.set_next_player.assert_not_called()
