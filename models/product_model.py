from product import Product


class ProductModel:
    def __init__(self):
        self.products = [
            Product("Банани", "banana-bunch.png", 45, 4.8, ["tropical"], 124,
                    description="Стиглі, солодкі банани з ніжною м'якоттю."),
            Product("Яблука", "apple.png", 35, 4.7, ["apples"], 98,
                    description="Соковиті червоні яблука з приємною кислинкою."),
            Product("Апельсини", "orange-whole.png", 55, 4.9, ["citrus"], 156,
                    description="Ароматні апельсини для свіжого соку та фруктових салатів."),
            Product("Полуниця", "strawberry.png", 120, 4.8, ["berries"], 87,
                    description="Запашна полуниця з яскравим літнім смаком."),
            Product("Чорниця", "blueberry.png", 150, 4.9, ["berries"], 72,
                    description="Добірні темні ягоди до сніданків, десертів і випічки."),
            Product("Виноград", "grapes.png", 95, 4.6, ["berries"], 64,
                    description="Солодкий виноград у стиглих соковитих гронах."),
            Product("Ківі", "kiwi-cut.png", 80, 4.7, ["tropical"], 53,
                    description="Зелене ківі з освіжаючим кисло-солодким смаком."),
            Product("Манго", "mango.png", 140, 4.8, ["tropical", "stone"], 45,
                    description="Стигле манго з ніжною золотистою м'якоттю."),
        ]

    def get_all_products(self):
        return self.products

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def create_product(self, product):
        self.products.append(product)
        return product
