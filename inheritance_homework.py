from decimal import Decimal, InvalidOperation


class Device:
    def __init__(self, model, manufacturer, power):
        self.model = model
        self.manufacturer = manufacturer
        self.power = power
        self.is_on = False

    def __str__(self):
        state = "увімкнено" if self.is_on else "вимкнено"
        return f"{self.manufacturer} {self.model}, потужність: {self.power} Вт, {state}"

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def _check_power(self):
        if not self.is_on:
            raise RuntimeError("Спочатку увімкніть пристрій.")


class CoffeeMachine(Device):
    def __init__(self, model, manufacturer, power, water_capacity):
        super().__init__(model, manufacturer, power)
        self.water_capacity = water_capacity

    def __str__(self):
        return f"Кавомашина: {super().__str__()}, резервуар: {self.water_capacity} л"

    def make_coffee(self, coffee_type="еспресо"):
        self._check_power()
        print(f"Кавомашина {self.model} готує {coffee_type}.")


class Blender(Device):
    def __init__(self, model, manufacturer, power, bowl_capacity):
        super().__init__(model, manufacturer, power)
        self.bowl_capacity = bowl_capacity

    def __str__(self):
        return f"Блендер: {super().__str__()}, об'єм чаші: {self.bowl_capacity} л"

    def blend(self, ingredients):
        self._check_power()
        print(f"Блендер {self.model} змішує: {ingredients}.")


class MeatGrinder(Device):
    def __init__(self, model, manufacturer, power, productivity):
        super().__init__(model, manufacturer, power)
        self.productivity = productivity

    def __str__(self):
        return f"М'ясорубка: {super().__str__()}, продуктивність: {self.productivity} кг/хв"

    def grind(self, product):
        self._check_power()
        print(f"М'ясорубка {self.model} подрібнює: {product}.")


class Ship:
    def __init__(self, name, country, displacement, speed):
        self.name = name
        self.country = country
        self.displacement = displacement
        self.speed = speed
        self.is_sailing = False

    def __str__(self):
        state = "у плаванні" if self.is_sailing else "на стоянці"
        return (
            f"{self.name}, країна: {self.country}, водотоннажність: {self.displacement} т, "
            f"швидкість: {self.speed} вузлів, {state}"
        )

    def sail(self):
        self.is_sailing = True

    def stop(self):
        self.is_sailing = False


class Frigate(Ship):
    def __init__(self, name, country, displacement, speed, missiles):
        super().__init__(name, country, displacement, speed)
        self.missiles = missiles

    def __str__(self):
        return f"Фрегат: {super().__str__()}, ракет: {self.missiles}"

    def patrol(self):
        self.sail()
        print(f"Фрегат {self.name} патрулює акваторію.")


class Destroyer(Ship):
    def __init__(self, name, country, displacement, speed, torpedoes):
        super().__init__(name, country, displacement, speed)
        self.torpedoes = torpedoes

    def __str__(self):
        return f"Есмінець: {super().__str__()}, торпед: {self.torpedoes}"

    def escort(self, ship):
        if not isinstance(ship, Ship):
            raise TypeError("Для супроводу потрібно передати корабель.")
        self.sail()
        print(f"Есмінець {self.name} супроводжує корабель {ship.name}.")


class Cruiser(Ship):
    def __init__(self, name, country, displacement, speed, guns):
        super().__init__(name, country, displacement, speed)
        self.guns = guns

    def __str__(self):
        return f"Крейсер: {super().__str__()}, гармат: {self.guns}"

    def lead_fleet(self):
        self.sail()
        print(f"Крейсер {self.name} очолює ескадру.")


class Money:
    def __init__(self, whole=0, cents=0, currency="UAH"):
        self.currency = currency
        self.set_amount(whole, cents)

    def __str__(self):
        return f"{self.whole}.{self.cents:02d} {self.currency}"

    def set_amount(self, whole, cents):
        if type(whole) is not int or whole < 0:
            raise ValueError("Ціла частина має бути невід'ємним цілим числом.")
        if type(cents) is not int or not 0 <= cents < 100:
            raise ValueError("Копійки мають бути цілим числом від 0 до 99.")
        self.whole = whole
        self.cents = cents

    def set_whole(self, whole):
        self.set_amount(whole, self.cents)

    def set_cents(self, cents):
        self.set_amount(self.whole, cents)

    def show_amount(self):
        print(self)


class Product(Money):
    def __init__(self, name, whole, cents=0, currency="UAH"):
        super().__init__(whole, cents, currency)
        self.name = name

    def __str__(self):
        return f"{self.name}: {super().__str__()}"

    def reduce_price(self, amount):
        try:
            amount = Decimal(str(amount))
        except InvalidOperation:
            raise ValueError("Сума зменшення має бути числом.") from None
        if not amount.is_finite() or amount < 0:
            raise ValueError("Сума зменшення має бути невід'ємним скінченним числом.")
        discount_cents = amount * 100
        if discount_cents != discount_cents.to_integral_value():
            raise ValueError("Сума може містити не більше двох знаків після крапки.")
        current_cents = self.whole * 100 + self.cents
        if discount_cents > current_cents:
            raise ValueError("Зменшення не може перевищувати ціну товару.")
        remaining_cents = current_cents - int(discount_cents)
        self.set_amount(remaining_cents // 100, remaining_cents % 100)


if __name__ == "__main__":
    print("Завдання 1. Пристрої")
    coffee_machine = CoffeeMachine("CM-1", "Home", 1200, 1.5)
    blender = Blender("BL-1", "Home", 800, 1.2)
    meat_grinder = MeatGrinder("MG-1", "Home", 1500, 2)
    devices = [coffee_machine, blender, meat_grinder]

    for device in devices:
        device.turn_on()
        print(device)
    coffee_machine.make_coffee()
    blender.blend("банан і молоко")
    meat_grinder.grind("м'ясо")
    for device in devices:
        device.turn_off()

    print("\nЗавдання 2. Кораблі")
    frigate = Frigate("Фрегат 1", "Країна 1", 3000, 28, 8)
    destroyer = Destroyer("Есмінець 1", "Країна 1", 8000, 32, 12)
    cruiser = Cruiser("Крейсер 1", "Країна 1", 12000, 30, 6)
    frigate.patrol()
    destroyer.escort(frigate)
    cruiser.lead_fleet()
    for ship in [frigate, destroyer, cruiser]:
        print(ship)
        ship.stop()

    print("\nЗавдання 3. Гроші та товари")
    money = Money(10, 50)
    money.show_amount()
    money.set_whole(20)
    money.set_cents(75)
    money.show_amount()

    product = Product("Книга", 150, 50)
    product.show_amount()
    product.reduce_price(20.25)
    product.show_amount()
