from random import shuffle, choice
from copy import copy
from time import time

DIMENSIONS = 4
CUSTOM_BOARD = [1, 6, 3, 5, 8, 7, 2, 4, 9, 11, 10, 14, 15, 12, 11]
MAX_DEPTH = 200

class Node(object):
	global DIMENSIONS
	
	def __init__(self, parent, board, empty_pos):
		self.parent = parent
		self.board = board
		self.empty_pos = empty_pos
		self.heuristic = self.calculate_heuristic()
		self.possible_moves = self.calculate_possible_moves()
		
	def calculate_heuristic(self):
		heuristic = 0
		for dim, val in self.board.items():
			if val is None: continue
			y = int((val-1)/DIMENSIONS)
			x = (val-1)%DIMENSIONS
			h = abs(x - dim[0]) + abs(y - dim[1])
			heuristic += h
		return heuristic
	
	def calculate_possible_moves(self):
		p = self.empty_pos
		possible_moves = list()
		for pm in [(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)]:
			if pm[0] >= DIMENSIONS or pm[0] < 0 or pm[1] >= DIMENSIONS or pm[1] < 0: continue
			if self.parent is not None and self.parent.empty_pos == pm: continue
			possible_moves.append(pm)
		return possible_moves
	
	def get_children(self):
		children = list()
		for move in self.possible_moves:
			try:
				new_board = copy(self.board)
				new_board[self.empty_pos], new_board[move] = self.board[move], None
				children.append(Node(self, new_board, move))
			except KeyError: pass
		return children
	
	def __list__(self):
		n = len(str(DIMENSIONS**2-1))
		result = []
		for y in range(DIMENSIONS):
			for x in range(DIMENSIONS):
				result.append(str(self.board[x,y]).replace("None", "0").ljust(n))		
		return result



###################################################################################
#khoitao-input
def create_board(board=None):
	global DIMENSIONS
	solvable = lambda b: sum([sum([1 for i in range(n+1, len(b)) if b[n] > b[i]]) for n in range(0, len(b)-1)]) % 2 == 0
	if board is None:
		board = [i for i in range(1, DIMENSIONS**2)]
		shuffle(board)
		while not solvable(board): shuffle(board)
	else:
		if not solvable(board): return None
	board.append(None)
	return {(column, row): board.pop(0) for row in range(DIMENSIONS) for column in range(DIMENSIONS) if board}

def get_solution(node):
	solution = list()
	while node is not None:
		solution.append(node)
		node = node.parent
	solution.reverse()
	return solution

def search(node, g, bound):
	f = node.heuristic + g
	if f > bound or node.heuristic == 0: return node,f
	min_f = 9999
	for n in node.get_children():
		nn,t = search(n, g + 1, bound)
		if nn.heuristic == 0: return nn,t
		if t < min_f: min_f = t
	return node,min_f

def solve(board, bound):
	global MAX_DEPTH
	if bound > MAX_DEPTH: return None, None # Unsolvable
	n,t = search(root, 0, bound)
	if n.heuristic == 0: return n,t
	return solve(board, t)

if __name__ == "__main__":
	board = create_board(CUSTOM_BOARD)
	root = Node(None, board, (DIMENSIONS-1, DIMENSIONS-1))
	print("Board:")
	for row in root.__list__():
		print(row)
	start_time = time()
	end_node, moves = solve(root, root.heuristic)
	end_time = time() - start_time
	if end_node is None:
		print("Unsolvable")
	else:
		print("\nSolution (%d moves):" % moves)
		result=[]
		for node in get_solution(end_node):		
			result.append(node.__list__())
		print(result)
		print("\nSolved in %.4f seconds" % end_time)