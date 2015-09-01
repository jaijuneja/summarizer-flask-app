import os

from flask import flash
from flask_wtf import Form
from datetime import datetime


def flash_errors(*args):
    for error_set in args:
        if isinstance(error_set, Form):
            for field, errors in error_set.errors.items():
                for error in errors:
                    label = getattr(error_set, field).label.text
                    label = label[:-1] if label.endswith(':') else label
                    flash(u'{0}: {1}'.format(
                        label,
                        error
                    ))
        else:
            for error in error_set:
                flash(error)


def check_create_dir(path):
    if os.path.isdir(path):
        return
    os.makedirs(path)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """

    now = datetime.now()
    if type(time) is int:
        time = datetime.fromtimestamp(time)
        diff = now - time
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    else:
        return ''

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "Just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "A minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "An hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    # if day_diff < 31:
        # return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return time.strftime('%-d %b')
        # return str(day_diff / 30) + " months ago"
    # return str(day_diff / 365) + " years ago"
    return time.strftime('%-d %b %Y')