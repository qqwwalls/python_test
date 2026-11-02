from django.shortcuts import render


def home(request):
    technologies = [
        {
            'title': 'Python',
            'category': 'Мова програмування',
            'text': 'Зрозумілий синтаксис, робота з даними та автоматизація. Основа для перших програм і майбутніх вебпроєктів.',
            'image': 'main/images/python.png',
            'url': 'https://docs.python.org/3/',
            'theme': 'image-python',
        },
        {
            'title': 'Django',
            'category': 'Вебфреймворк',
            'text': 'Маршрути, шаблони та робота з базою даних. Усе необхідне, щоб перетворити ідею на повноцінний вебсайт.',
            'image': 'main/images/django.png',
            'url': 'https://docs.djangoproject.com/en/6.1/',
            'theme': 'image-django',
        },
        {
            'title': 'Flask',
            'category': 'Мікрофреймворк',
            'text': 'Невеликий старт для власного застосунку. Створюй сторінки, описуй маршрути та розширюй проєкт у своєму темпі.',
            'image': 'main/images/flask.svg',
            'url': 'https://flask.palletsprojects.com/en/stable/',
            'theme': 'image-flask',
        },
    ]
    return render(request, 'main/index.html', {'technologies': technologies})


def about(request):
    return render(request, 'main/about.html')

