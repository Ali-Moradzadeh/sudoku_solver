class errors :
	
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

class log :
	
	log_code_DEFAULT_EXACT = "set exact values"
	log_code_AFTER_GUESS_EXACT = "exact value after guess"
	log_code_GUESS = "guess"
	log_code_POSSIBLES = "possible values"
	log_code_INCORRECT_GUESS = "incorrect guess"
	log_code_RETURN = "return to last valid table"
	log_code_SOLVE_MESSAGE = "solve message"
	log_code_RESULT = "result"
	
	log_color_RED = "red"
	log_color_GREEN = "green"
	log_color_YELLOW = "yellow"
	log_color_WHITE = "white"
	log_color_MAGENTA = "magenta"
	log_color_BLUE = "blue"
	
	
	colorOf ={
log_code_DEFAULT_EXACT :
	log_color_GREEN,
		log_code_AFTER_GUESS_EXACT :
		log_color_WHITE, 
			
log_code_GUESS :
	log_color_YELLOW,
			
log_code_POSSIBLES :
	log_color_MAGENTA,
			
log_code_INCORRECT_GUESS :
	log_color_RED,

log_code_RETURN :
	log_color_RED,
			
log_code_SOLVE_MESSAGE :
	log_color_GREEN,

log_code_RESULT :
	log_color_GREEN
	}
