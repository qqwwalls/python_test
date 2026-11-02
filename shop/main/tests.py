from django.contrib.staticfiles import finders
from django.test import SimpleTestCase


class StaticFilesTests(SimpleTestCase):
    def test_bootstrap_files_are_found(self):
        for path in ('css/bootstrap.min.css', 'js/bootstrap.bundle.min.js'):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))

    def test_pages_use_local_bootstrap(self):
        for path in ('/', '/about'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, '/static/css/bootstrap.min.css')
                self.assertContains(response, '/static/js/bootstrap.bundle.min.js')
                self.assertNotContains(response, 'cdn.jsdelivr.net/npm/bootstrap')
