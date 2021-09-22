from django.core.files.storage import FileSystemStorage

from HyperAnnales.settings import BASE_MEDIA_URL, BASE_MEDIA_ROOT
from static_files.methods.annexe_methods import update_git_direct
from static_files.models import UnsecureFile


def save_unsecure_file(request, context):
    new_file = context['file']
    fs = FileSystemStorage()
    fs.save(context['raw_path'], new_file)
    context['message'] = "Fichier ajouté avec succès"
    commit = "File({}); {}\nAuteur: {}".format(context['extension'], context['filename'], request.user)
    update_git_direct(context['raw_path'], BASE_MEDIA_ROOT, commit, context)


def add_unsecured_file(request, context, type):
    type += '/'
    if context['url']:
        url = context['url']
        filename = context['title']
        count = 0
        while len(UnsecureFile.objects.filter(filename__exact=filename)):
            filename = "{}_{}".format(context['title'], ++count)
    else:
        filename = "{}.{}".format(context['title'], context['extension'].extension)
        count = 0
        while len(UnsecureFile.objects.filter(filename__exact=filename)):
            filename = "{}_{}.{}".format(context['title'], ++count, context['extension'].extension)
        context['raw_path'] = BASE_MEDIA_ROOT + str(type) + filename
        url = BASE_MEDIA_URL + str(type) + filename
    new_file = UnsecureFile(
        title=context['title'],
        bulletin=context['bulletin'],
        author=context['bulletin'].author,
        filename=filename,
        url=url,
        extension=context['extension'],
    )
    context['filename'] = filename
    if context['file']:
        save_unsecure_file(request, context)
    new_file.save()


def update_unsecure_file(context):
    pass