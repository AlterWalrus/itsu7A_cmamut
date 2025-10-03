from parser import Node, NodeType

table = {}

def analyze(node: Node):
	nodes = [node]
	for node in nodes:
		process_node(node)
		nodes.extend(node.children)
	return table

def process_node(node):
	match node.type:
		case NodeType.DEC:
			valid_declaration(node)
		
		case NodeType.ASS:
			valid_assign(node)
		
		case NodeType.PRINT:
			valid_print(node)
		
		case NodeType.INPUT:
			valid_input(node)

def valid_declaration(node):
	if node.value in table.keys():
		raise RuntimeError(f"la variable {node.value} ya ha sido declarada")

	table[node.value] = node.children[0].value
	if not table[node.value].isdigit():
		table[node.value] = "expresion"
	valid_assign(node)

def valid_assign(node):
	op = {"+", "-", "*", "/"}
	nodes = [node]
	for n in nodes:
		nodes.extend(n.children)
		if n.value in op:
			continue
		
		if n.value.isdigit():
			if int(n.value) < 0 or int(n.value) > 255:
				raise RuntimeError(f"el lenguaje solo acepta numeros positivos de 8 bits (0-255)")
			
		elif n.value not in table.keys():
			raise RuntimeError(f"la variable {n.value} no ha sido declarada")

def valid_print(node):
	if node.value[0] != '"' :
		if not node.value in table.keys():
			raise RuntimeError(f"la variable {node.value} no ha sido declarada")

def valid_input(node):
	if node.value[0] != '"' :
		if not node.value in table.keys():
			raise RuntimeError(f"la variable {node.value} no ha sido declarada")

def print_table(d: dict):
	print("{:<15} {:<10}".format('VARIABLE', 'VALOR'))
	for k in d.keys():
		print("{:<15} {:<10}".format(k, d[k]))
   
