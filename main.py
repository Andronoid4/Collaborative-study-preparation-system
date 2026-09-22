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
