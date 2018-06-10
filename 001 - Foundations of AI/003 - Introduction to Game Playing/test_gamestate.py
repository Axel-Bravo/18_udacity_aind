import unittest
import gamestate


class TestGameState(unittest.TestCase):

    def test_initializer_default(self):
        board = [[0]*2 for _ in range(3)]
        board[2][1] = '/'
        game = gamestate.GameState()

        self.assertEqual(game._board, board)

    def test_forecast_move(self):
        game = gamestate.GameState()
        future_game_1 = game.forecast_move((0, 0))
        future_game_2 = future_game_1.forecast_move((1, 1))
        # Player 1 checks
        self.assertEqual(future_game_1._board[0][0], 1)
        self.assertEqual(future_game_1._initiative, 2)
        self.assertEqual(future_game_1._player_1_position, (0, 0))
        # Player 2 checks
        self.assertEqual(future_game_2._board[1][1], 2)
        self.assertEqual(future_game_2._initiative, 1)
        self.assertEqual(future_game_2._player_2_position, (1, 1))

    def test_player_current_position(self):
        game = gamestate.GameState()
        future_game_1 = game.forecast_move((0, 0))  # Player 1
        future_game_2 = future_game_1.forecast_move((1, 1))  # Player 2
        future_game_3 = future_game_2.forecast_move((0, 1))  # Player 1

        self.assertEqual(future_game_2.player_current_position(), (0, 0))  # Player_1: with initiative position
        self.assertEqual(future_game_3.player_current_position(), (1, 1))  # Player_2: with initiative position

    def test_in_game_board(self):
        game = gamestate.GameState()

        self.assertEqual(game.in_game_board((-1, 0)), False)
        self.assertEqual(game.in_game_board((0, -1)), False)
        self.assertEqual(game.in_game_board((3, 0)), False)
        self.assertEqual(game.in_game_board((0, 0)), True)
        self.assertEqual(game.in_game_board((0, 1)), True)
        self.assertEqual(game.in_game_board((2, 1)), True)

    def test_free_position(self):
        game = gamestate.GameState()
        future_game_1 = game.forecast_move((0, 0))  # Player 1

        self.assertEqual(game.free_position((0, 0)), True)
        self.assertEqual(game.free_position((2, 1)), False)
        self.assertEqual(future_game_1.free_position((0, 0)), False)
        self.assertEqual(future_game_1.free_position((1, 1)), True)

    def test_get_legal_moves(self):
        game_1 = gamestate.GameState()
        future_game_1_1 = game_1.forecast_move((0, 0))  # Player 1
        future_game_1_2 = future_game_1_1.forecast_move((1, 1))  # Player 2
        future_game_1_3 = future_game_1_2.forecast_move((0, 1))  # Player 1

        game_2 = gamestate.GameState()
        future_game_2_1 = game_2.forecast_move((1, 1))  # Player 1
        future_game_2_2 = future_game_2_1.forecast_move((0, 1))  # Player 2

        game_3 = gamestate.GameState()
        future_game_3_1 = game_3.forecast_move((1, 0))  # Player 1
        future_game_3_2 = future_game_3_1.forecast_move((0, 0))  # Player 2


        # Initial case:
        self.assertEqual(game_1.get_legal_moves(), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)])
        self.assertEqual(future_game_1_1.get_legal_moves(), [(0, 1), (1, 0), (1, 1), (2, 0)])

        # Other cases:
        self.assertEqual(future_game_1_2.get_legal_moves(), [(1, 0), (2, 0), (0, 1)])
        self.assertEqual(future_game_1_3.get_legal_moves(), [(1, 0), (2, 0)])

        self.assertEqual(future_game_2_2.get_legal_moves(), [(1, 0), (2, 0), (0, 0)])

        self.assertEqual(future_game_3_2.get_legal_moves(), [(2, 0), (1, 1), (0, 1)])


if __name__ == '__main__':
    unittest.main()
