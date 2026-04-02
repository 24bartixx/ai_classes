from engine import *
from heuristics import *

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
	heuristic_mode = 1
	search_depth = 3
	game = Game(initial_board, heuristic_mode, search_depth)
	print("Initial board:")
	game.display()

	print("\nLegal moves for W (White):")
	moves_w = get_legal_moves(game, 'W')
 
	for move in moves_w:
		print(f"From {move[0]} to {move[1]}")

	print("\nLegal moves for B (Black):")
	moves_b = get_legal_moves(game, 'B')
	for move in moves_b:
		print(f"From {move[0]} to {move[1]}")

	print("\n--- Making a few moves ---")
 
	for _ in range(5):
		moves_w = get_legal_moves(game, 'W')
		make_move(game, moves_w[0])
	
		moves_b = get_legal_moves(game, 'B')
		make_move(game, moves_b[0])

		game.display()
		print()
  
		score = evaluate_sides_proximity(game, 'W')
		print(f"Sides proximity: {score}")
  
		score = evaluate_mobility(game, 'W')
		print(f"Mobility: {score}")

		print()

if __name__ == "__main__":
	main()
