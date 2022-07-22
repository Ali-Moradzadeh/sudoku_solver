from random import shuffle
from constants import log
from squaresHandle import ( sqCoordinate as square,
absoluteOf, homeOf, catchError, err_code_INVALID_STRUCTURE)
from tableDefiner import tableDefiner
from functools import reduce
import time

class Solver :
	
	__rowFlag = "row"
	__columnFlag = "column"
	__homeFlag = "home"
	__compare_emptyFlag = "empty"
	__compare_solvedFlag = "solved"
	__guessCounter = 0
	
	__directFindDoneCount = 0
	__indirectFindDoneCount = 0
	__invalidNumberAccured = False
	__definer = None
	__showLogs = False
	__invalidStructure = False
	__guessLogNums = []
	
	def __init__(self, rows) :
		
		self.start_time = time.time()
		try :
			eachNumberSquares = {square(x, y) : int(rows[y - 1][x - 1]) for y in range(1, 10) for x in range(1, 10)}
			self.__definer = tableDefiner(eachNumberSquares)
			self.__writer = self.__definer.writer()
			self.__reader = self.__definer.reader()
			self.__branches = self.__definer.branchTree()
			
		except :
			self.__invalidStructure = True
		
		
	def start(self) :
		if self.__invalidStructure :
			catchError(err_code_INVALID_STRUCTURE)
			
		elif self.__reader.checkValidTable() :
			self.__updateTill()
		
		else :
			self.__reader.showInvalidTable()
	
	def __indirectFinded(self, relatedTo, compareWith) :
	
		
		self.__writer.listenToChanges()
		for sq, value in self.__reader.getTable().items() :
			if value != None :
				continue
	
			relation = None
			compare = None
	
			#reference for reduce num from possible
			reference = None
	
			#find relation with row or column or home
			forRow = lambda x, y : x.Y == y.Y
			forColumn = lambda x, y : x.X == y.X
			forHome = lambda x, y : homeOf(x) == homeOf(y)
	
			if relatedTo == self.__rowFlag :
				relation = forRow
	
			elif relatedTo == self.__columnFlag :
				relation = forColumn
	
			else :
				relation = forHome
		
	
			#find comparing with empty squares or solved squares
			if compareWith == self.__compare_emptyFlag :
				compare = lambda sq :self.__reader.getTable()[sq] == None
				reference = lambda sq :  set(self.__reader.possibleValuesOf(sq))
			
			elif compareWith == self.__compare_solvedFlag :
				compare = lambda sq : self.__reader.getTable()[sq] != None
				relation = lambda sq, _sq: True
				reference = lambda sq : {self.__reader.getTable()[sq]}
	
			absolute = tuple( (_sq for _sq in absoluteOf(sq) if relation(sq, _sq) and compare(sq)))
	
			possib = self.__reader.possibleValuesOf
			possibleNums = possib(sq)
		
			if len(possibleNums) == 0 and self.__guessCounter == 0 :
				self.__definer.reachToNoWayState()
				return 0
				
			elif len(possibleNums) == 0 :
				self.__setLog(f"error. {sq} found with no possible value", log.log_code_INCORRECT_GUESS)
				self.__writer.finishListening()
				self.__invalidNumberAccured = True
				return 0
			
			for _sq in absolute :
				possibleNums -= reference(_sq)
			
			if len(possibleNums) == 1 and value == None :
				flag = log.log_code_DEFAULT_EXACT
				string = f"exactly {sq} = { list(possibleNums)[0]}"
				
				if self.__guessCounter != 0 :
					flag = log.log_code_AFTER_GUESS_EXACT
					string = '--->' + string
					
				self.__setLog(string, flag)
				self.__writer.setValue(sq, list(possibleNums)[0])
	
		#cprint("finish", "blue")
		return self.__writer.getChanges(False)
	
	
	def __getExactNumbers(self) :
	
		lastThirdUpdatesResult = [None for i in range(0, 6)]
	
		relations = (self.__rowFlag, self.__columnFlag, self.__homeFlag)
	
		compares = (self.__compare_emptyFlag, self.__compare_solvedFlag)
	
		argsList = [(x, y) for x in relations for y in compares]
	
		args = tuple(argsList)
	
		func = self.__indirectFinded
	
		i = 0
	
		while lastThirdUpdatesResult.count(False) != 6 :
		
			updatesCount = func(args[i % 6][0], args[(i + 1) %6][1])
			
			if self.__definer.isInNoWayState() :
				break
			
			if self.__invalidNumberAccured :
				break
		
			lastThirdUpdatesResult[i % 6] = updatesCount != 0
		
			i += 1
	

	def __minPossibilitySquares(self) :
	
		mini = 9
		for x in range(2,10) :
		
			if len(self.__reader.squaresWithExactPossibleValues(x)) != 0 :
				mini = min(mini, x)
	
		return self.__reader.squaresWithExactPossibleValues(mini)


	def __chooseBestLuckySet(self) :
	
		minPossibleSquares = self.__minPossibilitySquares()
		
		
		def findBest() :
		
			comman = lambda sq : set(minPossibleSquares.keys()) & set(absoluteOf(sq))
			sqWithMaxCommanWithItsAbsoluteSqs = lambda sq1, sq2 : sq1 if len(comman(sq1)) > len(comman(sq2)) else sq2
			
			shuffleKeys = list(minPossibleSquares.keys())
			
			if len( minPossibleSquares[shuffleKeys[0]]) > 2 :
				shuffle(shuffleKeys)
			
			sq = reduce(sqWithMaxCommanWithItsAbsoluteSqs, shuffleKeys)
	
			values = [0]
			values.extend(minPossibleSquares[sq])
		
			values = tuple([v for v in values if not self.__branches.existInForbiddenTrees(sq, v)])
		
			if len(values) == 1 :
			
				self.__branches.mergeForbiddens(sq, minPossibleSquares[sq])
			
				return {sq : 0}
			string = f"for {sq} possibles are {set(values) - {0}}"
			self.__setLog(f"{string}", log.log_code_POSSIBLES)
			return {sq : reduce(lambda x, y : x if x > self.__reader.valueCount(y) else y, values)}
	
	
		pare = findBest()
	
		sq = list(pare.keys())[0]
		maxed = list(pare.values())[0]
	
	
		if maxed == 0 :
			return None
	
		exact = dict(minPossibleSquares)

		if len(exact[sq]) == 0 :
			return None
	
		return tuple((sq, maxed))


	def __makeBranch(self) :
	
		randPossible = self.__chooseBestLuckySet()
	
		if randPossible == None :
			return self.__backToLastTable()

		self.__writer.createBranchOf({randPossible[0] : randPossible[1]})
	
		self.__guessCounter += 1
		
		self.__guessLogNums.append((self.__writer.logLength(), randPossible[0], randPossible[1]))
		
		self.__setLog(f"{self.__guessCounter}) guess {randPossible[0]} = {randPossible[1]}\n", log.log_code_GUESS)
	


	def __backToLastTable(self) :
	
		self.__invalidNumberAccured = False
		
		self.__writer.returnLastTable()
		lastIncorrectTry = self.__guessLogNums.pop()
		
		
		
		self.__setLog(f"guess {lastIncorrectTry[1]} = {lastIncorrectTry[2]} was wrong so migrate to log number {lastIncorrectTry[0]}", log.log_code_RETURN)


	def __updateTill(self) :
		while self.__reader.solvedSquaresCount() != 81 :
		
			self.__getExactNumbers()
			
			if self.__definer.isInNoWayState() :
				self.__reader.showInvalidTable()
				break
			
			if self.__invalidNumberAccured :
				self.__backToLastTable()
		
			if self.__reader.solvedSquaresCount() == 81 :
				continue
		
			self.__makeBranch()
	
	
		else :
			self.__setLog(f"{32 * '*'}\nSuccessfully solved in {time.time() - self.start_time} seconds \n{32* '*'}", log.log_code_SOLVE_MESSAGE)
			
			self.__setLog(self.__reader.rowsValues(), log.log_code_RESULT)
		
	def __setLog(self, message, flag) :
		self.__writer.setLog(message, flag, self.__showLogs)
	
	
	def getResult(self) :
		return self.__reader.rowsValues()
	
	
	def setShowLogsWhileCalculate(self,  condition) :
		self.__showLogs = bool(condition)
		
		
	def getLogs(self) :
		return self.__writer.getLogs()
		
	def colorPrintLog(self) :
		self.__writer.printLogs()
