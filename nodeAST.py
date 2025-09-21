from enum import Enum

class NodeType(Enum):
	START = "START"
	INPUT = "INPUT"
	PRINT = "PRINT"
	MATH = "MATH"
	DEC = "DEC"
	VAR = "VAR"
	ASS = "ASS"

class Node:
	def __init__(self, type: NodeType, value=None):
		self.type = type
		self.value = value
		self.children = []
	
	def add_child(self, node):
		self.children.append(node)

	def __str__(self):
		return self._stringify()

	def _stringify(self, prefix: str = "", is_last: bool = True):
		connector = "└─ " if is_last else "├─ "
		node_str = f"{prefix}{connector}{self.type.value}: {self.value}\n"

		child_prefix = prefix + ("   " if is_last else "│  ")
		for i, child in enumerate(self.children):
			last = i == len(self.children) - 1
			node_str += child._stringify(child_prefix, last)

		return node_str
