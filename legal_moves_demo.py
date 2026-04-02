from engine import Game

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
	moves_w = game.get_legal_moves('W')
 
	for move in moves_w:
		print(f"From {move[0]} to {move[1]}")

	print("\nLegal moves for B (Black):")
	moves_b = game.get_legal_moves('B')
	for move in moves_b:
		print(f"From {move[0]} to {move[1]}")

	print("\n--- Making a few moves ---")
 
	moves_to_make = []
 
	for i in range(5):
		moves_w = game.get_legal_moves('W')
		game.make_move(moves_w[0])
	
		moves_w = game.get_legal_moves('B')
		game.make_move(moves_w[0])

		game.display()
		print()

if __name__ == "__main__":
	main()
