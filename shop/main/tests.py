import json
from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import Client, SimpleTestCase
from django.urls import reverse


class StaticFilesTests(SimpleTestCase):
    def test_bootstrap_files_are_found(self):
        for path in ('main/css/bootstrap.min.css', 'main/js/bootstrap.bundle.min.js',
                     'main/css/site.css', 'main/images/python.png',
                     'main/images/django.png', 'main/images/flask.svg',
                     'main/js/registration.js'):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))

    def test_pages_use_local_bootstrap(self):
        for path in ('/', '/about', '/registration/'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, '/static/main/css/bootstrap.min.css')
                self.assertContains(response, '/static/main/js/bootstrap.bundle.min.js')
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
        for path, label in (('/', 'Головна'), ('/about', 'Про проєкт'),
                            ('/registration/', 'Реєстрація')):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, 'aria-current="page">' + label)


class RegistrationTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse('registration')
        self.data = {
            'name': 'Тестовий користувач',
            'email': 'practice@example.com',
            'password': 'PracticeDemo123!',
            'password_confirm': 'PracticeDemo123!',
        }

    def test_registration_page_and_menu(self):
        home = self.client.get('/')
        self.assertContains(home, 'href="/registration/"')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main/layout.html')
        self.assertTemplateUsed(response, 'main/registration.html')
        for name in ('name', 'email', 'password', 'password_confirm', 'csrfmiddlewaretoken'):
            self.assertContains(response, f'name="{name}"')
        self.assertContains(response, '/static/main/js/registration.js')

    def test_json_is_received_and_printed_without_passwords(self):
        with patch('builtins.print') as output:
            response = self.client.post(self.url, self.data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Дані реєстрації отримано.')
        output.assert_called_once()
        printed = output.call_args.args[0]
        logged = json.loads(printed)
        self.assertEqual(logged['name'], self.data['name'])
        self.assertEqual(logged['email'], self.data['email'])
        self.assertEqual(logged['password'], '********')
        self.assertEqual(logged['password_confirm'], '********')
        self.assertNotIn(self.data['password'], printed)
        self.assertTrue(output.call_args.kwargs['flush'])

    def test_invalid_fields_are_not_logged(self):
        invalid = [{}, {**self.data, 'email': 'invalid'},
                   {**self.data, 'password_confirm': 'different'},
                   {**self.data, 'password': 'short', 'password_confirm': 'short'}]
        with patch('builtins.print') as output:
            for data in invalid:
                with self.subTest(data=data):
                    response = self.client.post(self.url, data, content_type='application/json')
                    self.assertEqual(response.status_code, 400)
                    self.assertIn('errors', response.json())
        output.assert_not_called()

    def test_malformed_json_is_rejected(self):
        for body in ('{', b'\xff'):
            with self.subTest(body=body):
                response = self.client.post(self.url, body, content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', response.json())

    def test_json_must_be_an_object(self):
        response = self.client.post(self.url, [], content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_non_json_request_is_rejected(self):
        self.assertEqual(self.client.post(self.url, self.data).status_code, 415)

    def test_unsupported_method(self):
        self.assertEqual(self.client.put(self.url).status_code, 405)

    def test_csrf_is_required_and_valid_token_works(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.url)
        response = client.post(self.url, self.data, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        with patch('builtins.print'):
            response = client.post(
                self.url, self.data, content_type='application/json',
                HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value,
            )
        self.assertEqual(response.status_code, 200)
