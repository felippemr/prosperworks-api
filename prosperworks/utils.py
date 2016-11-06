from datetime import datetime

import exceptions


EPOCH = datetime(1970, 1, 1)


def validate_fields(fields, valid_fields, field_name=''):
    for field in fields.keys():
        if field not in valid_fields:
            raise exceptions.ProsperWorksApplicationException(
                u"%s is not a valid %s field." % (field, field_name)
            )


def timestamp(dt, convert_to_int=True):
    stamp = (dt - EPOCH).total_seconds()
    return int(stamp) if convert_to_int else stamp


class QuickRepr(object):
    def get_fields(self):
        return [
            key for key in self.__dict__
            if not key.startswith('_')
        ]

    def __unicode__(self):
        return repr(self)

    def __repr__(self):
        return u"<%s: %s>" % (
            self.__class__.__name__,
            u', '.join(
                u"%s=%s" % (key, str(getattr(self, key)))
                for key in self.get_fields()
            )
        )


class Data(QuickRepr):
    """Utility class to wrap a dict as an object."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = Data(**value)
            setattr(self, key, value)
