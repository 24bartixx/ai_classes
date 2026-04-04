from engine import Game
from heuristics import HEURISTIC_NAMES


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
    search_depth = 3
    game = Game(initial_board, search_depth, HEURISTIC_NAMES['SIDES_PROXIMITY'], HEURISTIC_NAMES['SIDES_PROXIMITY'])
 
    print("\nInitial board:\n")
    game.display()
    
    # game.play(iterations=10, is_simulation=True, should_log=True)
    game.play(iterations=None, is_simulation=True, should_log=True)


if __name__ == "__main__":
	main()
