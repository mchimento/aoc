from day import Day
import re
from collections import defaultdict

class Day23(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.rows = self.input.process_data_as_rows(0)
        self.graph = defaultdict(set)
        for row in self.rows:
            c1 , c2 = re.split("-", row)
            self.graph[c1].add(c2)
            self.graph[c2].add(c1)

    def part1(self):
        def find_computer_sets_of_3():
            networks = set()
            for pc in self.graph:
                for neighbor in self.graph[pc]:
                    common_neighbors = self.graph[pc] & self.graph[neighbor]
                    for common in common_neighbors:
                        if pc.startswith('t') or neighbor.startswith('t') or common.startswith('t'):
                            triangle = tuple(sorted([pc, neighbor, common]))
                            networks.add(triangle)
            return networks

        sets = find_computer_sets_of_3()
        return len(sets)

    def part2(self):
        def bron_kerbosch(R, P, X, graph, cliques):
            if not P and not X:
                cliques.append(R)
                return
            for node in list(P):
                bron_kerbosch(R | {node}, P & graph[node], X & graph[node], graph, cliques)
                P.remove(node)
                X.add(node)

        def find_maximal_cliques(graph):
            cliques = []
            nodes = set(graph.keys())
            bron_kerbosch(set(), nodes, set(), graph, cliques)
            return cliques

        cliques = find_maximal_cliques(self.graph)
        max_size = max(len(clique) for clique in cliques)
        largest_cliques = sorted([clique for clique in cliques if len(clique) == max_size][0])
        return largest_cliques