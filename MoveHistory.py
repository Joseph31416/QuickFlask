class MoveHistory:
    def __init__(self, size):
        self.size = size
        self.data = [None]*self.size
        self.head = None
    
    def push(self, move):
        if self.head is None:
            self.head = 0
        else:
            self.head  = (self.head + 1) % self.size
        self.data[self.head] = move
    
    def pop(self):
        if self.head is None:
            return None
        else:
            move = self.data[self.head]
            self.data[self.head] = None
            if self.head == 0:
                self.head  = self.size - 1
                if self.data[self.head] is None:
                    self.head = None
            else:
                self.head -= 1
            return move