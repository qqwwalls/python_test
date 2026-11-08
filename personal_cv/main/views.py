from django.shortcuts import render

from .data import education, languages, profile, projects, skill_groups


def index(request):
    return render(request, "main/index.html", {
        "profile": profile,
        "education": education,
        "skill_groups": skill_groups,
        "languages": languages,
        "projects": projects,
    })
