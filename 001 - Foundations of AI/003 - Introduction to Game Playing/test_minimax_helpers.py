import unittest
import gamestate
import minimax_helpers as mmh


class TestMinimaxHelpers(unittest.TestCase):

    def test_terminal_test(self):
        # Case Player 1 game is not over works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        self.assertEqual(mmh.terminal_test(game), False)

        # Case Player 1 game is over (works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game._board = [[2, 0], [1, 2], [1, '/']]
        game._player_1_position = (2, 0)
        game._player_2_position = (1, 1)
        self.assertEqual(mmh.terminal_test(game), True)

        # Case Player 2 game is not over works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game_future = game.forecast_move((0, 0))
        self.assertEqual(mmh.terminal_test(game_future), False)

        # Case Player 2 game is over (works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game._board = [[1, 2], [1, 2], [2, '/']]
        game._player_1_position = (2, 0)
        game._player_2_position = (0, 1)
        game._initiative = 2
        self.assertEqual(mmh.terminal_test(game), True)

    def test_min_value(self):
        # Case Player 2 (min_game is over (works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game._board = [[1, 2], [1, 2], [2, '/']]
        game._player_1_position = (2, 0)
        game._player_2_position = (0, 1)
        game._initiative = 2
        self.assertEqual(mmh.min_value(game), 1)

        # Case Player 2 (min_value) game is not over (works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game._board = [[1, 0], [2, 0], [0, '/']]
        game._player_1_position = (0, 0)
        game._player_2_position = (1, 0)
        self.assertEqual(mmh.min_value(game), -1)

    def test_max_value(self):
        # Case Player 1 (max_value) game is over (works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game._board = [[2, 0], [1, 2], [1, '/']]
        game._player_1_position = (2, 0)
        game._player_2_position = (1, 1)
        self.assertEqual(mmh.max_value(game), -1)

        # Case Player 1 (max_value) game is not over (works for dim_x = 3 , dim_y = 2)
        game = gamestate.GameState()
        game._board = [[0, 0], [1, 0], [2, '/']]
        game._player_1_position = (1, 0)
        game._player_2_position = (2, 0)
        self.assertEqual(mmh.max_value(game), 1)


if __name__ == '__main__':
    unittest.main()
