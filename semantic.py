from parser import Node

def analyze(start_node: Node):
    table = {}  # symbol table: var_name -> value/type/etc
    curr_var_name = None

    node = start_node
    while node:
        print(node.type, end="\t->\t")
        print(node.value)

        if node.type == "DECLARAR_VAR":
            if node.value in table:
                raise TypeError(f"{node.value} ya ha sido declarada")
            # register variable in the table (value 0 as placeholder)
            table[node.value] = 0
            curr_var_name = node.value

        elif node.type == "EXPRESION":
            if not node.value.isnumeric():
                raise TypeError(f"{curr_var_name} debe ser un número entero")

        node = node.next  # move forward in the linked list

    return table
