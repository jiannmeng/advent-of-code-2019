from functools import reduce
from itertools import combinations
from math import gcd


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f"<x={self.x}, y={self.y}, z={self.z}>"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def sign(self):
        return Vector3(*map(lambda t: -1 if t < 0 else 0 if t == 0 else 1, self))


class Moon:
    def __init__(self, position, velocity=Vector3(0, 0, 0)):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return f"pos: {self.position}, vel={self.velocity}"

    def __eq__(self, other):
        return self.position == other.position and self.velocity == other.velocity

    def move(self):
        self.position += self.velocity

    def potential_energy(self):
        return sum(map(abs, self.position))

    def kinetic_energy(self):
        return sum(map(abs, self.velocity))

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


class System:
    def __init__(self, moons, debug=False):
        # moons should be a list of Moon objects.
        self.moons = moons
        self.step = 0
        self.debug = debug

    def apply_gravity(self):
        for m1, m2 in combinations(self.moons, 2):  # moon1 and moon2
            diff = m1.position - m2.position
            m1.velocity -= diff.sign()
            m2.velocity += diff.sign()
        if self.debug:
            print(self)

    def tick(self):
        self.step += 1
        for m in self.moons:
            m.move()
        if self.debug:
            print(self)

    def energy(self):
        return sum([m.total_energy() for m in self.moons])

    def state(self):
        return (
            tuple((m.position.x, m.velocity.x) for m in self.moons),
            tuple((m.position.y, m.velocity.y) for m in self.moons),
            tuple((m.position.z, m.velocity.z) for m in self.moons),
        )

    def __str__(self):
        output = f"After {self.step} steps:"
        for m in self.moons:
            output += f"\n{m}"
        return output

    def __eq__(self, other):
        return all(a == b for a, b in zip(self.moons, other.moons))


def parse_vec(vecstr):
    vecstr = vecstr.replace("<", "").replace(">", "").replace(" ", "")
    vec = vecstr.split(",")
    x = int(vec[0].replace("x=", ""))
    y = int(vec[1].replace("y=", ""))
    z = int(vec[2].replace("z=", ""))
    return Vector3(x, y, z)


def lcm(a, b):
    """Lowest common multiple."""
    return int(a * b / gcd(a, b))


def lcms(*numbers):
    """Lowest common multiple of more than 2 numbers."""
    return reduce(lcm, numbers)


with open("inputs/input_12.txt") as file:
    moons = [m.strip() for m in file.readlines()]

# PART 1.
moons = list(map(parse_vec, moons))
moons = list(map(Moon, moons))
jupiter = System(moons)
for _ in range(1000):
    jupiter.apply_gravity()
    jupiter.tick()
part1 = jupiter.energy()

# PART 2.
jupiter = System(moons)  # reset system
history = {"x": set(), "y": set(), "z": set()}
period = [None, None, None]
while True:
    state = jupiter.state()
    for i, axis in enumerate("xyz"):
        if period[i] is None:
            if state[i] in history[axis]:
                period[i] = jupiter.step
                del history[axis]
            else:
                history[axis].add(state[i])
    if all(period):
        break
    jupiter.apply_gravity()
    jupiter.tick()
part2 = lcms(*period)

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
