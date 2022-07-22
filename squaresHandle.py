from collections import namedtuple
from termcolor import cprint

#errors code
err_code_INVALID_STRUCTURE = 0
err_code_REPEATED_VALUE = 1
err_code_UNSOLVABLE_TABLE = 2

Errors = {
err_code_INVALID_STRUCTURE : 
	"table is not a standard sudoku table", 
err_code_REPEATED_VALUE : 
	"some datas repeated in row , column or home", 
err_code_UNSOLVABLE_TABLE :
	"table is unsolvable"}





__row_flag = "row"
__column_flag = "column"
__squaresDefiner = namedtuple("Square", ["X", "Y"])
__homesDefiner = namedtuple("Home", ["X", "Y"])
	
sqCoordinate = lambda x, y : __squaresDefiner(x, y)

homeCoordinate = lambda x, y : __homesDefiner(x, y)

__squares = tuple((sqCoordinate(x, y) for x in range(1, 10) for y in range(1,10)))
	
	
def rows() :
	ordered = tuple(sorted(__squares, key = lambda sq : sq.Y * 9 + sq.X))
	return tuple((ordered[i : i + 9] for i in range(0, 81, 9)))


def rowOf(_sq) :
	return tuple({sq for sq in __squares if _sq.Y == sq.Y} - {_sq})


def columns() :
	ordered = tuple(sorted(__squares, key = lambda sq : sq.X * 9 + sq.Y))
	return tuple((ordered[i : i + 9]) for i in range(0, 81, 9))


def columnOf(_sq) :
	return tuple({sq for sq in __squares if _sq.X == sq.X} - {_sq})


def homes() :
	return {homeCoordinate(a, b) :  tuple((sqCoordinate((a - 1) * 3 + x, (b - 1) * 3 + y) for y in range(1, 4) for x in range(1, 4))) for b in range(1, 4) for a in range(1, 4)}


def homeOf(sq) :
	return homeCoordinate((sq.X - 1) // 3 + 1, (sq.Y - 1) // 3 + 1)


def homeSquaresOf(sq) :
	home = list( homes()[sqCoordinate((sq.X - 1) // 3 + 1 , (sq.Y - 1) // 3 + 1)] )
	
	home.remove(sq)
	return tuple(home)
	
	
def absoluteOf(sq) :
	return tuple(set(rowOf(sq)) | set(columnOf(sq)) | set(homeSquaresOf(sq)))
	

def absoluteOfInHome(sq, home) :
	return tuple( (_sq for _sq in absoluteOf(sq) if homeOf(_sq) == home) ) 


def relatedRowsOf(sq) :
	return __relatedOf(__row_flag, sq.Y)


def relatedColumnsOf(sq) :
	return __relatedOf(__column_flag, sq.X)


def __relatedOf(flag, num) :
	minInRelated = 3 * ((num - 1) // 3) + 1
	
	related = [x for x in range(minInRelated, minInRelated + 3)]
	related = tuple(set(related) - {num})
	
	func = None
	if flag == __row_flag :
		func = rows
		
	elif flag == __column_flag :
		func = columns
	
	return tuple((tuple(func())[rowNum - 1] for rowNum in related))
	

def catchError(errorCode) :
	message = None
	if errorCode not in Errors :
		message = "invalid error."
	
	message = Errors[errorCode]
	cprint(message, "red",attrs=["bold"])