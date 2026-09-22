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
