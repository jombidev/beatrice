import time


def get_system_time() -> int:
    return time.time_ns() // 1000000