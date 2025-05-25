import os
import uuid


class LocalStorage:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def store(self, filename: str, content: bytes) -> str:
        """
        Сохраняет байты в файл data/<uuid>_<filename> и возвращает относительный путь.
        """
        unique_id = uuid.uuid4().hex
        safe_name = f"{unique_id}_{filename}"
        path = os.path.join(self.base_dir, safe_name)
        with open(path, "wb") as f:
            f.write(content)
        return path  # сохраняем именно файловую систему путь
