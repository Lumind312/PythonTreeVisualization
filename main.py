from graphviz import Digraph
from queue import Queue

def printTree(root, formulas):
	# https://treelib.readthedocs.io/en/latest/
	tree = Digraph()

	seen = [root]
	tree.node(root, root, shape='star')

	q = Queue()
	q.put(root)
	next_group = Queue()		# needed for subgraph

	while not q.empty():
		curr = q.get()
		if curr == 'Cats' or curr == 'Dogs':	# any cat/dog applies, so there's no df row for it
			continue
		child = (formulas.loc[curr]).to_list()
		# print(child)
		# print(curr)
		for i in child:
			if i == 'Hippo':
				i = 'Hippopotamus'				# it was sometimes shortened, sometimes not
			if i not in seen and i not in tree.body:
				seen.append(i)
				next_group.put(i)
				tree.node(i, i)
			tree.edge(i, curr)					# duplicate lines are ok
			# print(tree)
		
		if q.empty():							# when we use up our main queue, pull from the next group
			# cannot clone a queue directly
			while not next_group.empty():
				q.put(next_group.get())
	
	print('Tree has been created.')
	tree.unflatten().render()					# save diagram in generated .pdf

def readSheet(sheet):			# 1
	import pandas as pd
	df = pd.read_csv(sheet)		# 2
	df.rename(columns=df.iloc[0], inplace=True)
	df.drop([0], inplace=True)
	df.dropna(inplace=True)
	df.set_index(df['Result'], inplace=True)
	df.drop(columns=['Result','Season','Position'], inplace=True)
	
	print(df)
	return df

df = readSheet('Pixel People Formulas.csv')
animal = input('Give an animal to display (\'q\' to quit): ')	# 3
printTree(animal, df)
print('Thank you.')



# Given the formula for animals, display animals needed to create
# Also display when there is a cycle
# TODO: figure out when to stop displaying, or if I need to continue displaying an animal
# Also, display cycles if possible. So maybe stop when we hit a cycle?

# 1. Read in excel sheet, save to df
# 2. Get animal to display.
# 3. Grab animal from df, get results for child animals. *BFS*
# 4. Need to know when to stop creating the graph. Currently uses BFS and stops at cycles, but I want it to stop like 3 levels down. Or format it to have levels (rank).
