from day import Day
import networkx as nx
from itertools import chain

class Day11(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        def parse(row):
            edges = []
            node , reach_nodes = row.split(':')

            for rnode in reach_nodes.strip().split(' '):
                edges.append((node, rnode))

            return edges
        self.input =  list(chain.from_iterable(self.input.process_data_as_listed_rows(0, lambda row: parse(row))))

    def part1(self):
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(self.input)
        paths = list(nx.all_simple_paths(self.graph, source="you", target="out"))

        return len(paths)

    def count_paths_from(self, topo, source):
        dp = {n: 0 for n in topo}
        dp[source] = 1
        start_idx = topo.index(source)

        for u in topo[start_idx:]:
            if dp[u] == 0:
                continue
            for v in self.graph.successors(u):
                dp[v] += dp[u]

        return dp

    def part2(self):
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(self.input)

        topo = list(nx.topological_sort(self.graph))

        paths_from_svr_to_any_node = self.count_paths_from(topo, "svr")
        paths_from_ftt_to_any_node = self.count_paths_from(topo, "fft")
        paths_from_dac_to_any_node = self.count_paths_from(topo, "dac")

        return paths_from_svr_to_any_node["fft"] * paths_from_ftt_to_any_node["dac"] * paths_from_dac_to_any_node["out"]