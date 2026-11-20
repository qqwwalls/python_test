from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .forms import CardForm
from .models import Card


def make_image(format="PNG", size=(640, 360), name=None, total_bytes=None):
    content = BytesIO()
    Image.new("RGB", size, color="#306998").save(content, format=format)
    data = content.getvalue()
    if total_bytes is not None:
        data += b"\0" * (total_bytes - len(data))
    return SimpleUploadedFile(name or f"picture.{format.lower()}", data, content_type=f"image/{format.lower()}")


class CardFormTests(SimpleTestCase):
    def form(self, data=None, image=None):
        fields = {"title": "Мій проєкт", "description": "Навчальний проєкт з формами та базою даних."}
        if data is not None:
            fields.update(data)
        return CardForm(fields, {"image": image if image is not None else make_image()})

    def test_supported_image_formats(self):
        for format in ("PNG", "JPEG", "WEBP"):
            with self.subTest(format=format):
                form = self.form(image=make_image(format=format))
                self.assertTrue(form.is_valid(), form.errors)

    def test_all_fields_are_required_with_custom_messages(self):
        form = CardForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["Введіть назву картки."])
        self.assertEqual(form.errors["description"], ["Додайте опис картки."])
        self.assertEqual(form.errors["image"], ["Додайте зображення для картки."])

    def test_text_length_limits(self):
        cases = [
            ({"title": "АБ"}, "title", "Назва має містити щонайменше 3 символи."),
            ({"title": "А" * 81}, "title", "Скоротіть назву до 80 символів."),
            ({"description": "Коротко"}, "description", "Розкажіть трохи більше: опис має містити щонайменше 20 символів."),
            ({"description": "А" * 501}, "description", "Скоротіть опис до 500 символів."),
            ({"title": "   "}, "title", "Введіть назву картки."),
        ]
        for data, field, message in cases:
            with self.subTest(field=field, length=len(next(iter(data.values())))):
                form = self.form(data)
                self.assertFalse(form.is_valid())
                self.assertEqual(form.errors[field], [message])

    def test_text_boundary_values_are_valid(self):
        for title_length, description_length in ((3, 20), (80, 500)):
            with self.subTest(title_length=title_length):
                form = self.form({"title": "А" * title_length, "description": "Б" * description_length})
                self.assertTrue(form.is_valid(), form.errors)

    def test_fake_and_corrupt_images_are_rejected(self):
        image = SimpleUploadedFile("picture.png", b"not an image", content_type="image/png")
        form = self.form(image=image)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["image"], ["Цей файл не є справним зображенням. Оберіть JPG, PNG або WebP."])

    def test_unsupported_format_and_extension_are_rejected(self):
        for image in (make_image(format="GIF"), make_image(name="picture.txt")):
            with self.subTest(name=image.name):
                form = self.form(image=image)
                self.assertFalse(form.is_valid())
                self.assertEqual(form.errors["image"], ["Дозволені лише зображення JPG, PNG або WebP."])

    def test_image_size_limit(self):
        for size, valid in ((2 * 1024 * 1024, True), (2 * 1024 * 1024 + 1, False)):
            with self.subTest(bytes=size):
                form = self.form(image=make_image(total_bytes=size))
                self.assertEqual(form.is_valid(), valid, form.errors)
                if not valid:
                    self.assertEqual(form.errors["image"], ["Зображення завелике. Максимальний розмір — 2 МБ."])

    def test_image_dimensions(self):
        for size, valid in (((320, 180), True), ((4096, 4096), True),
                            ((319, 180), False), ((320, 179), False),
                            ((4097, 180), False), ((320, 4097), False)):
            with self.subTest(size=size):
                form = self.form(image=make_image(size=size))
                self.assertEqual(form.is_valid(), valid, form.errors)
                if not valid:
                    self.assertEqual(form.errors.as_data()["image"][0].code, "dimensions")


class CardViewsTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        settings = override_settings(MEDIA_ROOT=self.media.name)
        settings.enable()
        self.addCleanup(settings.disable)
        self.url = reverse("create_card")
        self.data = {"title": "Мій проєкт", "description": "Навчальний проєкт з формами та базою даних."}

    def test_form_is_accessible_from_catalogue_and_menu(self):
        home = self.client.get(reverse("home"))
        self.assertContains(home, 'href="/cards/"')
        catalogue = self.client.get(reverse("cards"))
        self.assertContains(catalogue, "Тут будуть ваші картки")
        self.assertContains(catalogue, f'href="{self.url}"')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "main/create_card.html")
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, "novalidate")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_valid_submission_saves_image_and_redirects(self):
        response = self.client.post(self.url, {**self.data, "image": make_image()}, follow=True)
        self.assertRedirects(response, reverse("cards"))
        card = Card.objects.get()
        self.assertEqual(card.title, self.data["title"])
        self.assertEqual(card.description, self.data["description"])
        self.assertIsNotNone(card.created_at)
        self.assertTrue(Path(card.image.path).is_file())
        self.assertRegex(card.image.name, r"^cards/[0-9a-f]{32}\.png$")
        self.assertContains(response, card.image.url)
        self.assertContains(response, "успішно додано")
        self.client.get(reverse("cards"))
        self.assertEqual(Card.objects.count(), 1)

    def test_invalid_submission_keeps_text_and_does_not_save(self):
        response = self.client.post(self.url, {**self.data, "image": make_image(size=(100, 100))})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Картку ще не збережено.")
        self.assertContains(response, "Оберіть зображення від 320 × 180 до 4096 × 4096 пікселів.")
        self.assertContains(response, 'aria-invalid="true"')
        self.assertEqual(response.context["form"]["title"].value(), self.data["title"])
        self.assertEqual(response.context["form"]["description"].value(), self.data["description"])
        self.assertFalse(Card.objects.exists())
        self.assertEqual(list(Path(self.media.name).iterdir()), [])

    def test_empty_submission_shows_custom_errors(self):
        response = self.client.post(self.url, {})
        for message in ("Введіть назву картки.", "Додайте опис картки.", "Додайте зображення для картки."):
            self.assertContains(response, message)
        self.assertFalse(Card.objects.exists())

    def test_catalogue_escapes_user_text_and_shows_newest_first(self):
        self.client.post(self.url, {**self.data, "image": make_image()})
        title = "<script>alert(1)</script>"
        self.client.post(self.url, {**self.data, "title": title, "image": make_image()})
        response = self.client.get(reverse("cards"))
        self.assertNotContains(response, title)
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertEqual(list(response.context["cards"].values_list("title", flat=True)), [title, self.data["title"]])

    def test_csrf_is_required(self):
        response = Client(enforce_csrf_checks=True).post(self.url, self.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Card.objects.exists())

    def test_unsupported_method_is_rejected(self):
        self.assertEqual(self.client.put(self.url).status_code, 405)
