from solver import Solver
from os import system

rows = ("800000000", 
			  "003600000", 
			  "070090200", 
			  
			  "050007000", 
			  "000045700", 
			  "000100030",
			  
			  "001000068", 
			  "008500010", 
			  "090000400")

solver = Solver(rows)
solver.setShowLogsWhileCalculate(True)
solver.start()
#solver.colorPrintLog()
