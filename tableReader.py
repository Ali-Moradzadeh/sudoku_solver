from squaresHandle import *
from termcolor import cprint

class tReader :
	
	__column = "column"
	__row = "row"
	__mainSquares = {}
	__savedNumbers = []

	def __init__(self, definer, tbFunc) :
		
		self.__Definer = definer
		self.__table = tbFunc
	
	
	def getTable(self) :
		return self.__table()
		
	
	def valuesOf(self, subSquares) :
		return tuple( [self.__table()[sq] for sq in subSquares] )
		
		
	def valuesOfNested(self, sqs) :
		return tuple( (self.valuesOf(k) for k in sqs) )
	

	def rowsValues(self) :
		return tuple([self.valuesOf(rows()[i]) for i in range(0, 9)])


	def columnsValues(self) :
		return tuple([self.valuesOf(columns()[i]) for i in range(0, 9)])


	def homesValues(self)  :
		return tuple( tuple( [self.__table()[sq] for sq in subSq]) for subSq in set(homes().values()) )
	
	
	def __checkValidRowOrColumn(self,which) :
	
		values = self.rowsValues if which == self.__row else self.columnsValues
		
		for sub in values() :
			
			valid = True
			for num in sub :
			
				if num != None :
				
					if not (valid := sub.count(num) == 1) :
						break
		
			if not valid :
				break
			
		return valid
	
	
	def checkValidTable(self) :
		return self.__checkValidRowOrColumn(self.__row) and self.__checkValidRowOrColumn(self.__column)


	def valueCount(self, number) :
		return list(self.__table().values()).count(number)


	def valuePositions(self, number) :
		return tuple( (k for k, v in self. __table.items() if v == number) )


	def possibleValuesOf(self, sq) :
		if self.__table()[sq] != None :
			return set()
	
		z = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		for _sq in absoluteOf(sq) :
			z-= {self.__table()[_sq]}
	
		return z


	def forbiddenValuesOf(self, square) :
	
		alls = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		possible = self. possibleValuesOf(square)
		return alls - possible


	def solvedSquaresCount(self) :
	
		result = 0
		for v in self.__table().values() :
			result += 1 if v != None else 0
		
		return result


	def relatedRowsValuesOf(self, sq) :
		return self.valuesOfNested(relatedRowsOf(sq))

	def relatedColumnsValuesOf(self, sq) :
		return self. valuesOfNested(relatedColumnsOf(sq))


	def abosulteValuesOf(self, sq) :
		return self. valuesOf(absoluteOf(sq))


	def getPossibleNumsOfEmptySquares(self) :
		result = {}
		for k,v in self.__table().items() :
		
			if v == None :
				result[k] = set(self.possibleValuesOf(k))
	
		return result


	def squaresWithExactPossibleValues(self, number) :
	
		return {k : v for k, v in self.getPossibleNumsOfEmptySquares().items() if len(v) == number}

	
	def backToLastTable(self) :
		return self.__savedNumbers.pop()
	

	def getLastSavedNumbers(self) :
		return self.__savedNumbers
	
	
	def getMainTables(self) :
		return self.__mainSquares
	
	
	def dictValues(self, subSquares) :
		
		return {k : v for k, v in self.__table().items() if k in subSquares}

	def showInvalidTable(self) :
			
		if self.__Definer.isInNoWayState() :
			catchError(err_code_UNSOLVABLE_TABLE)
			
		elif not self.checkValidTable() :
			catchError(err_code_REPEATED_VALUE)
			