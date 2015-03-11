from flask import flash
from flask_wtf import Form


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