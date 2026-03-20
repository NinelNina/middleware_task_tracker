import datetime

# Упрощенная «база» задач
TASKS_DB = {}


def create_task(title: str, user_id: int, due_date: datetime.date) -> dict:
    """
    Создает новую задачу и сохраняет ее в TASKS_DB.
    Возвращает словарь с данными о задаче.
    Генерирует ValueError, если title пустой или дата просрочена.
    """
    if not title:
        raise ValueError("Task title cannot be empty.")
    if due_date < datetime.date.today():
        raise ValueError("Due date cannot be in the past.")

    task_id = len(TASKS_DB) + 1
    task_data = {
        "task_id": task_id,
        "title": title,
        "user_id": user_id,
        "due_date": due_date,
        "created_at": datetime.datetime.now(),
        "completed": False
    }
    TASKS_DB[task_id] = task_data
    return task_data


def complete_task(task_id: int) -> dict:
    """
    Отмечает задачу как завершенную.
    Поднимает KeyError, если такой задачи нет.
    """
    if task_id not in TASKS_DB:
        raise KeyError(f"Task with id={task_id} not found.")

    task_data = TASKS_DB[task_id]
    task_data["completed"] = True
    return task_data


# Пример использования (для теста)
if __name__ == "__main__":
    # Создаем задачу
    new_task = create_task("Finish project", user_id=101, due_date=datetime.date(2025, 8, 1))
    print("Created task:", new_task)

    # Завершаем задачу
    updated_task = complete_task(new_task["task_id"])
    print("Updated (completed) task:", updated_task)