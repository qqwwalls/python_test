class Person:
    def __init__(self, full_name="Невідомо", birth_date="", phone="", city="", country="", address=""):
        self.full_name = full_name
        self.__birth_date = birth_date
        self.__phone = phone
        self.__city = city
        self.__country = country
        self.__address = address

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, new_full_name):
        new_full_name = new_full_name.strip()
        if not new_full_name:
            raise ValueError("ПІБ не може бути порожнім.")
        self.__full_name = new_full_name

    def __str__(self):
        return (
            f"ПІБ: {self.full_name}\n"
            f"Дата народження: {self.__birth_date}\n"
            f"Контактний телефон: {self.__phone}\n"
            f"Місто: {self.__city}\n"
            f"Країна: {self.__country}\n"
            f"Домашня адреса: {self.__address}"
        )

    def input_data(self):
        self.full_name = input("Введіть ПІБ: ")
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
