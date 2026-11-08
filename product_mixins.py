import json


class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class JsonMixin:
    def to_json(self):
        return json.dumps({"name": self.name, "price": self.price}, ensure_ascii=False)


class DiscountMixin:
    def apply_discount(self, percent):
        if not 0 <= percent <= 100:
            raise ValueError("Знижка має бути від 0 до 100 відсотків.")
        self.price -= self.price * percent / 100
        return self.price


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class ProductManager(Product, LoggingMixin, JsonMixin, DiscountMixin):
    pass


if __name__ == "__main__":
    product = ProductManager("Навушники", 1000)
    product.log(f"Створено товар: {product.name}")
    print(f"Початкова ціна: {product.price:g} грн")

    discounted_price = product.apply_discount(15)
    print(f"Ціна після знижки 15%: {discounted_price:g} грн")
    print("JSON:", product.to_json())

    print("MRO:", ProductManager.mro())
    print(
        "Методи шукаються у порядку ProductManager -> Product -> "
        "LoggingMixin -> JsonMixin -> DiscountMixin -> object."
    )
    print(
        "Батьківські класи незалежні та мають спільного предка object, "
        "тому алгоритм C3 зберігає їхній порядок у списку успадкування, "
        "а object стоїть останнім."
    )
