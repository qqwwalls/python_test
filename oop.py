class Person:
    def __init__(self, full_name="", birth_date="", phone="", city="", country="", address=""):
        self.__full_name = full_name
        self.__birth_date = birth_date
        self.__phone = phone
        self.__city = city
        self.__country = country
        self.__address = address

    def __str__(self):
        return (
            f"ПІБ: {self.__full_name}\n"
            f"Дата народження: {self.__birth_date}\n"
            f"Контактний телефон: {self.__phone}\n"
            f"Місто: {self.__city}\n"
            f"Країна: {self.__country}\n"
            f"Домашня адреса: {self.__address}"
        )

    def input_data(self):
        self.__full_name = input("Введіть ПІБ: ").strip()
        self.__birth_date = input("Введіть дату народження: ").strip()
        self.__phone = input("Введіть контактний телефон: ").strip()
        self.__city = input("Введіть місто: ").strip()
        self.__country = input("Введіть країну: ").strip()
        self.__address = input("Введіть домашню адресу: ").strip()

    def show_person(self):
        print(self)


if __name__ == "__main__":
    person = Person()
    person.input_data()
    person.show_person()
