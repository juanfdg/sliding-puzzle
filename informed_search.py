from sliding_puzzle import SlidingPuzzle
import heapq
import random
import time


def greedy_search(puzzle: SlidingPuzzle):
    start = SlidingPuzzle(puzzle.side, greedy=True, empty=puzzle.empty,
                          tiles=puzzle.tiles, score=puzzle.score)
    goal = SlidingPuzzle(puzzle.side, greedy=True)
    states = {start.key: start}
    heap = []
    heapq.heappush(heap, start)
    found = False
    while heap:
        state = heapq.heappop(heap)
        state.visited = True
        if state.key == goal.key:
            found = True

        up = state.up()
        down = state.down()
        left = state.left()
        right = state.right()
        children = [up, down, left, right]
        for c in children:
            if c is not None:
                curr_c = states.get(c.key)
                if curr_c is None or not curr_c.visited:
                    states[c.key] = c
                    heapq.heappush(heap, c)

        if found:
            break

    path = [states[goal.key]]
    while path[0].parent:
        path.insert(0, states[path[0].parent])
    return path


def a_star_search(puzzle: SlidingPuzzle):
    start = SlidingPuzzle(puzzle.side, empty=puzzle.empty, tiles=puzzle.tiles,
                          score=puzzle.score)
    goal = SlidingPuzzle(puzzle.side)
    states = {start.key: start}
    heap = []
    heapq.heappush(heap, start)
    found = False
    while heap:
        state = heapq.heappop(heap)

        if state.key == goal.key:
            found = True

        up = state.up()
        down = state.down()
        left = state.left()
        right = state.right()
        children = [up, down, left, right]
        for c in children:
            if c is not None:
                curr_c = states.get(c.key)
                if curr_c is None:
                    states[c.key] = c
                    heapq.heappush(heap, c)
                elif curr_c.cost > c.cost:
                    states[c.key] = c
                    i = 0
                    while heap[i].key != c.key:
                        i += 1
                    heap[i] = c
                    heapq._siftdown(heap, c)

        if found:
            break

    path = [states[goal.key]]
    while path[0].parent:
        path.insert(0, states[path[0].parent])
    return path


def compare_searches(puzzle):
    print(f"Starting state:")
    print(puzzle)
    start = time.time()
    path = greedy_search(puzzle)
    end = time.time()
    print(f"Greedy search computing time: {end - start}")
    print(f"Greedy search path cost: {len(path) - 1}")
    print("Path for greedy search:")
    #for state in path:
    #    print(state, state.score)
    print('\n------------------------------------------\n')
    start = time.time()
    path = a_star_search(puzzle)
    end = time.time()
    print(f"A* search computing time: {end - start}")
    print(f"A* search path cost: {len(path) - 1}")
    print("Path for A* search:")
    #for state in path:
    #    print(state)
    print('\n******************************************\n')


if __name__ == "__main__":
    print("Easy case:")
    puzzle = SlidingPuzzle.from_tuple((
        1,  2,  3,  4,  5,  6,  7,  8,  9,
        10, 11, 12, 13, 14, 15, 16, 17, 18,
        19, 20, 21, 22, 23, 24, 25, 26, 27,
        28, 29, 30, 31, 32, 33, 34, 35, 36,
        37, 38, 39, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49, 50, 51, 52, 53, 54,
        55, 56, 57, 58, 59, 81, 61, 62, 63,
        64, 65, 66, 67, 68, 60, 71, 79, 72,
        73, 74, 75, 76, 77, 69, 78, 70, 80
    ))
    compare_searches(puzzle)

    """
    print("Hard case:")
    puzzle = SlidingPuzzle.from_tuple((
        10, 44, 27, 28, 61, 8,  14, 17, 81,
        22, 6,  16, 43, 48, 51, 36, 2,  68,
        24, 38, 37, 45, 18, 41, 70, 34, 46,
        55, 4,  1,  30, 50, 58, 32, 12, 9,
        3,  23, 60, 56, 40, 15, 72, 54, 20,
        7,  25, 11, 47, 5,  74, 29, 35, 26,
        52, 57, 73, 65, 49, 42, 77, 78, 21,
        31, 67, 13, 53, 62, 66, 80, 33, 69,
        39, 75, 64, 19, 59, 76, 63, 79, 71
    ))
    compare_searches(puzzle)
    """

    random.seed(20)
    for i in range(15):
        print(f"Random case {i}:")
        puzzle = SlidingPuzzle(9).random(30)
        compare_searches(puzzle)
