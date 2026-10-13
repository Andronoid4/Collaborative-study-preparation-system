from django.shortcuts import render


def index(request):
    """Главная страница проекта."""
    return render(request, "homepage/index.html")
