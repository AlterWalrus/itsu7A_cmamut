class Node:
	def __init__(self, type, value=None, prev=None, next=None, line=None):
		self.type = type
		self.value = value
		self.prev = prev
		self.next = next
		self.line = line
	
	def __str__(self, level=0):
		indent = "  " * level
		res = f"{indent}{self.type}"
		if self.value:
			res += f": {self.value}"
		if self.line:
			res += f" (linea {self.line})"
		res += "\n"
		
		if self.prev:
			res += self.prev.__str__(level + 1)
		if self.next:
			res += self.next.__str__(level + 1)
		
		return res

def create_node(type, value=None, prev=None, next=None, line=None):
	return Node(type, value, prev, next, line)

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.pos = 0
		self.curr_token = tokens[0] if tokens else None

	def next(self):
		self.pos += 1
		if self.pos < len(self.tokens):
			self.curr_token = self.tokens[self.pos]

	def expect(self, value, error):
		if self.curr_token == value:
			self.next()
		else:
			raise SyntaxError(f"{error}. Se esperaba '{value}' y se obtuvo '{self.curr_token}'")
	
	def parse(self):
		self.expect("whencuando", "El programa debe empezar con 'whencuando'")

		program = Node("PROGRAMA")
		while self.curr_token and self.curr_token != "xdxd":
			statement = self.parse_statement()
			if statement:
				if program.prev is None:
					program.prev = statement
					last_statement = statement
				else:
					last_statement.next = statement
					last_statement = statement
			self.next()
        
		self.expect("xdxd", "El programa debe terminar con 'xdxd'")
		return program

	def parse_statement(self):
		print(self.curr_token)
		if self.curr_token == ":v":
			return self.parse_print()
		elif self.curr_token == "var":
			return self.parse_variable()
		elif self.curr_token == "plox":
			return self.parse_input()
		else:
			return self.parse_assign()
	
	def parse_print(self):
		self.next() #Consume :v
		if self.curr_token and self.curr_token.startswith('"'):
			msg = self.curr_token
			return Node("IMPRIMIR", msg)
		else:
			expression = self.parse_expression()
			return Node("IMPRIMIR", None, expression)
		
	def parse_variable(self):
		self.next()  #Consume "var"
		name = self.curr_token
		
		if self.tokens[self.pos+1] == "=":
			self.next() #Consume var name
			self.next() #Consume "="

			value = self.parse_expression()
			return Node("DECLARAR_VAR", name, value)
		else:
			#No value provided
			return Node("DECLARAR_VAR", name)
	
	def parse_input(self):
		self.next()  #Consume "plox"
		variable = self.curr_token
		self.next()
		return Node("LEER", variable)

	def parse_assign(self):
		if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1] == "=":
			variable = self.curr_token
			self.next()  #Consume variable
			self.next()  #Consume "="
			value = self.parse_expression()
			return Node("ASIGNAR", variable, value)
		else:
			return self.parse_expression()
	
	def parse_expression(self):
		izquierda = self.curr_token
		
		if self.pos + 2 < len(self.tokens) and self.tokens[self.pos + 1] in ["+", "-", "*", "/"]:
			operador = self.tokens[self.pos + 1]
			derecha = self.tokens[self.pos + 2]
			
			self.next()
			self.next()
			return Node("OPERACION", operador, 
						Node("EXPRESION", izquierda),
						Node("EXPRESION", derecha))
		else:
			expresion = self.curr_token
			self.next()
			return Node("EXPRESION", expresion)