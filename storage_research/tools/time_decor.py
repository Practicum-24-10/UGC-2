import time
import csv
from typing import Callable


def timing_decorator(text: str, path: str):
    def func_wrapper(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            # print(f"Время начала выполнения: {start_time}")
            # print(f"Время окончания выполнения: {end_time}")
            if result is not None:
                with open(path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [text, func.__name__, execution_time, result])
            # print(f"Время выполнения: {execution_time} секунд")
            return result

        return wrapper

    return func_wrapper
