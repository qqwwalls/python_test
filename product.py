import uuid
from math import isfinite


class Product:
    def __init__(self, title, image, price, rating, categories=None, reviews=0,
                 available=True, description=""):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Назва товару не може бути порожньою.")
        if not isinstance(image, str) or not image.strip():
            raise ValueError("Потрібно вказати зображення товару.")
        if type(price) not in (int, float) or not isfinite(price) or price < 0:
            raise ValueError("Ціна має бути невід'ємним числом.")
        if type(rating) not in (int, float) or not isfinite(rating) or not 0 <= rating <= 5:
            raise ValueError("Рейтинг має бути числом від 0 до 5.")
        self.id = str(uuid.uuid4())
        self.title = title.strip()
        self.image = image.strip()
        self.price = price
        self.rating = rating
        self.categories = categories if categories is not None else []
        self.reviews = reviews
        self.available = available
        self.description = description
