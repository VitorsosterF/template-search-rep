from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (busca em grafo).

    Expande os nós em ordem FIFO, garantindo a solução com o menor número de
    movimentos. O teste de objetivo é feito na geração do nó.
    """

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1

        if not initial.is_solvable:  # paridade de inversões: objetivo inalcançável
            return SearchResult(None, 0, nodes_generated, 1, 0)

        if initial.is_goal:
            return SearchResult(initial, 0, nodes_generated, 1, initial.cost)

        frontier = deque([initial])
        reached = {initial.tiles}          # estados já gerados (fronteira + explorados)
        nodes_expanded = 0
        max_frontier = 1

        while frontier:
            node = frontier.popleft()
            nodes_expanded += 1

            for child in node.neighbors():
                if child.tiles in reached:
                    continue
                nodes_generated += 1
                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier,
                        depth=child.cost,
                    )
                reached.add(child.tiles)
                frontier.append(child)

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
