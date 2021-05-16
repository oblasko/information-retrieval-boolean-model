class Node:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.next_val = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, doc_id):
        new_node = Node(doc_id)
        if self.head is None:
            self.head = new_node
            return
        traverse = self.head
        while(traverse.next_val):
            traverse = traverse.next_val
        traverse.next_val = new_node

    def print(self):
        print_str = ""
        traverse = self.head
        while traverse is not None:
            print_str += str(traverse.doc_id) + " -> "
            traverse = traverse.next_val
        return print_str
