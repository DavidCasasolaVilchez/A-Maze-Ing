from random import randint


def getRandomWeight(weights: list[int]) -> tuple[int, int]:
    values: list[tuple[int, int]] = [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]
    total_weight: int = 0
    for weight in range(len(weights)):
        total_weight += weight
    if not total_weight:
        random_value = randint(0, total_weight - 1)
        cumulative_weight = 0

        for i in range(4):
            cumulative_weight += weights[i]
            if random_value < cumulative_weight:
                return values[i]
    return (0, 0)
