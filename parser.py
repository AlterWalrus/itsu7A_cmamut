from nodeAST import Node, NodeType
from lexer import Token
import re

class Parser:
	def __init__(self, tokens):
		self.tokens: list = tokens
		self.pos = 0
		self.curr_token: Token = tokens[0] if tokens else None

	def jump(self, step=1):
		self.pos += step
		if self.pos < len(self.tokens):
			self.curr_token = self.tokens[self.pos]
		else:
			self.curr_token = self.tokens[-1]

	def expect(self, value, error):
		if self.curr_token.value == value:
			self.jump()
		else:
			raise SyntaxError(f"{error}. Se esperaba '{value}' y se obtuvo '{self.curr_token.value}' en linea {self.curr_token.line}")
	
	def parse(self):
		self.expect("whencuando", "El programa debe empezar con 'whencuando'")

		program = Node(NodeType.START)
		while self.curr_token and self.curr_token.value != "xdxd":
			if self.curr_token.type == "ENDL":
				self.jump()
				continue
			statement = self.parse_statement()
			program.add_child(statement)
			self.jump()
        
		self.expect("xdxd", "El programa debe terminar con 'xdxd'")
		return program

	def parse_statement(self):
		#print(self.curr_token)
		if self.curr_token.value == "var":
			return self.parse_declaration()
		elif self.curr_token.value == "plox":
			return self.parse_input()
		elif self.curr_token.value == ":v":
			return self.parse_print()
		else:
			return self.parse_assign()
	
	def parse_input(self):
		node = Node(NodeType.INPUT)
		self.jump()

		if self.curr_token.type == "KEYWORD":
			raise SyntaxError(f"{self.curr_token.value} es una palabra reservada")

		node.value = self.curr_token.value
		return node

	def parse_print(self):
		node = Node(NodeType.PRINT)
		self.jump()

		if self.curr_token.type == "KEYWORD":
			raise SyntaxError(f"{self.curr_token.value} es una palabra reservada")

		node.value = self.curr_token.value
		return node
		
	def parse_declaration(self):
		#node = Node(NodeType.DEC)
		self.jump() #Consume var
		node = self.parse_assign()
		node.type = NodeType.DEC
		return node
		
	def parse_assign(self):
		node = Node(NodeType.ASS)

		if self.curr_token.type == "KEYWORD":
			raise SyntaxError(f"{self.curr_token.value} es una palabra reservada")
		
		node.value = self.curr_token.value

		self.jump()
		self.expect("=", "")

		exp = [self.curr_token.value]
		ext = 1
		while True:
			next = self.tokens[self.pos+ext]
			if next.type == "ENDL":
				break
			exp.append(next.value)
			ext += 1
		self.jump(ext-1)

		post_exp = self.postfix(exp)
		stack = []
		op = {'+', '-', '*', '/'}
		for t in post_exp:
			n = Node(NodeType.MATH)
			n.value = t
			if t in op:
				right = stack.pop()
				left = stack.pop()
				n.add_child(left)
				n.add_child(right)
			stack.append(n)
		node.add_child(stack[0])

		return node

	#what the fuck
	def postfix(self, tokens):
		precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
		output = []
		stack = []

		for token in tokens:
			if token == '(':
				stack.append(token)

			elif token == ')':
				while stack and stack[-1] != '(':
					output.append(stack.pop())
				if not stack:
					raise ValueError("Error de parentesis")
				stack.pop()
			
			elif token in precedence:
				while (stack and stack[-1] != '(' and
					((precedence[stack[-1]] > precedence[token]) or
						(precedence[stack[-1]] == precedence[token] and token != '^'))):
					output.append(stack.pop())
				stack.append(token)

			else:
				output.append(token)

		while stack:
			if stack[-1] in ('(', ')'):
				raise ValueError("Error de parentesis")
			output.append(stack.pop())

		return output