import uuid


class Product:
    def __init__(self, title, image, price, rating, categories=None, reviews=0,
                 available=True, description=""):
        self.id = str(uuid.uuid4())
        self.title = title
        self.image = image
        self.price = price
        self.rating = rating
        self.categories = categories if categories is not None else []
        self.reviews = reviews
        self.available = available
        self.description = description
