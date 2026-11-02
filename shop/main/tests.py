from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import SimpleTestCase


class StaticFilesTests(SimpleTestCase):
    def test_bootstrap_files_are_found(self):
        for path in ('css/bootstrap.min.css', 'js/bootstrap.bundle.min.js',
                     'main/css/site.css', 'main/images/python.png',
                     'main/images/django.png', 'main/images/flask.svg'):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))

    def test_pages_use_local_bootstrap(self):
        for path in ('/', '/about'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, '/static/css/bootstrap.min.css')
                self.assertContains(response, '/static/js/bootstrap.bundle.min.js')
                self.assertNotContains(response, 'cdn.jsdelivr.net/npm/bootstrap')

    def test_home_renders_three_technology_cards(self):
        response = self.client.get('/')
        self.assertContains(response, 'class="card technology-card h-100"', count=3)
        for number, technology in enumerate(response.context['technologies'], start=1):
            with self.subTest(title=technology['title']):
                self.assertContains(response, technology['title'])
                self.assertContains(response, '/static/' + technology['image'])
                self.assertContains(response, 'href="' + technology['url'] + '"')
                self.assertContains(response, f'{number}. {technology["category"]}')
        self.assertContains(response, 'href="#technologies"')
        self.assertNotContains(response, 'btn-solid')

    def test_empty_technology_list(self):
        html = render_to_string('main/index.html', {'technologies': []})
        self.assertIn('Немає даних', html)
        self.assertNotIn('class="card technology-card h-100"', html)

    def test_cards_follow_template_data(self):
        technologies = [{
            'title': 'Test framework',
            'category': 'Test category',
            'text': 'Test description',
            'image': 'main/images/django.png',
            'url': 'https://example.com/docs/',
            'theme': 'image-django',
        }]
        html = render_to_string('main/index.html', {'technologies': technologies})
        self.assertEqual(html.count('class="card technology-card h-100"'), 1)
        self.assertIn('Test framework', html)
        self.assertIn('1. Test category', html)
        self.assertIn('https://example.com/docs/', html)
        self.assertNotIn('Немає даних', html)

    def test_about_has_its_own_content(self):
        response = self.client.get('/about')
        self.assertContains(response, 'Про Python Web Lab')
        self.assertContains(response, 'href="/#technologies"')
        self.assertNotContains(response, 'Розділ 1')

    def test_active_navigation_matches_page(self):
        for path, label in (('/', 'Головна'), ('/about', 'Про проєкт')):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, 'aria-current="page">' + label)
