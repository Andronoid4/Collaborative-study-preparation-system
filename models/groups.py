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
