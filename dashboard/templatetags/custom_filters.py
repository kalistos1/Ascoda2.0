# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='divide_by_half')
def divide_by_half(amount, income_type):
    if income_type in ['APPRECIATION', 'LOOSE_OFFERING', 'CHILD_DEDICATION', 'THANKS_OFFERING', 'SABBATH_SCHOOL_EXPENSE_OFFERING','ENVELOPE_OFFERING','INFANT_DEPT_OFFERING']:
        return amount / 2
    return amount


@register.filter(name='add_attributes')
def add_attributes(field, css):
    return field.as_widget(attrs={"class": css})