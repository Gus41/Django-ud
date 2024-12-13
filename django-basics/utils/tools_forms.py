from django.core.exceptions import ValidationError
import re

def add_attr(field,attr_name,attr_val):
    field.widget.attrs[attr_name] = f'{attr_val}'.strip()


def add_placeholder(field,place_holder_val: str):
    add_attr(field,'placeholder',place_holder_val)

def strong_password(password: str):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError("Password is not strong",code='invalid')
    
    
    
def is_positive_number(value):
    try:
        number = float(value)
    except (ValueError, TypeError):
        return False
    
    return number > 0
