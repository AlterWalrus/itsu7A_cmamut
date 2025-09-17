from enum import Enum

keywords = ["whencuando", "var", ":v", "plox", "xdxd"]

class NodeType(Enum):
	START = "START"
	DEC = "DEC"
	INPUT = "INPUT"
	PRINT = "PRINT"
	MATH = "MATH"
	STR = "STR"
	VAR = "VAR"
	ASSIGN = "ASSIGN"
	END = "END"

class Node:
	def __init__(self, type: NodeType, value=None):
		self.type = type
		self.value = value
		self.children = []
	
	def add_child(self, node):
		self.children.append(node)

	def __str__(self):
		return self._stringify()

	def _stringify(self, level=0):
		indent = "  " * level
		node_str = f"{indent}{self.type.value}: {self.value}\n"
		for child in self.children:
			node_str += child._stringify(level + 1)
		return node_str

class Parser:
	def __init__(self, tokens):
		self.tokens: list = tokens
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

		program = Node(NodeType.START)
		while self.curr_token and self.curr_token != "xdxd":
			statement = self.parse_statement()
			program.add_child(statement)
			self.next()
        
		self.expect("xdxd", "El programa debe terminar con 'xdxd'")
		return program

	def parse_statement(self):
		#print(self.curr_token)
		if self.curr_token == ":v":
			return self.parse_print()
		elif self.curr_token == "var":
			return self.parse_declaration()
		elif self.curr_token == "plox":
			return self.parse_input()
		else:
			return self.parse_assign()
	
	def parse_print(self):
		node = Node(NodeType.PRINT)
		self.next()

		if self.curr_token in keywords:
			raise SyntaxError(f"{self.curr_token} es una palabra reservada")

		node.value = self.curr_token
		return node
		
	def parse_declaration(self):
		node = Node(NodeType.DEC)
		self.next() #Consume var

		if not self.valid_var_name(self.curr_token):
			raise SyntaxError(f"{self.curr_token} no es un nombre de variable valido")
		
		if self.curr_token in keywords:
			raise SyntaxError(f"{self.curr_token} es una palabra reservada")
		
		node.value = self.curr_token

		self.next()
		self.expect("=", "Forma de declaracion es var x = y")

		#only demo!!! get properly done later for complex operations and shit
		node.add_child(Node(NodeType.MATH, self.curr_token))

		return node
	
	def parse_input(self):
		pass

	def parse_assign(self):
		node = Node(NodeType.ASSIGN)
		
		if not self.valid_var_name(self.curr_token):
			raise SyntaxError(f"{self.curr_token} no es un nombre de variable valido")
		
		if self.curr_token in keywords:
			raise SyntaxError(f"{self.curr_token} es una palabra reservada")
		
		node.value = self.curr_token

		self.next()
		self.expect("=", "Forma de asignacion es x = y")

		#only demo!!! get properly done later for complex operations and shit
		node.add_child(Node(NodeType.MATH, self.curr_token))
		return node
	
	def parse_expression(self):
		pass

	def valid_var_name(self, var_name: str):
		if var_name[0] in "0123456789":
			return False
		return True