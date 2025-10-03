import re
TEMP_RE = re.compile(r"_t[0-9]+$")

class ASMGen:
	def __init__(self):
		self.data_block = ""
		self.code_block = ""
		self.string_id = 0
		self.temps = set()
		
	def generate(self, code: str, table: dict):
		for v in table.keys():
			self.data_block += f"{v} db ?\n"

		for line in code.splitlines():
			if line == "":
				continue
			tokens = line.split()

			for tok in tokens:
				if TEMP_RE.match(tok) and tok not in self.temps:
					self.data_block += f"{tok} db ?\n"
					self.temps.add(tok)

			match tokens[0]:
				case "=":
					self.code_block += f"mov al, {tokens[1]}\n"
					self.code_block += f"mov {tokens[2]}, al\n"

				case "+":
					self.code_block += f"mov al, {tokens[1]}\n"
					self.code_block += f"add al, {tokens[2]}\n"
					self.code_block += f"mov {tokens[3]}, al\n"
				
				case "-":
					self.code_block += f"mov al, {tokens[1]}\n"
					self.code_block += f"sub al, {tokens[2]}\n"
					self.code_block += f"mov {tokens[3]}, al\n"
				
				case "*":
					self.code_block += f"mov al, {tokens[1]}\n"
					self.code_block += f"mov bl, {tokens[2]}\n"
					self.code_block += f"mul bl\n"
					self.code_block += f"mov {tokens[3]}, al\n"
				
				case "/":
					self.code_block += f"xor ax, ax\n"
					self.code_block += f"mov al, {tokens[1]}\n"
					self.code_block += f"mov bl, {tokens[2]}\n"
					self.code_block += f"div bl\n"
					self.code_block += f"mov {tokens[3]}, al\n"
				
				case "print":
					if tokens[1].startswith('"'):
						msg = " ".join(tokens[1:])
						msg = msg.replace('"', '')
						self.data_block += f"_s{self.string_id} db '{msg}', 10, '$'\n"
						self.code_block += f"print _s{self.string_id}\n"
						self.string_id += 1
					else:
						self.code_block += f"mov al, {tokens[1]}\n"
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
		