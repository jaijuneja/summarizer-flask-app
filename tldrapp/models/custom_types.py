import json
from .. import db

# from sqlalchemy import TypeDecorator, Text, String
# class Json(TypeDecorator):
#     impl = Text
#
#     def process_bind_param(self, value, engine):
#         return json.dumps(value)
#
#     def process_result_value(self, value, engine):
#         return json.loads(value)


# Note that in a typical scenario we would use the commented code above to construct
# new type. However, the above does not work using Flask-WhooshAlchemy so we need to
# inherit directly from String.
class Json(db.String):

    def __init__(self, *args, **kwargs):
        super(Json, self).__init__(args, kwargs)

    def bind_processor(self, dialect):
        def processor(value):
            return json.dumps(value)
        return processor

    def result_processor(self, dialect, coltype):
        def processor(value):
            return json.loads(value)
        return processor