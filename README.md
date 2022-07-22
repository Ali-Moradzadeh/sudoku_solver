# sudoku_solver
this is a terminal little application that solve sudoku on any hardness level. save all calculates as log and you can see all calculates this program done while solving your sudoku
from

--requirement modules are :
	termcolor (for print colorful)

how to use ??
	as you can see in sample.py file sudoku table
	must save as list that this list should has
	rows number 1 to 9

	*********************************************
	***            IMPORTANT NOTE             ***
	*********************************************
	***      you must use 0 instead of        ***
	***    empty squares in sudoku puzzle     ***
	*********************************************

	then make an object of Solver class of solver.py
	file and pass it the list assigned previously
	as argument

	after that : just call start function of created
	object

	if you wana see calculates while solving just
	add this code
	solverObjectName.setShowLogsWhileCalculate(True)
	if you pass it 'False' you see nothing till end
	
	solverObjectName.getResult()
	give you a list of 9 tuples that each store
	solved numbers of a row

	solverObjectName.colorPrintLog()
	print all calculates in user-friendly colors

Good Luck
Thanks
