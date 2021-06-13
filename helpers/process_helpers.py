import random


def get_random_heart_rate() -> int:
    """Returns a random heart rate value.

    Returns:
        int: Random heart rate.
    """
    return random.randint(40, 200)


def get_random_resp_rate() -> int:
    """Returns a random repiratory rate value.

    Returns:
        int: Random respiratory rate.
    """
    return random.randint(10, 50)


def get_random_activity() -> int:
    """Returns a random activity number.

    Returns:
        int: Random activity id.
    """
    return random.randint(0, 100)