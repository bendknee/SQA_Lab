from django import template
from django.utils import timezone

register = template.Library()
@register.filter()
def smother_timedelta(datetime_obj):
    delta = timezone.now() - datetime_obj
    seconds_delta = delta.total_seconds()
    if seconds_delta > 2628000:
        return "{} month(s) ago".format(int(seconds_delta//2628000))
    elif seconds_delta > 604800:
        return "{} week(s) ago".format(int(seconds_delta//604800))
    elif seconds_delta > 86400:
        return "{} day(s) ago".format(int(seconds_delta//86400))
    elif seconds_delta > 3600:
        return "{} hour(s) ago".format(int(seconds_delta//3600))
    elif seconds_delta > 60:
        return "{} minute(s) ago".format(int(seconds_delta//60))
    elif seconds_delta < 10:
        return "Just now"
    else:
        return "{} second(s) ago".format(int(seconds_delta))
