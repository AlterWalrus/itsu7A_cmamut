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
			table[node.value] = node.children[0].value
		
		case NodeType.ASS:
			valid_assign(node)
		
		case NodeType.PRINT:
			valid_print(node)
		
		case NodeType.INPUT:
			valid_input(node)

def valid_declaration(node):
	if node.value in table.keys():
		raise RuntimeError(f"la variable {node.value} ya ha sido declarada")

def valid_assign(node):
	if not node.value in table.keys():
		raise RuntimeError(f"la variable {node.value} no ha sido declarada")

def valid_print(node):
	if node.value[0] != '"' :
		if not node.value in table.keys():
			raise RuntimeError(f"la variable {node.value} no ha sido declarada")

def valid_input(node):
	if node.value[0] != '"' :
		if not node.value in table.keys():
			raise RuntimeError(f"la variable {node.value} no ha sido declarada")