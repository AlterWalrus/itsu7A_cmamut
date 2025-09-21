import re
KEYWORDS		= {"whencuando", "var", ":v", "plox", "xdxd"}
OPERATORS		= {"=", "+", "-", "*", "/"}
IDENTIFIER_RE	= re.compile(r"[a-z_][a-z0-9_]*$")

class Token():
	def __init__(self, value, type, line):
		self.value = value
		self.type = type
		self.line = line

	def __str__(self):
		return f"{self.value}: {self.type}\tln {self.line}"

def classify_token(token: str, line: int):
	if token in KEYWORDS:
		return Token(token, "KEYWORD", line)
	elif token in OPERATORS:
		return Token(token, "OPERATOR", line)
	elif IDENTIFIER_RE.match(token):
		return Token(token, "IDENTIFIER", line)
	elif token.isdigit():
		return Token(token, "NUMBER", line)
	elif token.startswith('"'):
		return Token(token, "STRING", line)
	else:
		raise SyntaxError(f"Token invalido en linea {line}")

def tokenize(code):
	tokens = []
	line = 0
	token = ""
	in_string = False
	in_comment = False

	for c in code:
		if c == '\n':
			line += 1
			if in_comment:
				in_comment = False

		if c == '!' and not in_string:
			in_comment = True
		if in_comment:
			continue

		#Build tokens
		if c.isspace() and not in_string:
			if not token == "":
				tokens.append(classify_token(token, line))
				token = ""
		elif c == '"':
			in_string = not in_string
			token += c
			if not in_string:
				tokens.append(classify_token(token, line))
				token = ""
		else:
			token += c
	tokens.append(classify_token(token, line))
	return tokens