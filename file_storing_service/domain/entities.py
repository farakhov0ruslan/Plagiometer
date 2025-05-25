from dataclasses import dataclass

@dataclass
class FileEntity:
    id: str
    name: str
    hash: str
    location: str
