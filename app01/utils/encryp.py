import hashlib
from django.conf import settings


def md5(data_string):
    hash_obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    hash_obj.update(data_string.encode("utf-8"))
    return hash_obj.hexdigest()
