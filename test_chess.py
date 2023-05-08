import pytest
from unittest.mock import Mock, patch
from chess_engine import game_state
from enums import Player
from Piece import Knight, Bishop
import ai_engine


class TestChess:
    @pytest.fixture
    def game(self):
        return game_state()

    @pytest.fixture
    def board_empty(self):
        game = game_state()
        empty_row = [Player.EMPTY] * 8
        game.board = [empty_row[:] for _ in range(8)]
        return game

    #Unit - test
    def test1_get_valid_peaceful_moves(self, game):
        knight = Knight('n', 3, 4, Player.PLAYER_1)
        with patch.object(game, 'get_piece', return_value=Player.EMPTY):
            knight_moves = knight.get_valid_peaceful_moves(game)
            knight_moves_exccept = [(1, 3), (2, 2), (4, 2), (5, 3), (5, 5), (4, 6), (2, 6), (1, 5)]
            assert set(knight_moves) == set(knight_moves_exccept)

    def test2_knight_get_valid_peaceful_moves(self, game):
        knight = Knight('n', 0, 0, Player.PLAYER_1)

        def mock_get_piece(r, c):
            if (r, c) != (0, 0) and (0 <= r < 8) and (0 <= c < 8):
                return Player.EMPTY
            else:
                return None

        game.get_piece = Mock(side_effect=mock_get_piece)
        knight_moves = knight.get_valid_peaceful_moves(game)
        knight_moves_exccept = [(1, 2), (2, 1)]
        assert set(knight_moves) == set(knight_moves_exccept)

    def test3_knight_get_valid_peaceful_moves(self, game):
        knight = Knight('n', 7, 3, Player.PLAYER_1)

        def mock_get_piece(r, c):
            if (r, c) != (7, 3) and (0 <= r < 8) and (0 <= c < 8):
                return Player.EMPTY
            else:
                return None
        game.get_piece = Mock(side_effect=mock_get_piece)
        knight_moves = knight.get_valid_peaceful_moves(game)
        knight_moves_exccept = [(6, 1), (6, 5), (5, 4), (5, 2)]
        assert set(knight_moves) == set(knight_moves_exccept)

    def test1_get_valid_piece_takes(self, game):
        knight = Knight('n', 4, 4, Player.PLAYER_1)
        knight_moves = knight.get_valid_piece_takes(game)
        knight_moves_exccept = [(6, 3), (6, 5)]
        assert set(knight_moves) == set(knight_moves_exccept)

    def test2_get_valid_piece_takes(self, game):
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        knight_moves = knight.get_valid_piece_takes(game)
        knight_moves_exccept = []
        assert set(knight_moves) == set(knight_moves_exccept)

    def test3_knight_get_valid_piece_takes(self, board_empty):
        board_empty.board[2][1] = Knight('n', 2, 1, Player.PLAYER_2)
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        board_empty.board[0][0] = knight
        moves = knight.get_valid_piece_takes(board_empty)
        expected_moves = [(2, 1)]
        assert set(moves) == set(expected_moves)

    #integration-test
    def test_evaluate_board(self, board_empty):
        board_empty.board[3][4] = Knight('n', 3, 4, Player.PLAYER_1)
        board_empty.board[2][5] = Bishop('b', 2, 5, Player.PLAYER_2)
        chess_ai = ai_engine.chess_ai()

        score = chess_ai.evaluate_board(board_empty, Player.PLAYER_1)

        assert score == 0

    def test_get_valid_moves(self, game):
        game.board[3][4] = Knight('n', 3, 4, Player.PLAYER_1)
        with patch.object(Knight, 'get_valid_piece_takes') as mock_takes, \
                patch.object(Knight, 'get_valid_peaceful_moves') as mock_moves:
            mock_takes.return_value = [(2, 2), (4, 2)]
            mock_moves.return_value = [(1, 3), (2, 6)]
            valid_moves = game.get_valid_moves((3, 4))
            expected_moves = [(2, 2), (4, 2), (1, 3), (2, 6)]
            assert set(valid_moves) == set(expected_moves)

    #System_test
    def test_chekmate(self, game):
        game.move_piece((1, 2), (2, 2), False)
        game.move_piece((6, 3), (5, 3), False)
        game.move_piece((1, 1), (3, 1), False)
        game.move_piece((7, 4), (3, 0), False)
        res = game.checkmate_stalemate_checker()
        assert res == 0

