from django.shortcuts import render

from models.tasks import find_task_by_id
from storage import load_groups, load_students, load_tasks, load_topics


def task_list(request):
    """Список задач."""
    students = load_students()
    topics = load_topics()
    groups = load_groups(students)
    tasks = load_tasks(topics, groups)
    context = {"tasks": tasks}
    return render(request, "tasks/task_list.html", context)


def task_detail(request, task_id):
    """Страница отдельной задачи."""
    students = load_students()
    topics = load_topics()
    groups = load_groups(students)
    tasks = load_tasks(topics, groups)
    task = find_task_by_id(tasks, task_id)
    context = {"task": task}
    return render(
        request,
        "tasks/task_detail.html",
        context,
        status=404 if task is None else 200,
    )
