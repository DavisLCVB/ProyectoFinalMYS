from Generators import *


class Server:
    def __init__(self, gen: Generator) -> None:
        self.gen = gen
        self.end = 0

    def reset(self):
        self.end = 0


class ServiceArray:
    def __init__(self, servers: list[Server] = None) -> None:
        self.servers = servers
        self.end = 0

    def min_server(self):
        min = 100000000
        imin = 0
        for i, serv in enumerate(self.servers):
            if min > serv.end:
                min = serv.end
                imin = i
        return imin, min

    def reset(self):
        for serv in self.servers:
            serv.reset()


class Doc:
    def __init__(self):
        self.end = 0


class DocsArray:
    def __init__(self):
        self.count = 0
        self.docs = []

    def update(self, time):
        for doc in self.docs:
            if doc.end <= time:
                self.docs.remove(doc)
                self.count -= 1

    def add(self, end):
        self.docs.append(Doc())
        self.docs[-1].end = end
        self.count += 1

    def reset(self):
        self.count = 0
        self.docs = []
