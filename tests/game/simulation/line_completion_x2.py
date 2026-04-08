from engine import Game
from heuristics import HEURISTIC_NAMES

SEARCH_DEPTH = 4

def main():
    initial_board = '''
	B B B B B B B B
	B B B B B B B B
	_ _ _ _ _ _ _ _
	_ _ _ _ _ _ _ _
	_ _ _ _ _ _ _ _
	_ _ _ _ _ _ _ _
	W W W W W W W W
	W W W W W W W W
	'''
    game = Game(initial_board, SEARCH_DEPTH, HEURISTIC_NAMES['LINE_COMPLETION'], HEURISTIC_NAMES['LINE_COMPLETION'])
    print("\nInitial board:\n")
    game.display()
    game.play(iterations=None, is_simulation=True, should_log=True)

if __name__ == "__main__":
	main()
