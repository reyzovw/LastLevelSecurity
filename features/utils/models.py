from dataclasses import dataclass


@dataclass
class PasswordModel:
    id: int
    name: str
    value: str
