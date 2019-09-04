from math import log10, sqrt
from random import randint

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class SlidingPuzzle(object):
    @classmethod
    def from_tuple(cls, tiles):
        side = int(sqrt(len(tiles)) + 0.5)
        if side ** 2 != len(tiles):
            raise RuntimeError("Argument passed not a perfect square sized tuple")
        puzzle = SlidingPuzzle(side)
        check = [0 for _ in range(side**2)]
        # Check if tiles passed satisfy the range of values wanted
        try:
            for idx, t in enumerate(tiles):
                # Avoid Python's list reverse indexing
                if t <= 0:
                    raise RuntimeError()
                check[t-1] += 1
                # Start computing puzzle attributes
                if t == side**2:
                    puzzle.empty = idx
                    puzzle.score += abs(t % side - idx % side)
                    puzzle.score += abs(int(t/side) - int(idx/side))

            for c in check:
                if c != 1:
                    raise RuntimeError()

        except (RuntimeError, IndexError):
            raise RuntimeError("Argument passed not restricted to correct range"
                               " of values (1 to side**2)")
        puzzle.tiles = list(tiles)
        return puzzle

    def __init__(self, side, greedy=False, tiles=None, empty=None, score=0,
                 cost=0, parent=None):
        self.side = side
        self.digits = int(log10(side**2)) + 1
        self.empty = empty if empty else side**2 - 1
        self.tiles = tiles if tiles else [i+1 for i in range(side**2)]
        # Path planning specifics
        self.score = score  # Sum of Manhattan distances
        self.cost = cost  # Cost function
        self.parent = parent  # Previous state in path
        self.greedy = greedy  # Whether cost should be solely based on score
        self.visited = False

    @property
    def key(self):
        """ Returns hashable key based on the unique configuration
        """
        return tuple(self.tiles)

    def move_up(self):
        if self.empty >= self.side:
            moved_tile = self.tiles[self.empty - self.side]
            self.tiles[self.empty] = moved_tile
            self.tiles[self.empty - self.side] = self.side**2
            self.empty = self.empty - self.side
            # Calculate score variation
            if int(self.empty/self.side) >= int((moved_tile - 1)/self.side):
                self.score = self.score + 1
            else:
                self.score = self.score - 1
            return self
        return None

    def move_down(self):
        if self.empty < (self.side-1)*self.side:
            moved_tile = self.tiles[self.empty + self.side]
            self.tiles[self.empty] = moved_tile
            self.tiles[self.empty + self.side] = self.side**2
            self.empty = self.empty + self.side
            # Calculate score variation
            if int(self.empty/self.side) <= int((moved_tile - 1)/self.side):
                self.score = self.score + 1
            else:
                self.score = self.score - 1
            return self
        return None

    def move_left(self):
        if self.empty % self.side > 0:
            moved_tile = self.tiles[self.empty - 1]
            self.tiles[self.empty] = self.tiles[self.empty - 1]
            self.tiles[self.empty - 1] = self.side**2
            self.empty = self.empty - 1
            # Calculate score variation
            if self.empty % self.side >= (moved_tile - 1) % self.side:
                self.score += 1
            else:
                self.score -= 1
            return self
        return None

    def move_right(self):
        if self.empty % self.side < self.side - 1:
            moved_tile = self.tiles[self.empty + 1]
            self.tiles[self.empty] = self.tiles[self.empty + 1]
            self.tiles[self.empty + 1] = self.side**2
            self.empty = self.empty + 1
            # Calculate score variation
            if self.empty % self.side <= (moved_tile - 1) % self.side:
                self.score += 1
            else:
                self.score -= 1
            return self
        return None

    def random(self, moves):
        for i in range(moves):
            possible_moves = [False] * 4
            if self.empty >= self.side:
                possible_moves[UP] = True
            if self.empty < (self.side - 1) * self.side:
                possible_moves[DOWN] = True
            if self.empty % self.side > 0:
                possible_moves[LEFT] = True
            if self.empty % self.side < self.side - 1:
                possible_moves[RIGHT] = True

            r = randint(0, 3)
            while not possible_moves[r]:
                r = randint(0, 3)

            if r == UP:
                self.move_up()
            elif r == DOWN:
                self.move_down()
            elif r == LEFT:
                self.move_left()
            elif r == RIGHT:
                self.move_right()

        return self

    def up(self):
        if self.empty >= self.side:
            tiles = self.tiles.copy()
            moved_tile = self.tiles[self.empty - self.side]
            tiles[self.empty] = moved_tile
            tiles[self.empty - self.side] = self.side**2
            empty = self.empty - self.side
            # Calculate score variation
            if int(empty/self.side) >= int((moved_tile - 1)/self.side):
                score = self.score + 1
            else:
                score = self.score - 1
            cost = self.cost + 1 + score
            return SlidingPuzzle(self.side, greedy=self.greedy, empty=empty,
                                 tiles=tiles, score=score, cost=cost,
                                 parent=self.key)
        return None

    def down(self):
        if self.empty < (self.side-1)*self.side:
            tiles = self.tiles.copy()
            moved_tile = self.tiles[self.empty + self.side]
            tiles[self.empty] = moved_tile
            tiles[self.empty + self.side] = self.side**2
            empty = self.empty + self.side
            # Calculate score variation
            if int(empty/self.side) <= int((moved_tile - 1)/self.side):
                score = self.score + 1
            else:
                score = self.score - 1
            cost = self.cost + 1 + score
            return SlidingPuzzle(self.side, greedy=self.greedy, empty=empty,
                                 tiles=tiles, score=score, cost=cost,
                                 parent=self.key)
        return None

    def left(self):
        if self.empty % self.side > 0:
            tiles = self.tiles.copy()
            moved_tile = self.tiles[self.empty - 1]
            tiles[self.empty] = moved_tile
            tiles[self.empty - 1] = self.side ** 2
            empty = self.empty - 1
            # Calculate score variation
            if empty % self.side >= (moved_tile - 1) % self.side:
                score = self.score + 1
            else:
                score = self.score - 1
            cost = self.cost + 1 + score
            return SlidingPuzzle(self.side, greedy=self.greedy, empty=empty,
                                 tiles=tiles, score=score, cost=cost,
                                 parent=self.key)
        return None

    def right(self):
        if self.empty % self.side < self.side - 1:
            tiles = self.tiles.copy()
            moved_tile = self.tiles[self.empty + 1]
            tiles[self.empty] = moved_tile
            tiles[self.empty + 1] = self.side**2
            empty = self.empty + 1
            # Calculate score variation
            if empty % self.side <= (moved_tile - 1) % self.side:
                score = self.score + 1
            else:
                score = self.score - 1
            cost = self.cost + 1 + score
            return SlidingPuzzle(self.side, greedy=self.greedy, empty=empty,
                                 tiles=tiles, score=score, cost=cost,
                                 parent=self.key)
        return None

    def __lt__(self, other):
        """ Comparing method between two puzzles based on score solely
        """
        if self.greedy:
            return self.score < other.score
        else:
            return self.cost < other.cost

    def __str__(self):
        ret = ''
        for i in range(self.side):
            for j in range(self.side):
                n = i*self.side + j
                if self.tiles[n] % self.side > 0:
                    ret += f'{self.tiles[n]:#{self.digits}d}'
                elif self.tiles[n] != self.side**2:
                    ret += f'{self.tiles[n]:#{self.digits}d}'
                else:
                    ret += ' ' * (self.digits-1) + '*'

                if j == self.side - 1:
                    ret += '\n'
                else:
                    ret += ' | '
        return ret


if __name__ == "__main__":
    # Test sliding puzzle class
    sp = SlidingPuzzle(9).random(5)
    print(sp)
    print(f'Score: {sp.score}')
