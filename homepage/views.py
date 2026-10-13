from django.http import HttpResponse


def page(title, content):
    """Собрать HTML-страницу с общим каркасом."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{bootstrap}">
</head>
<body>
<nav class="nav">
<a class="nav-link" href="/">Главная</a>
<a class="nav-link" href="/students/">Студенты</a>
<a class="nav-link" href="/groups/">Группы</a>
<a class="nav-link" href="/topics/">Темы</a>
<a class="nav-link" href="/tasks/">Задачи</a>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница проекта."""
    content = """
<h1 class="display-4">Система совместной подготовки</h1>
<p class="lead">
Приложение для организации совместной подготовки студентов к занятиям.
</p>
<p>Основные разделы:</p>
<a href="/students/" class="btn btn-primary me-2">Студенты</a>
<a href="/groups/" class="btn btn-primary me-2">Группы</a>
<a href="/topics/" class="btn btn-secondary me-2">Темы</a>
<a href="/tasks/" class="btn btn-secondary">Задачи</a>
"""
    return HttpResponse(page("Система совместной подготовки", content))
