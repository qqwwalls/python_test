import time
from functools import wraps


def horizontal_line(symbol):
    print(symbol * 10)


def vertical_line(symbol):
    for _ in range(10):
        print(symbol)


def show_line(symbol, function_to_call):
    function_to_call(symbol)


def measure_time(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Час виконання функції: {end_time - start_time:.3f} секунди")
        return result

    return wrapper


@measure_time
def calculate_sum(n):
    return sum(range(1, n + 1))


if __name__ == "__main__":
    while True:
        symbol = input("Введіть символ для лінії: ")
        if len(symbol) == 1:
            break
        print("Введіть один символ.")

    while True:
        direction = input("Виберіть лінію: 1 - горизонтальна, 2 - вертикальна: ").strip()
        if direction in {"1", "2"}:
            break
        print("Введіть 1 або 2.")

    if direction == "1":
        show_line(symbol, horizontal_line)
    else:
        show_line(symbol, vertical_line)

    result = calculate_sum(1_000_000)
    print(f"Сума чисел: {result}")
