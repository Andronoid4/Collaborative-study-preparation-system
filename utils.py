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
