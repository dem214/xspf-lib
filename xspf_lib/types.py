from typing import TypeVar

URI = str
Milliseconds = int

T = TypeVar("T")


class NonNegative:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value: int):
        if value < 0:
            raise ValueError
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        getattr(owner, instance)
