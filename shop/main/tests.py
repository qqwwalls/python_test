from django.contrib.staticfiles import finders
from django.test import SimpleTestCase


class StaticFilesTests(SimpleTestCase):
    def test_bootstrap_files_are_found(self):
        for path in ('css/bootstrap.min.css', 'js/bootstrap.bundle.min.js',
                     'main/images/django.png'):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))

    def test_pages_use_local_bootstrap(self):
        for path in ('/', '/about'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, '/static/css/bootstrap.min.css')
                self.assertContains(response, '/static/js/bootstrap.bundle.min.js')
                self.assertNotContains(response, 'cdn.jsdelivr.net/npm/bootstrap')

    def test_home_renders_django_card(self):
        response = self.client.get('/')
        self.assertContains(response, 'src="/static/main/images/django.png"')
        self.assertContains(response, '<h4 class="card-title">Django</h4>')
        self.assertContains(response, 'href="https://www.djangoproject.com/"')
        self.assertNotContains(response, 'btn-solid')
