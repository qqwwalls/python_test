from flask import Flask, render_template

from models.product_model import ProductModel


app = Flask(__name__)
product_model = ProductModel()


categories = [
    {"id": "all", "name": "Всі фрукти", "image": "apple.png"},
    {"id": "berries", "name": "Ягоди", "image": "strawberry.png"},
    {"id": "citrus", "name": "Цитрусові", "image": "orange-whole.png"},
    {"id": "stone", "name": "Кісточкові", "image": "mango.png"},
    {"id": "tropical", "name": "Тропічні", "image": "banana-bunch.png"},
    {"id": "apples", "name": "Яблука та груші", "image": "apple.png"},
]


@app.route("/index")
@app.route("/")
def home():
    products = product_model.get_all_products()
    category_data = []
    for category in categories:
        count = 0
        for product in products:
            if category["id"] == "all" or category["id"] in product.categories:
                count += 1
        category_data.append({**category, "count": count})
    product_data = []
    for product in products:
        product_data.append(vars(product))
    return render_template("index.html", categories=category_data,
                           products=products, product_data=product_data)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
