# coding: utf-8

import heapq


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self.queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]


if __name__ == "__main__":
    p = PriorityQueue()
    p.push(100, 1)
    p.push(200, 1)
    p.push(300,1)

    print(p.pop())
    print(p.queue)