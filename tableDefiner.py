from tableWriter import tWriter
from tableReader import tReader
from branches import makeBranches

class tableDefiner :
	
	__reader = None
	__writer = None
	__makeBranch = None
	__noWayState = False
	
	def __init__(self, table) :
	
		self.__table = {k : v if v != 0 else None for k, v in table.items()}
		
		self.__constantValues = {k : v for k, v in table.items() if v != 0}
		
		self.__reader = tReader(self, self.__Table)
		
		self.__writer = tWriter(self, self.__update, self.__table)
	
	
	def writer(self) :
		return self.__writer
	
	
	def reader(self) :
		return self.__reader
	
	def branchTree(self) :
		if self.__makeBranch == None :
			self.__makeBranch = makeBranches(self)
		return self.__makeBranch
	
	
	def __update(self, table) :
		self.__table = table
	
	
	def constantValues(self) :
		return self.__constantValues
	
	def reachToNoWayState(self) :
		self.__noWayState = True
	
	
	def isInNoWayState(self) :
		return self.__noWayState
			
	def __Table(self) :
		return self.__table

