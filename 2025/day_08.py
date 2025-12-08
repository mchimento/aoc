from day import Day
import itertools
from collections import Counter
import math

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False

        # union by rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[rb] < self.rank[ra]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

class Day8(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.input = self.input.process_data_as_listed_rows(0, lambda s: tuple(map(int, s.split(','))))

    def current_cluster_sizes(self):
        n = len(self.uf.parent)
        roots = [self.uf.find(i) for i in range(n)]
        counter = Counter(roots)
        return sorted(counter.values(), reverse=True)

    def compute_edges(self, points):
        """ All points pairwise distances """
        edges = []
        for i, j in itertools.combinations(range(len(points)), 2):
            p = points[i]
            q = points[j]
            dx = p[0] - q[0]
            dy = p[1] - q[1]
            dz = p[2] - q[2]
            dist2 = dx*dx + dy*dy + dz*dz
            edges.append((dist2, i, j))

        edges.sort(key=lambda e: e[0])
        return edges

    def part1(self):
        points = list(self.input)
        n = len(points)

        self.uf = UnionFind(n)
        self.edges = self.compute_edges(points)
        self.edge_index = 0

        x = 0
        iter = 10
        while x < iter and self.edge_index < len(self.edges):
            dist2, i, j = self.edges[self.edge_index]
            self.edge_index += 1
            self.uf.union(i, j)
            x += 1
            sizes = self.current_cluster_sizes()
            if len(sizes) == 1:
                break

        self.large_circuit = points[i][0] * points[j][0]

        while len(sizes) < 3:
            sizes.append(1)

        return sizes[0] * sizes[1] * sizes[2]

    def part2(self):
        return self.large_circuit