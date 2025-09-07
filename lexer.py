alpha = 'abcdefghijklmnopqrstuvwxyz1234567890!?,":=+-\n\t '

def tokenize(code):
	tokens = []
	line = 1
	token = ""
	in_string = False
	for c in code:
		if c == '\n':
			line += 1

		#Error
		if c not in alpha:
			raise SyntaxError(f"Caracter no valido en linea {line}")

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
	return tokens