#Backend should be in english
#Frontend can (and should) use spanish
import sys

class Node:
	token = ""
	prev = None
	next = None
	def __init__(self, t):
		token = t

#Analizers return -1 if everything is alright
#error line otherwise

alpha = 'abcdefghijklmnopqrstuvwxyz1234567890!?":+-\n\t '
tokens = []
symbols = []
root = None
curr = None

def read_file(file_name) -> str:
	code = ""
	try:
		with open(file_name, "r") as f:
			lines = f.readlines()
			for line in lines:
				code += line
			return code
	except:
		sys.exit("[ERROR] No se puede abrir el archivo :'v")

def lexer(code) -> int:
	line = 1
	token = ""
	in_string = False
	for c in code:
		if c == '\n':
			line += 1

		#Error
		if c not in alpha:
			return line

		#Build tokens
		if c.isspace() and not in_string:
			if not token == "":
				tokens.append(token)
				token = ""
		elif c == '"':
			in_string = not in_string
			token += c
			if not in_string:
				tokens.append(token)
				token = ""
		else:
			token += c
	tokens.append(token)
	return -1

#Process tokens here or something idk
def parser(code):
	pass


#Start of compilation
#file_name = input("file: ")
file_name = "exports/test.cmt"
code = read_file(file_name)

error = lexer(code)
if error > 0:
	sys.exit("[ERROR] de analisis lexico en linea " + str(error))

print(tokens)
   