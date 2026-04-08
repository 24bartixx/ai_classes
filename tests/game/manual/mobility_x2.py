from engine import Game
from heuristics import HEURISTIC_NAMES

SEARCH_DEPTH = 5

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
    game = Game(initial_board, SEARCH_DEPTH, HEURISTIC_NAMES['MOBILITY'], HEURISTIC_NAMES['MOBILITY'])
    print("\nInitial board:\n")
    game.display()
    game.play(iterations=None, is_simulation=False, should_log=True)

if __name__ == "__main__":
	main()
