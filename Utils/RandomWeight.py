from random import randint


def get_random_weight(weights: list[int]) -> tuple[int, int]:
    values: list[tuple[int, int]] = [
        (-1, 0), (0, 1), (1, 0), (0, -1)
    ]
    total_weight: int = 0
    for index in range(len(weights)):
        total_weight += weights[index]
    if total_weight != 0:
        random_value = randint(0, total_weight - 1)
        cumulative_weight = 0
        for i in range(4):
            cumulative_weight += weights[i]
            if random_value < cumulative_weight:
                return values[i]
    return (0, 0)


def generate_weights(weights: list[int], now: tuple[int, int],
                     exit: tuple[int, int]) -> list[int]:
    if now[0] < exit[0]:
        weights[2] = 1
        if weights[0] > 0:
            weights[0] = 0
    else:
        weights[0] = 1
        if weights[2] > 0:
            weights[2] = 0
    if now[1] < exit[1]:
        weights[1] = 1
        if weights[3] > 0:
            weights[3] = 0
    else:
        weights[3] = 1
        if weights[1] > 0:
            weights[1] = 0
    return weights
