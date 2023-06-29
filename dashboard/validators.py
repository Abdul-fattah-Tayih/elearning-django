from typing import List
from django.core.exceptions import ValidationError

class InList:
    def __init__(self, valid_values: List) -> None:
        self.valid_values = valid_values

    def __call__(self, value) -> None:
        if value not in self.valid_values:
            raise ValidationError(f"{value} is an invalid value")
    