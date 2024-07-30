from graphviz import Digraph

def create_graph(min_heap, file_name = "output"):
    print(min_heap)
    dot = Digraph()

    # Add nodes
    for i in range(len(min_heap)):
        dot.node(str(i), str(min_heap[i]))

    # Add edges
    for i in range(len(min_heap)):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(min_heap):
            dot.edge(str(i), str(left))
        if right < len(min_heap):
            dot.edge(str(i), str(right))

    # Save as .svg file
    dot.render(file_name, format='svg')

class Node:
    def __init__(self, value, data) -> None:
        self.val = value
        self.data = data
    def __repr__(self) -> str:
        return f"{self.val}"


class MinHeap:
    def __init__(self) -> None:
        # Heap property: all child nodes of a given parent node should be greater than the parent node 
        # indexing the heap is as follows: min=heap[0], parent=heap[(i-1)//2], 
        # left_child = heap[(2*i)+1], right_child = heap[(2*i)+2]
        self.heap = []

    def heapSize(self):
        return len(self.heap)

    def getMin(self):
        return self.heap[0]
    
    def removeMin(self):
        self.heap.pop(0)
    
    def parent(self, i):
        return self.heap[(i-1)//2]
    
    def leftChild(self, i):
        return self.heap[(2*i)+1]
    
    def rightChild(self, i):
        return self.heap[(2*i)+2]

    def heapify(self):
        for i in range((self.heapSize()//2 -1), -1, -1):
           self.downHeap(i)

    def downHeap(self, i):
        sm_idx = i
        n = self.heapSize()
        if 2*i+1 < n and self.leftChild(i).val < self.heap[sm_idx].val:
            sm_idx = 2*i+1
        if 2*i+2 < n and self.rightChild(i).val < self.heap[sm_idx].val:
            sm_idx = 2*i+2
        if sm_idx != i:
            self.heap[i], self.heap[sm_idx] = self.heap[sm_idx], self.heap[i]
            self.downHeap(sm_idx)            

    def bubbleUp(self):
        i = len(self.heap)-1
        while i>0:
            parent_i = ((i-1)//2)
            if self.heap[i].val < self.heap[parent_i].val:
                self.heap[parent_i], self.heap[i] = self.heap[i], self.heap[parent_i] 
                i = parent_i
            else:
                break

    def addNode(self, node):
        self.heap.append(node)
        self.bubbleUp()

if __name__ == "__main__":
    nodes = [(35, "E"),(15, "M"), (22, "A"), (27,"C"), (40, "F"), (29, "G"), (76, "Z")]
    nodes = [Node(i[0], i[1]) for i in nodes]
    min_heap = MinHeap()
    for n in nodes:
        min_heap.addNode(n)
    min_heap.removeMin()
    create_graph(min_heap.heap, file_name = "output2")
    min_heap.heapify()
    create_graph(min_heap.heap, file_name = "output3")