def odd_numbers(start, end):
    for number in range(start, end + 1):
        if number % 2 != 0:
            yield number


def multiples_of_five(start, end):
    for number in range(start, end + 1):
        if number % 5 == 0:
            yield number


def palindromes(start, end):
    for number in range(start, end + 1):
        text = str(number)
        if text == text[::-1]:
            yield number


if __name__ == "__main__":
    start = int(input("Введіть початок діапазону: "))
    end = int(input("Введіть кінець діапазону: "))

    print("Непарні числа:", list(odd_numbers(start, end)))
    print("Числа, кратні п'яти:", list(multiples_of_five(start, end)))
    print("Паліндроми:", list(palindromes(start, end)))
