from dataclasses import dataclass, field

import networkx as nx


@dataclass
class CausalDAG:
    treatment: str
    outcome: str
    confounders: list[str] = field(default_factory=list)
    graph: nx.DiGraph = field(default_factory=nx.DiGraph)

    def add_edge(self, u: str, v: str) -> None:
        self.graph.add_edge(u, v)

    def from_config(self, edges: list[tuple[str, str]]) -> None:
        for u, v in edges:
            self.add_edge(u, v)

    def identify(self):
        # Returns backdoor adjustment set or raises IdentificationError
        raise NotImplementedError

    def plot(self) -> None:
        raise NotImplementedError
