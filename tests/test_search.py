import random

import pytest

from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def apply(state: State, actions):
    """Reaplica as ações a partir do estado inicial e devolve as peças finais."""
    current = State(state.tiles)
    for action in actions:
        current = next(n for n in current.neighbors() if n.action == action)
    return current.tiles


def scramble(moves: int, seed: int) -> State:
    rng = random.Random(seed)
    s = State(GOAL_STATE)
    for _ in range(moves):
        s = rng.choice(s.neighbors())
    return State(s.tiles)


SOLVABLE = [
    (State((1, 2, 3, 4, 5, 6, 7, 0, 8)), 1),
    (State((1, 2, 3, 4, 5, 6, 0, 7, 8)), 2),
    (State((1, 2, 3, 0, 4, 6, 7, 5, 8)), 3),
    (State((7, 2, 4, 5, 0, 6, 8, 3, 1)), 20),
]
UNSOLVABLE = State((2, 8, 3, 1, 6, 4, 7, 0, 5))


# ---------- State ----------

def test_neighbors_corner_and_center():
    corner = State((0, 1, 2, 3, 4, 5, 6, 7, 8))
    assert sorted(n.action for n in corner.neighbors()) == ["DOWN", "RIGHT"]
    center = State((1, 2, 3, 4, 0, 5, 6, 7, 8))
    assert len(center.neighbors()) == 4
    for n in center.neighbors():
        assert n.parent is center and n.cost == 1


def test_path_and_actions():
    s0 = State((1, 2, 3, 4, 5, 6, 0, 7, 8))
    s1 = next(n for n in s0.neighbors() if n.action == "RIGHT")
    s2 = next(n for n in s1.neighbors() if n.action == "RIGHT")
    assert s2.is_goal
    assert s2.path() == [s0, s1, s2]
    assert s2.actions() == ["RIGHT", "RIGHT"]
    assert s0.actions() == []


def test_solvability():
    assert State(GOAL_STATE).is_solvable
    assert not UNSOLVABLE.is_solvable


# ---------- Algoritmos ----------

ALGOS = [BFS, DFS, AStar]


@pytest.mark.parametrize("algo", ALGOS)
def test_goal_is_initial(algo):
    r = algo().search(State(GOAL_STATE))
    assert r.found and r.actions == [] and r.depth == 0 and r.path_cost == 0


@pytest.mark.parametrize("algo", ALGOS)
@pytest.mark.parametrize("initial,_", SOLVABLE)
def test_finds_valid_solution(algo, initial, _):
    r = algo().search(initial)
    assert r.found
    assert r.solution.is_goal
    assert apply(initial, r.actions) == GOAL_STATE
    assert r.depth == len(r.actions) == r.path_cost
    assert r.nodes_generated >= r.nodes_expanded


@pytest.mark.parametrize("algo", [BFS, AStar])
@pytest.mark.parametrize("initial,optimal", SOLVABLE)
def test_optimal(algo, initial, optimal):
    assert algo().search(initial).depth == optimal


def test_dfs_respects_depth_limit():
    initial = State((7, 2, 4, 5, 0, 6, 8, 3, 1))  # ótimo = 20
    assert not DFS(depth_limit=10).search(initial).found
    r = DFS(depth_limit=25).search(initial)
    assert r.found and r.depth <= 25


@pytest.mark.parametrize("algo", ALGOS)
def test_unsolvable(algo):
    r = algo().search(UNSOLVABLE)
    assert not r.found and r.actions == [] and r.path_cost == -1


def test_heuristic_admissible():
    astar = AStar()
    assert astar.heuristic(State(GOAL_STATE)) == 0
    for seed in range(30):
        s = scramble(25, seed)
        assert astar.heuristic(s) <= BFS().search(s).depth


def test_astar_expands_less_than_bfs():
    initial = State((7, 2, 4, 5, 0, 6, 8, 3, 1))
    assert AStar().search(initial).nodes_expanded < BFS().search(initial).nodes_expanded


@pytest.mark.parametrize("seed", range(10))
def test_random_bfs_astar_agree(seed):
    s = scramble(30, seed)
    assert BFS().search(s).depth == AStar().search(s).depth
