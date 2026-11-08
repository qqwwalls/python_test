from flask import Flask, abort, render_template, request

from models.product_model import ProductModel
from product import Product


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


@app.route("/product/<product_id>")
def product_by_id(product_id):
    product = product_model.get_product_by_id(product_id)
    if product is None:
        abort(404, description="Товар не знайдено.")
    return render_template("product.html", product=product,
                           product_data=[vars(product)])


@app.route("/product", methods=["POST"])
def create_product():
    data = request.get_json()
    if not isinstance(data, dict):
        return {"error": "Очікується JSON-об'єкт із даними товару."}, 400
    try:
        product = Product(data["title"], data["image"], data["price"], data["rating"])
    except KeyError as error:
        return {"error": f"Відсутнє поле: {error.args[0]}"}, 400
    except ValueError as error:
        return {"error": str(error)}, 400
    product_model.create_product(product)
    return vars(product), 201


if __name__ == "__main__":
    app.run(debug=True, port=5050)
