import unittest
import uuid
from unittest.mock import patch

from app import app
from models.product_model import ProductModel
from product import Product


class ProductModelTests(unittest.TestCase):
    def setUp(self):
        self.model = ProductModel()
        model_patch = patch("app.product_model", self.model)
        model_patch.start()
        self.addCleanup(model_patch.stop)
        self.client = app.test_client()

    def test_product_fields_and_id(self):
        first = Product("Товар", "apple.png", 35, 4.7)
        second = Product("Товар", "apple.png", 35, 4.7)
        self.assertEqual((first.title, first.image, first.price, first.rating),
                         ("Товар", "apple.png", 35, 4.7))
        self.assertEqual(uuid.UUID(first.id).version, 4)
        self.assertNotEqual(first.id, second.id)

    def test_get_all_products(self):
        products = self.model.get_all_products()
        self.assertEqual(len(products), 8)
        self.assertTrue(all(isinstance(product, Product) for product in products))

    def test_get_product_by_id(self):
        product = self.model.get_all_products()[0]
        self.assertIs(self.model.get_product_by_id(product.id), product)
        self.assertIsNone(self.model.get_product_by_id(str(uuid.uuid4())))
        self.assertIsNone(self.model.get_product_by_id(None))

    def test_create_product_in_model(self):
        product = Product("Новий товар", "apple.png", 25, 4.5)
        self.assertIs(self.model.create_product(product), product)
        self.assertEqual(len(self.model.get_all_products()), 9)
        self.assertIs(self.model.get_product_by_id(product.id), product)

    def test_home_gets_products_from_model(self):
        product = Product("Товар із моделі", "apple.png", 25, 4.5)
        with patch.object(self.model, "get_all_products", return_value=[product]) as get_all:
            response = self.client.get("/")
        get_all.assert_called_once_with()
        self.assertEqual(response.status_code, 200)
        self.assertIn(product.title, response.get_data(as_text=True))

    def test_catalog_links_to_product_pages(self):
        for path in ("/", "/index"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                for product in self.model.get_all_products():
                    self.assertEqual(html.count(f'href="/product/{product.id}"'), 2)

    def test_product_page_uses_model_lookup(self):
        product = self.model.get_all_products()[0]
        with patch.object(self.model, "get_product_by_id", return_value=product) as get_one:
            response = self.client.get("/product/selected-id")
        get_one.assert_called_once_with("selected-id")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for value in (product.title, str(product.price), str(product.rating), product.image):
            self.assertIn(value, html)

    def test_missing_product_returns_404(self):
        self.assertEqual(self.client.get("/product/missing").status_code, 404)

    def test_post_creates_product_visible_on_both_pages(self):
        data = {"title": "Тестовий фрукт", "image": "apple.png", "price": 29, "rating": 4.6}
        response = self.client.post("/product", json=data)
        self.assertEqual(response.status_code, 201)
        created = response.get_json()
        product = self.model.get_product_by_id(created["id"])
        self.assertIsNotNone(product)
        for key, value in data.items():
            self.assertEqual(getattr(product, key), value)
        for path in ("/", "/product/" + product.id):
            with self.subTest(path=path):
                page = self.client.get(path)
                self.assertEqual(page.status_code, 200)
                self.assertIn(data["title"], page.get_data(as_text=True))

    def test_invalid_product_data_is_rejected(self):
        valid = {"title": "Товар", "image": "apple.png", "price": 20, "rating": 4}
        invalid = [[], {}, {**valid, "title": " "}, {**valid, "image": None},
                   {**valid, "price": -1}, {**valid, "price": True},
                   {**valid, "price": float("inf")}, {**valid, "rating": 6},
                   {**valid, "rating": "4"}]
        for data in invalid:
            with self.subTest(data=data):
                response = self.client.post("/product", json=data)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())
        self.assertEqual(len(self.model.get_all_products()), 8)


if __name__ == "__main__":
    unittest.main()
