from _collections import deque


class MovingAverage:
    """
    A class to calculate moving average of a value, implemented with deque.
    """
    __slots__ = 'capacity', 'avg', 'dq', 'sum'

    def __init__(self, capacity):
        self.capacity = capacity
        self.avg = 0
        self.dq = deque()
        self.sum = 0

    def add(self, val):
        """
        :param val: new value
        :return: nothing
        """
        if len(self.dq) == self.capacity:
            self.sum -= self.dq.popleft()
        self.dq.append(val)
        self.sum += val
        if len(self.dq) != 0:
            self.avg = self.sum / len(self.dq)

    def get_moving_average(self):
        """
        :return: the current moving average
        """
        return self.avg
