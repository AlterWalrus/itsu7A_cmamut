#Backend should be in english
#Frontend can (and should) use spanish
import sys
from lexer import tokenize
from parser import Parser
import semantic
from intermediate import IRGen

symbol_table = {}

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

#---- Start of compilation ----
#file_name = input("file: ")
file_name = "examples/hello.cmt"
code = read_file(file_name)

try:
	tokens = tokenize(code)
except Exception as e:
	sys.exit(f"[ERROR LEXICO] {e}")
for t in tokens:
	break
	print(t)
#print()
#print("-"*32)

try:
	parser = Parser(tokens)
	ast = parser.parse()
except Exception as e:
	sys.exit(f"[ERROR SINTACTICO] {e}")
#print(ast)
#print("-"*32)

try:
	symbol_table = semantic.analyze(ast)
except Exception as e:
	sys.exit(f"[ERROR SEMANTICO] {e}")
#print(symbol_table)

inter = IRGen()
ir = inter.generate(ast)
print(ir)