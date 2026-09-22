from models import Group, Student, Task, Topic
from models.tasks import calculate_group_readiness


def test_student_creation():
    student = Student(1, "Алипян Андраник", "test@example.com")
    assert student.id == 1
    assert student.name == "Алипян Андраник"


def test_student_from_data():
    data = {
        "id": 1,
        "name": "Алипян Андраник",
        "email": "test@example.com",
    }
    student = Student.from_data(data)
    assert student.email == "test@example.com"


def test_group_add_student():
    student = Student(1, "Алипян Андраник", "test@example.com")
    group = Group(1, "ЭФБО-18-24")
    group.add_student(student)
    assert group.has_student(1)


def test_task_complete():
    topic = Topic(1, "Основы Python", "2026-09-23")
    group = Group(1, "ЭФБО-18-24")
    task = Task(1, topic, group, "Сделать задачу")
    task.complete()
    assert task.done


def test_group_readiness():
    topic = Topic(1, "Основы Python", "2026-09-23")
    group = Group(1, "ЭФБО-18-24")
    task1 = Task(1, topic, group, "Задача 1")
    task2 = Task(2, topic, group, "Задача 2")
    task1.complete()
    tasks = [task1, task2]
    assert calculate_group_readiness(tasks, group.id) == 50
