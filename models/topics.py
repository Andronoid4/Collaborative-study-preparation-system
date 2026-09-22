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
