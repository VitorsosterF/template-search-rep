import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo.
_GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    """Busca A* com f(n) = g(n) + h(n).

    h(n) é a distância de Manhattan, que é admissível e consistente; por isso a
    primeira vez que o objetivo sai da fronteira o caminho é ótimo.
    """

    def heuristic(self, state: State) -> int:
        """Soma das distâncias de Manhattan de cada peça (exceto o vazio) até sua posição final."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            gr, gc = _GOAL_POS[tile]
            total += abs(r - gr) + abs(c - gc)
        return total

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:  # paridade de inversões: objetivo inalcançável
            return SearchResult(None, 0, 1, 1, 0)

        tie = count()  # desempate estável entre nós com o mesmo f
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: 0}
        closed = set()
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)

            if node.tiles in closed:
                continue  # entrada obsoleta, já expandida com custo menor

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier,
                    depth=node.cost,
                )

            closed.add(node.tiles)
            nodes_expanded += 1

            for child in node.neighbors():
                if child.tiles in closed:
                    continue
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    heapq.heappush(frontier, (child.cost + self.heuristic(child), next(tie), child))
                    nodes_generated += 1

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
