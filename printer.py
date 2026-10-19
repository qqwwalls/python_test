from abc import ABC, abstractmethod


class Document(ABC):
    def __init__(self, title, text, ext, pages):
        if type(pages) is not int or pages <= 0:
            raise ValueError("Кількість сторінок має бути додатним цілим числом.")
        self.title = title
        self.text = text
        self.ext = ext
        self.pages = pages

    def __str__(self):
        return f"Документ: {self.title}{self.ext}, сторінок: {self.pages}"

    @abstractmethod
    def get_content(self):
        pass


class ExcellDocument(Document):
    def __init__(self, title, text, pages):
        super().__init__(title, text, ".xlsx", pages)

    def get_content(self):
        return f"Таблиця Excel:\n{self.text}"


class WordDocument(Document):
    def __init__(self, title, text, pages):
        super().__init__(title, text, ".docx", pages)

    def get_content(self):
        return f"Документ Word:\n{self.text}"


class HtmlDocument(Document):
    def __init__(self, title, text, pages):
        super().__init__(title, text, ".html", pages)

    def get_content(self):
        return f"HTML-документ:\n{self.text}"


class Printer:
    def __init__(self, model):
        self.model = model

    def __str__(self):
        return f"Принтер: {self.model}"

    def print_document(self, document):
        if not isinstance(document, Document):
            raise TypeError("Для друку потрібно передати документ.")
        print(self)
        print(document)
        print(document.get_content())
        print()


if __name__ == "__main__":
    printer = Printer("HP LaserJet")
    documents = [
        ExcellDocument("Звіт", "Товар\tКількість\nКнига\t10\nЗошит\t20", 2),
        WordDocument("Заява", "Прошу надати відпустку з 1 листопада.", 1),
        HtmlDocument("Сторінка", "<h1>Вітаємо!</h1><p>Це HTML-документ.</p>", 1),
    ]

    for document in documents:
        printer.print_document(document)
