class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def is_new(self):
        return self.year >= 2020


class PositiveNumber:
    def __new__(cls, value):
        if type(value) is not int:
            raise ValueError("Число має бути цілим.")
        if value < 0:
            print("Від'ємне число заборонено")
            return None
        return super().__new__(cls)

    def __init__(self, value):
        self.value = value


if __name__ == "__main__":
    book1 = Book("Книга 1", "Автор 1", 2019)
    book2 = Book("Книга 2", "Автор 2", 2020)
    book3 = Book("Книга 3", "Автор 3", 2025)

    print(book1.is_new())
    print(book2.is_new())
    print(book3.is_new())

    a = PositiveNumber(10)
    b = PositiveNumber(-5)

    print(a.value)
    print(b)
