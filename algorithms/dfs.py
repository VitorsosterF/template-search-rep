from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade.

    Usa uma pilha (LIFO) explícita. Para evitar ciclos e trabalho repetido,
    guarda a menor profundidade em que cada estado já foi alcançado: um estado
    só é revisitado se for alcançado por um caminho mais curto. Assim a busca
    é completa dentro do limite, mas — como toda DFS — não garante a solução
    ótima.
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:  # paridade de inversões: objetivo inalcançável
            return SearchResult(None, 0, 1, 1, 0)

        stack = [initial]
        best_depth = {initial.tiles: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier = 1

        while stack:
            node = stack.pop()

            # Entrada obsoleta: o estado já foi alcançado por um caminho mais curto.
            if best_depth.get(node.tiles, node.cost) < node.cost:
                continue

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier,
                    depth=node.cost,
                )

            if node.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            # Empilha em ordem inversa para expandir na ordem UP, DOWN, LEFT, RIGHT.
            for child in reversed(node.neighbors()):
                previous = best_depth.get(child.tiles)
                if previous is not None and previous <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                stack.append(child)
                nodes_generated += 1

            max_frontier = max(max_frontier, len(stack))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
