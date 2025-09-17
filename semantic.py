from parser import Node, NodeType

table = {}

def analyze(node: Node):
	table = {}
	nodes = [node]

	for node in nodes:
		process_node(node)
		nodes.extend(node.children)

	return table

def process_node(node):
	match node.type:
		case NodeType.DEC:
			valid_declaration(node)
			table[node.value] = node.children[0].value
		
		case NodeType.ASSIGN:
			valid_assign(node)

def valid_declaration(node):
	val = node.children[0].value

	if not val.isnumeric():
		raise TypeError(f"el valor de {node.value} debe ser un entero positivo")
	
	if node.value in table.keys():
		raise RuntimeError(f"la variable {node.value} ya ha sido declarada")

def valid_assign(node):
	val = node.children[0].value
	if not val.isnumeric():
		raise TypeError(f"el valor de {node.value} debe ser un entero positivo")
	
	if not node.value in table.keys():
		raise RuntimeError(f"la variable {node.value} no ha sido declarada")