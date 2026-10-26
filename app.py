from flask import Flask, render_template


app = Flask(__name__)


categories = [
    {"id": "all", "name": "Всі фрукти", "image": "apple.png"},
    {"id": "berries", "name": "Ягоди", "image": "strawberry.png"},
    {"id": "citrus", "name": "Цитрусові", "image": "orange-whole.png"},
    {"id": "stone", "name": "Кісточкові", "image": "mango.png"},
    {"id": "tropical", "name": "Тропічні", "image": "banana-bunch.png"},
    {"id": "apples", "name": "Яблука та груші", "image": "apple.png"},
]

products = [
    {"id": 1, "name": "Банани", "price": 45, "image": "banana-bunch.png", "categories": ["tropical"],
     "rating": 4.8, "reviews": 124, "available": True, "description": "Стиглі, солодкі банани з ніжною м'якоттю."},
    {"id": 2, "name": "Яблука", "price": 35, "image": "apple.png", "categories": ["apples"],
     "rating": 4.7, "reviews": 98, "available": True, "description": "Соковиті червоні яблука з приємною кислинкою."},
    {"id": 3, "name": "Апельсини", "price": 55, "image": "orange-whole.png", "categories": ["citrus"],
     "rating": 4.9, "reviews": 156, "available": True, "description": "Ароматні апельсини для свіжого соку та фруктових салатів."},
    {"id": 4, "name": "Полуниця", "price": 120, "image": "strawberry.png", "categories": ["berries"],
     "rating": 4.8, "reviews": 87, "available": True, "description": "Запашна полуниця з яскравим літнім смаком."},
    {"id": 5, "name": "Чорниця", "price": 150, "image": "blueberry.png", "categories": ["berries"],
     "rating": 4.9, "reviews": 72, "available": True, "description": "Добірні темні ягоди до сніданків, десертів і випічки."},
    {"id": 6, "name": "Виноград", "price": 95, "image": "grapes.png", "categories": ["berries"],
     "rating": 4.6, "reviews": 64, "available": True, "description": "Солодкий виноград у стиглих соковитих гронах."},
    {"id": 7, "name": "Ківі", "price": 80, "image": "kiwi-cut.png", "categories": ["tropical"],
     "rating": 4.7, "reviews": 53, "available": True, "description": "Зелене ківі з освіжаючим кисло-солодким смаком."},
    {"id": 8, "name": "Манго", "price": 140, "image": "mango.png", "categories": ["tropical", "stone"],
     "rating": 4.8, "reviews": 45, "available": True, "description": "Стигле манго з ніжною золотистою м'якоттю."},
]


@app.route("/index")
@app.route("/")
def home():
    category_data = []
    for category in categories:
        count = sum(category["id"] in product["categories"] for product in products)
        if category["id"] == "all":
            count = len(products)
        category_data.append({**category, "count": count})
    return render_template("index.html", categories=category_data, products=products)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
