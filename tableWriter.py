from collections import namedtuple
from constants import log
from termcolor import cprint

class tWriter :
	
	__tables = []
	__log = namedtuple("Log", ["num", "topic", "message"])
	__listeningToUpdate = False
	__updatesCount = 0
	
	def __init__(self, definer, updateFunc, table) :
		
		self.__Definer = definer
		self.__mBranchObj = definer.branchTree()
		self.__table = dict(table)
		self.__updateFunc = updateFunc
		self.__logs = []
	
	
	def setValue(self, sq, record) :
		
		if sq in self.__Definer.constantValues().keys() :
			return False
		
		if self.__listeningToUpdate :
			self.__updatesCount += 1
		
		self.__table[sq] = record
		self.applyChanges()
		return True
		
	
	def applyChanges(self) :
		self.__updateFunc(self.__table)
	
	
	def createBranchOf(self, dic) :
		
		self.__mBranchObj.create(list(dic.keys())[0], list(dic.values())[0])
		self.applyChanges()
		self.__tables.append(dict(self.__table))
		for k, v in dic.items() :
			self.setValue(k, v)
	
	
	def returnLastTable(self) :
		if len(self.__tables) == 0 :
			self.__Definer.reachToNoWayState()
			return
		
		self.__table = self.__tables.pop()
		self.applyChanges()
		self.__Definer.branchTree().addForbiddenTree()
	
	
	def isListeningToUpdate(self) :
		return self.__listeningToUpdate
	
	
	def listenToChanges(self) :
		self.__listeningToUpdate = True
	
	
	def getChanges(self, nextListen) :
		result = self.__updatesCount
	
		if nextListen :
			self.listenToChanges()
		else :
		 	self.finishListening()
		 
		return result
	
	
	def finishListening(self) :
		self.__listeningToUpdate = False
		self.__updatesCount = 0
	
	def tableNumber(self, num) :
		return self.__table[num - 1]


	def setLog(self, message, code, show) :
		self.__logs.append(self.__log(len(self.__logs) + 1, code, message))
		
		if show :
			if code == log.log_code_RESULT :
				print(*message,sep="\n")
			else :
				cprint(message, log.colorOf[code])
	
	def logLength(self) :
		return len(self.__logs)
	
	
	def printLogs(self) :
		
		for logg in self.__logs :
			if logg.topic == log.log_code_RESULT :
				print(*logg.message, sep="\n")
			else :
				cprint(f"{logg.num}) {logg.topic} : {logg.message}", log.colorOf[logg.topic])
