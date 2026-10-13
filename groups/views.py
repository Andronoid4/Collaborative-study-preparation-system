from django.shortcuts import render

from models.groups import find_group_by_id
from models.tasks import calculate_group_readiness
from storage import load_groups, load_students, load_tasks, load_topics


def group_list(request):
    """Список групп."""
    students = load_students()
    groups = load_groups(students)
    context = {"groups": groups}
    return render(request, "groups/group_list.html", context)


def group_detail(request, group_id):
    """Страница отдельной группы."""
    students = load_students()
    groups = load_groups(students)
    topics = load_topics()
    tasks = load_tasks(topics, groups)
    group = find_group_by_id(groups, group_id)
    readiness = calculate_group_readiness(tasks, group_id)
    context = {"group": group, "readiness": readiness}
    return render(
        request,
        "groups/group_detail.html",
        context,
        status=404 if group is None else 200,
    )
