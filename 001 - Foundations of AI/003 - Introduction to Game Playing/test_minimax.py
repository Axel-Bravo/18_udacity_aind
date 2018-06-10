import unittest
import gamestate
import minimax


class TestMinimax(unittest.TestCase):

    def test_minimax_decision(self):
        game = gamestate.GameState()
        self.assertIn(minimax.minimax_decision(game), [(0, 1), (2, 0), (0, 0)])


if __name__ == '__main__':
    unittest.main()
