class PriorityQueue():
    
    def __init__(self):
        self.queue = []
    
    # add a new element to the heap
    def push(self, value):
        self.queue.append(value)
        index = len(self.queue) - 1
        while index > 0:
            parent = (index - 1) // 2
            if self.queue[index] < self.queue[parent]:
                self.queue[index], self.queue[parent] = self.queue[parent], self.queue[index]
                index = parent
            else:
                break
    
    # pop an element from the heap and return it
    def pop(self):
        if len(self.queue) == 0:
            return None
        elif len(self.queue) == 1:
            return self.queue.pop()
        else:
            self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
            value = self.queue.pop()
            self.__down_heapify(0)
            return value
    
    # return the element of highest priority
    def top(self):
        return self.queue[0]
    
    # return the number of elements in the heap
    def size(self):
        return len(self.queue)
    
    # try pushing an element down the heap as deep as possible
    def __down_heapify(self, index):
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        smallest = index

        if left_child < len(self.queue) and self.queue[left_child] < self.queue[index]:
            smallest = left_child
        if right_child < len(self.queue) and self.queue[right_child] < self.queue[smallest]:
            smallest = right_child
        if smallest != index:
            self.queue[index], self.queue[smallest] = self.queue[smallest], self.queue[index]
            self.__down_heapify(smallest)
    
    # try pushing an element up the heap as far as possible
    def __up_heapify(self, index):
        parent = (index - 1) // 2
        if parent >= 0 and self.queue[index] < self.queue[parent]:
            self.queue[parent], self.queue[index] = self.queue[index], self.queue[parent]
            self.__up_heapify(parent)

def main():
    # testing
    queue = PriorityQueue()
    queue.push(3)
    queue.push(2)
    queue.push(1)
    while queue.size():
        print(queue.top())
        queue.pop()

if __name__ == "__main__":
    main()
