class makeBranches :
	
	__currentBranch = []
	__forbiddenTrees = []
	__definerObj = None
	__index = -1
	
	def __init__(self, definerObj) :
		self.__definerObj = definerObj
		self.__currentBranch = []
		self.__forbiddenTrees = []
	
	
	def __exist(self, sq, value) :
		return {sq : value} in self.__currentBranch
	
	
	def create(self, sq, value) :
		
		if not self.__exist(sq, value) :
			self.__currentBranch.append({sq : value})
	
	
	def addForbiddenTree(self) :
		
		self.__forbiddenTrees.append(tuple(self.__currentBranch))
		self.__currentBranch.pop()
		
		
	def mergeForbiddens(self, sq, possibleValues) :
		
		x = [x for x in self.__forbiddenTrees if list(x[-1].keys())[0] == sq and list(x[-1].values())[0] in possibleValues]
		
		y = self.__forbiddenTrees
		
		for s in x :
			if s in y :
				y.remove(s)
		
		y.append(x[-1][:-1])
		
		del y
	
	
	def existInForbiddenTrees(self, sq, v) :
		
		lastBranchInTrees = [forbiddenTree[-1] for forbiddenTree in self.__forbiddenTrees]
		
		tillLastBranchInTrees = [forbiddenTree[:-1] for forbiddenTree in self.__forbiddenTrees]
		
		
		allsExist = True
		
		for forbiddenTree in tillLastBranchInTrees :
			
			allsExist = True
			for dic in forbiddenTree :
				
				_sq = list(dic.keys())[0]
				_v = list(dic.values())[0]
				
				
				if not (allExist := self.__definerObj.reader().getTable()[_sq] == _v) :
					break
			
			if not (allsExist := allExist) :
				break
		
		return allsExist and {sq : v} in lastBranchInTrees

