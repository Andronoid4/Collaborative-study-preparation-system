cd "/Users/andranik/Учеба/Collaborative-study-preparation-system"

mkdir -p data models tests

cat << 'EOF' > README.md
# Система совместной подготовки к занятиям

Консольное приложение для организации совместной подготовки студентов.

## Возможности
- добавление студентов;
- создание групп;
- добавление студентов в группы;
- создание тем занятий;
- создание задач для групп;
- отметка выполнения задач;
- отчет готовности группы.

## Структура проекта
- main.py - точка запуска;
- storage.py - загрузка и сохранение данных в JSON;
- utils.py - безопасный ввод данных;
- models/ - классы и функции предметной области;
- data/ - файлы данных;
- tests/ - автоматические тесты.

## Запуск программы
python main.py

## Запуск тестов
pytest -v

## Проверка качества кода
flake8
EOF

cat << 'EOF' > requirements.txt
pytest>=8.0
flake8>=7.0
EOF

cat << 'EOF' > .gitignore
venv/
__pycache__/
*.pyc
.pytest_cache/
.vscode/
.idea/
EOF

cat << 'EOF' > .flake8
[flake8]
exclude =
    venv,
    .venv,
    __pycache__,
    .pytest_cache
max-line-length = 79
EOF

cat << 'EOF' > conftest.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
EOF

cat << 'EOF' > utils.py
def input_int(prompt: str) -> int:
    """Запросить целое число."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Введите целое число.")


def input_non_empty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не может быть пустым.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt).strip()
        parts = value.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            return value
        print("Введите дату в формате ГГГГ-ММ-ДД.")
EOF

cat << 'EOF' > models/__init__.py
from models.groups import Group
from models.students import Student
from models.tasks import Task
from models.topics import Topic

__all__ = ["Group", "Student", "Task", "Topic"]
EOF

cat << 'EOF' > models/students.py
from typing import Optional


class Student:
    """Студент."""

    def __init__(self, student_id: int, name: str, email: str) -> None:
        self.id = student_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

    @classmethod
    def from_data(cls, data: dict) -> "Student":
        """Создать студента из словаря."""
        return cls(data["id"], data["name"], data["email"])


def find_student_by_id(
    students: list[Student],
    student_id: int,
) -> Optional[Student]:
    """Найти студента по ID."""
    for student in students:
        if student.id == student_id:
            return student
    return None
EOF

cat << 'EOF' > models/groups.py
from typing import Optional

from models.students import Student


class Group:
    """Группа студентов."""

    def __init__(self, group_id: int, name: str) -> None:
        self.id = group_id
        self.name = name
        self.students: list[Student] = []

    def add_student(self, student: Student) -> None:
        """Добавить студента в группу."""
        if not self.has_student(student.id):
            self.students.append(student)

    def has_student(self, student_id: int) -> bool:
        """Проверить, есть ли студент в группе."""
        for student in self.students:
            if student.id == student_id:
                return True
        return False

    def __str__(self) -> str:
        return f"{self.name}, студентов: {len(self.students)}"


def find_group_by_id(
    groups: list[Group],
    group_id: int,
) -> Optional[Group]:
    """Найти группу по ID."""
    for group in groups:
        if group.id == group_id:
            return group
    return None
EOF

cat << 'EOF' > models/topics.py
from typing import Optional


class Topic:
    """Тема для подготовки к занятию."""

    def __init__(self, topic_id: int, name: str, date: str) -> None:
        self.id = topic_id
        self.name = name
        self.date = date

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"


def find_topic_by_id(
    topics: list[Topic],
    topic_id: int,
) -> Optional[Topic]:
    """Найти тему по ID."""
    for topic in topics:
        if topic.id == topic_id:
            return topic
    return None
EOF

cat << 'EOF' > models/tasks.py
from typing import Optional

from models.groups import Group
from models.topics import Topic


class Task:
    """Задача по теме для группы."""

    def __init__(
        self,
        task_id: int,
        topic: Topic,
        group: Group,
        title: str,
    ) -> None:
        self.id = task_id
        self.topic = topic
        self.group = group
        self.title = title
        self.done = False

    def complete(self) -> None:
        """Отметить задачу выполненной."""
        self.done = True

    @staticmethod
    def status_text(done: bool) -> str:
        """Вернуть текст статуса задачи."""
        return "готово" if done else "в работе"

    def __str__(self) -> str:
        status = self.status_text(self.done)
        return f"{self.title} | {self.topic.name} | {status}"


def find_task_by_id(
    tasks: list[Task],
    task_id: int,
) -> Optional[Task]:
    """Найти задачу по ID."""
    for task in tasks:
        if task.id == task_id:
            return task
    return None


def calculate_group_readiness(
    tasks: list[Task],
    group_id: int,
) -> int:
    """Посчитать готовность группы в процентах."""
    total = 0
    done = 0
    for task in tasks:
        if task.group.id == group_id:
            total += 1
            if task.done:
                done += 1
    if total == 0:
        return 0
    return int(done / total * 100)
EOF

cat << 'EOF' > storage.py
import json
from pathlib import Path

from models import Group, Student, Task, Topic


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def _read_json(filename: Path) -> list[dict]:
    """Прочитать JSON-файл."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def _write_json(filename: Path, data: list[dict]) -> None:
    """Записать данные в JSON-файл."""
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_students() -> list[Student]:
    """Загрузить студентов."""
    data = _read_json(DATA_DIR / "students.json")
    students = []
    for item in data:
        students.append(Student.from_data(item))
    return students


def save_students(students: list[Student]) -> None:
    """Сохранить студентов."""
    data = []
    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
        })
    _write_json(DATA_DIR / "students.json", data)


def load_groups(students: list[Student]) -> list[Group]:
    """Загрузить группы."""
    data = _read_json(DATA_DIR / "groups.json")
    groups = []
    for item in data:
        group = Group(item["id"], item["name"])
        for student_id in item.get("student_ids", []):
            for student in students:
                if student.id == student_id:
                    group.add_student(student)
        groups.append(group)
    return groups


def save_groups(groups: list[Group]) -> None:
    """Сохранить группы."""
    data = []
    for group in groups:
        student_ids = []
        for student in group.students:
            student_ids.append(student.id)
        data.append({
            "id": group.id,
            "name": group.name,
            "student_ids": student_ids,
        })
    _write_json(DATA_DIR / "groups.json", data)


def load_topics() -> list[Topic]:
    """Загрузить темы."""
    data = _read_json(DATA_DIR / "topics.json")
    topics = []
    for item in data:
        topics.append(
            Topic(item["id"], item["name"], item["date"])
        )
    return topics


def save_topics(topics: list[Topic]) -> None:
    """Сохранить темы."""
    data = []
    for topic in topics:
        data.append({
            "id": topic.id,
            "name": topic.name,
            "date": topic.date,
        })
    _write_json(DATA_DIR / "topics.json", data)


def load_tasks(
    topics: list[Topic],
    groups: list[Group],
) -> list[Task]:
    """Загрузить задачи."""
    data = _read_json(DATA_DIR / "tasks.json")
    tasks = []
    for item in data:
        topic = None
        group = None
        for current_topic in topics:
            if current_topic.id == item["topic_id"]:
                topic = current_topic
        for current_group in groups:
            if current_group.id == item["group_id"]:
                group = current_group
        if topic is None or group is None:
            continue
        task = Task(item["id"], topic, group, item["title"])
        task.done = item.get("done", False)
        tasks.append(task)
    return tasks


def save_tasks(tasks: list[Task]) -> None:
    """Сохранить задачи."""
    data = []
    for task in tasks:
        data.append({
            "id": task.id,
            "topic_id": task.topic.id,
            "group_id": task.group.id,
            "title": task.title,
            "done": task.done,
        })
    _write_json(DATA_DIR / "tasks.json", data)
EOF

cat << 'EOF' > main.py
import storage
import utils
from models import Group, Student, Task, Topic
from models.groups import find_group_by_id
from models.students import find_student_by_id
from models.tasks import calculate_group_readiness, find_task_by_id
from models.topics import find_topic_by_id


def next_id(objects: list) -> int:
    """Сформировать следующий ID."""
    if not objects:
        return 1
    return max(obj.id for obj in objects) + 1


def show_students(students: list[Student]) -> None:
    """Показать студентов."""
    if not students:
        print("Студентов нет.")
        return
    for student in students:
        print(f"{student.id}. {student}")


def add_student(students: list[Student]) -> None:
    """Добавить студента."""
    name = utils.input_non_empty("Имя студента: ")
    email = utils.input_non_empty("Email: ")
    students.append(Student(next_id(students), name, email))
    print("Студент добавлен.")


def show_groups(groups: list[Group]) -> None:
    """Показать группы."""
    if not groups:
        print("Групп нет.")
        return
    for group in groups:
        print(f"{group.id}. {group}")


def add_group(groups: list[Group]) -> None:
    """Добавить группу."""
    name = utils.input_non_empty("Название группы: ")
    groups.append(Group(next_id(groups), name))
    print("Группа добавлена.")


def assign_student(
    students: list[Student],
    groups: list[Group],
) -> None:
    """Добавить студента в группу."""
    show_groups(groups)
    group_id = utils.input_int("ID группы: ")
    group = find_group_by_id(groups, group_id)
    if group is None:
        print("Группа не найдена.")
        return
    show_students(students)
    student_id = utils.input_int("ID студента: ")
    student = find_student_by_id(students, student_id)
    if student is None:
        print("Студент не найден.")
        return
    group.add_student(student)
    print("Студент добавлен в группу.")


def show_topics(topics: list[Topic]) -> None:
    """Показать темы."""
    if not topics:
        print("Тем нет.")
        return
    for topic in topics:
        print(f"{topic.id}. {topic}")


def add_topic(topics: list[Topic]) -> None:
    """Добавить тему."""
    name = utils.input_non_empty("Название темы: ")
    date = utils.input_date("Дата занятия (ГГГГ-ММ-ДД): ")
    topics.append(Topic(next_id(topics), name, date))
    print("Тема добавлена.")


def show_tasks(tasks: list[Task]) -> None:
    """Показать задачи."""
    if not tasks:
        print("Задач нет.")
        return
    for task in tasks:
        print(f"{task.id}. {task} | группа: {task.group.name}")


def add_task(
    tasks: list[Task],
    topics: list[Topic],
    groups: list[Group],
) -> None:
    """Добавить задачу."""
    show_topics(topics)
    topic_id = utils.input_int("ID темы: ")
    topic = find_topic_by_id(topics, topic_id)
    if topic is None:
        print("Тема не найдена.")
        return
    show_groups(groups)
    group_id = utils.input_int("ID группы: ")
    group = find_group_by_id(groups, group_id)
    if group is None:
        print("Группа не найдена.")
        return
    title = utils.input_non_empty("Текст задачи: ")
    tasks.append(Task(next_id(tasks), topic, group, title))
    print("Задача добавлена.")


def complete_task(tasks: list[Task]) -> None:
    """Отметить задачу выполненной."""
    show_tasks(tasks)
    task_id = utils.input_int("ID задачи: ")
    task = find_task_by_id(tasks, task_id)
    if task is None:
        print("Задача не найдена.")
        return
    task.complete()
    print("Задача выполнена.")


def show_readiness(
    tasks: list[Task],
    groups: list[Group],
) -> None:
    """Показать готовность группы."""
    show_groups(groups)
    group_id = utils.input_int("ID группы: ")
    group = find_group_by_id(groups, group_id)
    if group is None:
        print("Группа не найдена.")
        return
    percent = calculate_group_readiness(tasks, group.id)
    print(f"Готовность группы {group.name}: {percent}%")


def main() -> None:
    """Точка запуска приложения."""
    students = storage.load_students()
    topics = storage.load_topics()
    groups = storage.load_groups(students)
    tasks = storage.load_tasks(topics, groups)

    while True:
        print("=== Система совместной подготовки ===")
        print("1. Показать студентов")
        print("2. Добавить студента")
        print("3. Показать группы")
        print("4. Добавить группу")
        print("5. Добавить студента в группу")
        print("6. Показать темы")
        print("7. Добавить тему")
        print("8. Показать задачи")
        print("9. Добавить задачу")
        print("10. Выполнить задачу")
        print("11. Готовность группы")
        print("0. Выход")
        choice = utils.input_int("Выберите действие: ")
        if choice == 1:
            show_students(students)
        elif choice == 2:
            add_student(students)
        elif choice == 3:
            show_groups(groups)
        elif choice == 4:
            add_group(groups)
        elif choice == 5:
            assign_student(students, groups)
        elif choice == 6:
            show_topics(topics)
        elif choice == 7:
            add_topic(topics)
        elif choice == 8:
            show_tasks(tasks)
        elif choice == 9:
            add_task(tasks, topics, groups)
        elif choice == 10:
            complete_task(tasks)
        elif choice == 11:
            show_readiness(tasks, groups)
        elif choice == 0:
            break
        else:
            print("Неверный пункт меню.")

    storage.save_students(students)
    storage.save_groups(groups)
    storage.save_topics(topics)
    storage.save_tasks(tasks)
    print("Данные сохранены.")


if __name__ == "__main__":
    main()
EOF

cat << 'EOF' > tests/test_models.py
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
EOF

echo '[]' > data/students.json
echo '[]' > data/groups.json
echo '[]' > data/topics.json
echo '[]' > data/tasks.json

echo "✅ Все файлы созданы!"
