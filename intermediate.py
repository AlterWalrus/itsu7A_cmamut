from parser import Node, NodeType

class IRGen:
	def __init__(self):
		self.t = 1

	def generate(self, root: Node):
		code = ""
		for node in root.children:

			if node.type == NodeType.DEC or node.type == NodeType.ASS:
				if node.type == NodeType.DEC:
					code += f"\ndec {node.value}"
				first_child = node.children[0]
				if first_child.value.isdigit():
					code += f"\n= {first_child.value} {node.value}"
				else:
					code += self.evaluate(first_child)
					code += f"\n= _t{self.t-1} {node.value}"

			elif node.type == NodeType.PRINT:
				code += f"\nprint {node.value}"

			elif node.type == NodeType.INPUT:
				code += f"\ninput {node.value}"
			
			code += "\n"
		return code

	def evaluate(self, root: Node):
		code = ""
		stack = []
		nodes = [root]
		OP = {'+', '-', '*', '/'}
		for node in nodes:
			if node.value in OP:
				stack.append(node)
			nodes.extend(node.children)

		while stack:
			n = stack.pop()
			var_name = f"_t{self.t}"
			code += f"\n{n.value} {n.children[0].value} {n.children[1].value} {var_name}"
			n.value = var_name
			self.t += 1

		return code