import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm


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


@require_http_methods(["GET", "POST"])
def registration(request):
    if request.method == "POST":
        if request.content_type != "application/json":
            return JsonResponse({"error": "Потрібно надіслати дані у форматі JSON."}, status=415)
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"error": "Некоректний JSON."}, status=400)
        if not isinstance(data, dict):
            return JsonResponse({"error": "Очікується JSON-об'єкт."}, status=400)
        form = RegistrationForm(data)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        log_data = form.cleaned_data.copy()
        for field in ("password", "password_confirm"):
            log_data[field] = "********"
        print(json.dumps(log_data, ensure_ascii=False), flush=True)
        return JsonResponse({"message": "Дані реєстрації отримано."})
    return render(request, "main/registration.html", {"form": RegistrationForm()})
