# CUSTOM VALIDATORS
from django.core.exceptions import ValidationError

def is_isbn(value):
    """Check if value is 13 digit ISBN."""
    if len(value) != 13:
        raise ValidationError("Value should contain 13 digits.")