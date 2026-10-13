from django.shortcuts import render

from models.students import find_student_by_id
from storage import load_students


def student_list(request):
    """Список студентов."""
    students = load_students()
    context = {"students": students}
    return render(request, "students/student_list.html", context)


def student_detail(request, student_id):
    """Страница отдельного студента."""
    students = load_students()
    student = find_student_by_id(students, student_id)
    context = {"student": student}
    return render(
        request,
        "students/student_detail.html",
        context,
        status=404 if student is None else 200,
    )
