from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from .data import profile


class CvPageTests(SimpleTestCase):
    def test_home_route(self):
        self.assertEqual(reverse("index"), "/")
        self.assertEqual(resolve("/").view_name, "index")
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_template_inheritance_and_title(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "main/index.html")
        self.assertTemplateUsed(response, "main/layout.html")
        self.assertContains(response, "<title>Olena Test — персональне CV</title>")

    def test_personal_data_and_contacts(self):
        response = self.client.get("/")
        for value in ("Olena Test", "Одеса, Україна", "test@gmail.com",
                      "+380 000 000 000", "mailto:test@gmail.com", "tel:+380000000000"):
            with self.subTest(value=value):
                self.assertContains(response, value)
        self.assertContains(response, 'src="' + profile["photo_url"] + '"')
        self.assertTrue(profile["photo_url"].startswith("https://"))

    def test_all_resume_sections_and_navigation_targets(self):
        response = self.client.get("/")
        for section in ("about", "education", "skills", "projects", "contacts"):
            with self.subTest(section=section):
                self.assertContains(response, 'id="' + section + '"', count=1)
                self.assertContains(response, 'href="#' + section + '"')
        self.assertContains(response, "Особисті якості")
        self.assertContains(response, "Професійна мета")

    def test_education_and_language_levels(self):
        response = self.client.get("/")
        for value in ("Мечникова", "174", "2023–2027", "Англійська", "B2", "Німецька", "A2"):
            with self.subTest(value=value):
                self.assertContains(response, value)

    def test_bootstrap_cdn_and_components(self):
        response = self.client.get("/")
        self.assertContains(response, "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css")
        self.assertContains(response, "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js")
        for component in ("navbar", "container", "row g-4", "col-lg-9", "card project-card"):
            with self.subTest(component=component):
                self.assertContains(response, component)

    def test_three_projects_have_technologies_and_results(self):
        response = self.client.get("/")
        self.assertContains(response, 'class="card project-card h-100"', count=3)
        for project in response.context["projects"]:
            with self.subTest(project=project["title"]):
                self.assertContains(response, project["title"])
                self.assertContains(response, project["url"])
                self.assertTrue(project["technologies"])
                self.assertTrue(project["result"])

    def test_profile_data_is_rendered_dynamically_and_escaped(self):
        with patch("main.views.profile", {**profile, "name": "<b>Other Name</b>"}):
            response = self.client.get("/")
        self.assertContains(response, "&lt;b&gt;Other Name&lt;/b&gt;")
        self.assertNotContains(response, "<b>Other Name</b>")

    def test_static_files_are_available(self):
        for path in ("main/css/cv.css", "main/js/cv.js"):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))
