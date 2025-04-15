# tree is created using dict
def createTree(root, formulas, level=4):
	if level == 0 or root == 'Cats':
		return ''

	currDict = {}
	animal1 = formulas.loc[root]["Parent 1"]
	animal2 = formulas.loc[root]["Parent 2"]
	currDict[animal1] = createTree(animal1, formulas, level-1)
	currDict[animal2] = createTree(animal2, formulas, level-1)
	# input(root + ' ' + str(currDict))

	return currDict

def printTree(root: dict, level: int=0):
	if root == '':
		return
	
	keys = list(root.keys())
	# print(keys)

	# left side
	for i in range(level-1):
		print(' |  ', end='')
	if level > 0:
		print(' |--', end='')
	print(keys[0])
	printTree(root[keys[0]], level+1)

	# right side
	if len(keys) > 1:
		for i in range(level-1):
			print(' |  ', end='')
		if level > 0:
			print(' |--', end='')
		print(keys[1])
		printTree(root[keys[1]], level+1)

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
# animal = input('Give an animal to display (\'q\' to quit): ')	# 3
# animal = animal.title()
animal = 'Tiger'
tree = {}
tree[animal] = createTree(animal, df)
print(animal, tree)
printTree(tree, 0)
print('Thank you.')



# Given the formula for animals, display animals needed to create
# Also display when there is a cycle
# TODO: figure out when to stop displaying, or if I need to continue displaying an animal
# Also, display cycles if possible. So maybe stop when we hit a cycle?

# 1. Read in excel sheet, save to df
# 2. Get animal to display.
# 3. Grab animal from df, get results for child animals. *BFS*
# 4. Need to know when to stop creating the graph. Currently uses BFS and stops at cycles, but I want it to stop like 3 levels down. Or format it to have levels (rank).
