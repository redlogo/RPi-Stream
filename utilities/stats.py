from _collections import deque


class MovingAverage:
    __slots__ = 'capacity', 'avg', 'dq', 'sum'

    def __init__(self, capacity):
        self.capacity = capacity
        self.avg = 0
        self.dq = deque()
        self.sum = 0

    def add(self, val):
        if len(self.dq) == self.capacity:
            self.sum -= self.dq.popleft()
        self.dq.append(val)
        self.sum += val
        if len(self.dq) != 0:
            self.avg = self.sum / len(self.dq)

    def get_moving_average(self):
        return self.avg
