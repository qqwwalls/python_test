class Car:
    def __init__(self, model="", year=0, manufacturer="", engine_volume=0.0, color="", price=0.0):
        self.__model = model
        self.__year = year
        self.__manufacturer = manufacturer
        self.__engine_volume = engine_volume
        self.__color = color
        self.price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        self.__price = new_price

    def __str__(self):
        return (
            f"Модель: {self.__model}\n"
            f"Рік випуску: {self.__year}\n"
            f"Виробник: {self.__manufacturer}\n"
            f"Об'єм двигуна: {self.__engine_volume} л\n"
            f"Колір: {self.__color}\n"
            f"Ціна: {self.price:.2f}"
        )

    def input_data(self):
        self.__model = input("Введіть модель автомобіля: ").strip()
        self.__year = int(input("Введіть рік випуску: "))
        self.__manufacturer = input("Введіть виробника: ").strip()
        self.__engine_volume = float(input("Введіть об'єм двигуна в літрах: "))
        self.__color = input("Введіть колір автомобіля: ").strip()
        self.price = float(input("Введіть ціну автомобіля: "))

    def show_data(self):
        print(self)


class Book:
    def __init__(self, title="", year=0, publisher="", genre="", author="", price=0.0):
        self.__title = title
        self.__year = year
        self.__publisher = publisher
        self.__genre = genre
        self.__author = author
        self.price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError("Ціна не може бути від'ємною.")
        self.__price = new_price

    def __str__(self):
        return (
            f"Назва книги: {self.__title}\n"
            f"Рік видання: {self.__year}\n"
            f"Видавець: {self.__publisher}\n"
            f"Жанр: {self.__genre}\n"
            f"Автор: {self.__author}\n"
            f"Ціна: {self.price:.2f}"
        )

    def input_data(self):
        self.__title = input("Введіть назву книги: ").strip()
        self.__year = int(input("Введіть рік видання: "))
        self.__publisher = input("Введіть видавця: ").strip()
        self.__genre = input("Введіть жанр: ").strip()
        self.__author = input("Введіть автора: ").strip()
        self.price = float(input("Введіть ціну книги: "))

    def show_data(self):
        print(self)


class Stadium:
    def __init__(self, name="", opening_date="", country="", city="", capacity=0):
        self.__name = name
        self.__opening_date = opening_date
        self.__country = country
        self.__city = city
        self.capacity = capacity

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, new_capacity):
        if type(new_capacity) is not int or new_capacity < 0:
            raise ValueError("Місткість має бути невід'ємним цілим числом.")
        self.__capacity = new_capacity

    def __str__(self):
        return (
            f"Назва стадіону: {self.__name}\n"
            f"Дата відкриття: {self.__opening_date}\n"
            f"Країна: {self.__country}\n"
            f"Місто: {self.__city}\n"
            f"Місткість: {self.capacity}"
        )

    def input_data(self):
        self.__name = input("Введіть назву стадіону: ").strip()
        self.__opening_date = input("Введіть дату відкриття (дд.мм.рррр): ").strip()
        self.__country = input("Введіть країну: ").strip()
        self.__city = input("Введіть місто: ").strip()
        self.capacity = int(input("Введіть місткість стадіону: "))

    def show_data(self):
        print(self)


def main():
    while True:
        print("\n1. Автомобіль")
        print("2. Книга")
        print("3. Стадіон")
        print("0. Вихід")
        choice = input("Виберіть завдання: ").strip()

        if choice == "0":
            break
        if choice == "1":
            item = Car()
        elif choice == "2":
            item = Book()
        elif choice == "3":
            item = Stadium()
        else:
            print("Невірний вибір.")
            continue

        try:
            item.input_data()
            item.show_data()
        except ValueError as error:
            print(f"Помилка введення: {error}")


if __name__ == "__main__":
    main()
