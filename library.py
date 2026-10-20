from datetime import date


class Book:
    def __init__(self, title, author, year, pages):
        current_year = date.today().year
        if type(year) is not int or year < 1 or year > current_year:
            raise ValueError(f"Рік видання має бути цілим числом від 1 до {current_year}.")
        if type(pages) is not int or pages < 0:
            raise ValueError("Кількість сторінок має бути невід'ємним цілим числом.")
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages

    def __str__(self):
        return f"{self.title}, автор: {self.author}, рік: {self.year}, сторінок: {self.pages}"

    def __repr__(self):
        return (
            f"Book(title={self.title!r}, author={self.author!r}, "
            f"year={self.year}, pages={self.pages})"
        )

    def __len__(self):
        return self.pages

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Book):
            return self.pages < other.pages
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Book):
            return self.pages + other.pages
        return NotImplemented

    def __contains__(self, word):
        if not isinstance(word, str):
            raise TypeError("Для пошуку потрібно передати рядок.")
        return word.casefold() in self.title.casefold()

    def __bool__(self):
        return self.pages > 0


if __name__ == "__main__":
    book1 = Book("Вивчаємо Python", "Автор 1", 2021, 320)
    book2 = Book("Основи ООП", "Автор 2", 2020, 180)
    book3 = Book("Чернетка", "Автор 3", 2025, 0)
    books = [book1, book2, book3]

    print("Опис книги:", book1)
    print("Представлення для налагодження:", repr(book1))
    print("Кількість сторінок:", len(book1))
    print("Однакові книги:", book1 == Book("Вивчаємо Python", "Автор 1", 2025, 400))
    print("Друга книга має менше сторінок:", book2 < book1)
    print("Сумарна кількість сторінок:", book1 + book2)
    print("Слово Python є в назві:", "python" in book1)
    print("Перша книга непорожня:", bool(book1))
    print("Третя книга непорожня:", bool(book3))

    print("\nКниги за кількістю сторінок:")
    for book in sorted(books):
        print(book)

    print("Кількість книг:", len(books))
    print("Кількість непорожніх книг:", sum(bool(book) for book in books))
