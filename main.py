"""Script de demonstração — útil para depurar manualmente."""

from puzzle.state import State
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def print_result(name: str, result):
    print(f"\n{'='*40}")
    print(f"Algoritmo : {name}")
    if result.found:
        print(f"Solução   : {' → '.join(result.actions)}")
        print(f"Custo     : {result.path_cost}")
        print(f"Profund.  : {result.depth}")
    else:
        print("Solução   : NÃO ENCONTRADA")
    print(f"Expandidos: {result.nodes_expanded}")
    print(f"Gerados   : {result.nodes_generated}")
    print(f"Fronteira : {result.max_frontier_size} (máx)")


def run(initial: State):
    print("\nEstado inicial:")
    print(initial)
    if not initial.is_solvable:
        print("(sem solução para o objetivo 1 2 3 / 4 5 6 / 7 8 _ — paridade de inversões ímpar)")

    print_result("BFS",  BFS().search(initial))
    print_result("DFS",  DFS().search(initial))
    print_result("A*",   AStar().search(initial))


if __name__ == "__main__":
    # Estado do template original: clássico de livro, mas para o objetivo
    # 1 2 3 / 8 _ 4 / 7 6 5. Com o objetivo deste projeto ele não tem solução.
    run(State((2, 8, 3, 1, 6, 4, 7, 0, 5)))

    # Estado com solução ótima de 20 movimentos.
    run(State((7, 2, 4, 5, 0, 6, 8, 3, 1)))
