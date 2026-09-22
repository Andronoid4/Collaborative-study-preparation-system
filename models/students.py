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
