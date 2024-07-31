from graphviz import Digraph

class Node:
    def __init__(self, value, data=None) -> None:
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
        if self.heapSize() == 0:
            return None
        if self.heapSize() == 0:
            return self.heap.pop()
        self.heap.pop(0)
        self.heap[0] = self.heap.pop()
        self.downHeap(0)
    
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
        self.heapify()
    
    def create_graph(self, file_name = "output"):
        dot = Digraph()
        for i in range(self.heapSize):
            dot.node(str(i), str(self.heap[i]))
        for i in range(self.heapSize()):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < self.heapSize():
                dot.edge(str(i), str(left))
            if right < self.heapSize():
                dot.edge(str(i), str(right))
        dot.render(file_name, format='svg')