from engine import *
from algorithms import *
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
	search_depth = 3
	game = Game(initial_board, search_depth, HEURISTIC_NAMES['SIDES_PROXIMITY'], HEURISTIC_NAMES['SIDES_PROXIMITY'])
 
	print("\nInitial board:\n")
	game.display()

	print("\nLegal moves for W (White):")
	moves_w = get_legal_moves(game.board, 'W')
 
	for move in moves_w:
		print(f"From {move[0]} to {move[1]}")

	print("\nLegal moves for B (Black):")
	moves_b = get_legal_moves(game.board, 'B')
	for move in moves_b:
		print(f"From {move[0]} to {move[1]}")

	print("\n--- Making a few moves ---\n")
 
	for _ in range(10):
		next_white = get_best_move(game.board, game.search_depth, game.player_heuristic_mode, 'W')
		make_move(game.board, next_white)
	
		next_black = get_best_move(game.board, game.search_depth, game.opponent_heuristic_mode, 'B')
		make_move(game.board, next_black)

		game.display()
		print()
  
		score = evaluate_sides_proximity(game.board, 'W')
		print(f"Sides proximity: {score}")
  
		score = evaluate_mobility(game.board, 'W')
		print(f"Mobility: {score}")
  
		score = evaluate_line_completion(game.board, 'W')
		print(f"Line completion: {score}")

		print()
  
	# minimax_score = minmax(game.board, game.search_depth, True, game.heuristic_mode)
	# print(f"White minimax score: {minimax_score}")
 
	# minimax_score = minmax(game.board, game.search_depth, False, game.heuristic_mode)
	# print(f"Black minimax score: {minimax_score}")
 
	# next_white = get_best_move(game.board, game.search_depth, game.heuristic_mode, 'W')
	# print(f"White best move:\t{next_white[0]} ---> {next_white[1]}")
 
	# next_black = get_best_move(game.board, game.search_depth, game.heuristic_mode, 'B')
	# print(f"Black best move:\t{next_black[0]} ---> {next_black[1]}")
 
	print()

if __name__ == "__main__":
	main()
