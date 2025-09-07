#Backend should be in english
#Frontend can (and should) use spanish
import sys
from lexer import tokenize
from parser import Parser

def read_file(file_name):
	code = ""
	try:
		with open(file_name, "r") as f:
			lines = f.readlines()
			for line in lines:
				code += line
			return code
	except:
		sys.exit("[ERROR] No se puede abrir el archivo :'v")

#Start of compilation
#file_name = input("file: ")
file_name = "examples/hello.cmt"
code = read_file(file_name)

try:
	tokens = tokenize(code)
except Exception as e:
	sys.exit(f"[ERROR LEXICO] {e}")

print("Tokens: ")
print(tokens)

try:
	parser = Parser(tokens)
	ast = parser.parse()
	print("\nArbol de Sintaxis Abstracta:")
	print(ast)
except Exception as e:
	sys.exit(f"[ERROR SINTACTICO] {e}")
   