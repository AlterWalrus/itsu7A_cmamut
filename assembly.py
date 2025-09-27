class ASMGen:
	def __init__(self):
		self.data_block = ""
		self.code_block = ""
		
	def generate(self, code: str):
		for line in code.splitlines():
			if line == "":
				continue
			tokens = line.split()
			print(tokens)

			match tokens[0]:
				case "+":
					self.code_block += f"mov al {tokens[2]}\n"
					self.code_block += f"add {tokens[1]} al\n"

				case "dec":
					self.data_block += f"{tokens[1]} db ?\n"
				
				case "print":
					self.code_block += f"mov ax {tokens[1]}\n"
					self.code_block += f"call print_num\n"
				
				case "input":
					self.code_block += f"call read_num\n"
					self.code_block += f"mov {tokens[1]}, al\n"
		
		return self.insert_code()

	def insert_code(self):
		code = ""
		with open("template.asm", "r") as file:
			for line in file:
				ln = line.strip()
				if ln == ";DATABLOCK":
					code += self.data_block
				elif ln == ";CODEBLOCK":
					code += self.code_block
				else:
					code += line
		return code
		