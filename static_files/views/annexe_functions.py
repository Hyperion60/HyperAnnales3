from random import randint
from static_files.models import StaticContent, StaticFile, ExtensionFile


def get_color(static_content):
    if not type(static_content) is StaticContent:
        return None
    return str(static_content.classe)[1:-1].split(',')[1][2:-1]


def create_random_key():
    n = 0
    while n == 0 and len(StaticFile.objects.filter(randomkey__exact=n)):
        n = randint(1, 999999)
    return n


def create_list_extension():
    list_extension = ""
    for extension in ExtensionFile.objects.all():
        list_extension += ".{}, ".format(extension.extension)
    return list_extension[:-2]
