from django import template

register = template.Library()


@register.filter
def day_of_week(weekday_number:  int) -> str:
    if weekday_number == 0:
        return 'в понедельник'
    elif weekday_number == 1:
        return 'во вторник'
    elif weekday_number == 2:
        return 'в среду'
    elif weekday_number == 3:
        return 'в четверг'
    elif weekday_number == 4:
        return 'в пятницу'
    elif weekday_number == 5:
        return 'в субботу'
    elif weekday_number == 6:
        return 'в воскресенье'


@register.filter
def mediapath(object_img: str):
    return f'/media/{object_img}'


@register.simple_tag
def mediapath(object_img: str):
    return f'/media/{object_img}'
