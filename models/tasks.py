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
