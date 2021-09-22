from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from static_files.models import Bulletin, UnsecureFile, ExtensionFile
from static_files.methods.unsecure_file_methods import add_unsecured_file, update_unsecure_file
from static_files.views.annexe_functions import create_list_extension


def add_file_bulletin(request, pk):
    context = {
        'errors': [],
        'next': request.GET.get('next', ''),
    }
    try:
        context['bulletin'] = Bulletin.objects.get(pk=pk)
    except Bulletin.DoesNotExist:
        context['errors'].append("Le bulletin demandé n'existe pas. La clé est introuvable.")
        return render(request, "static_content/admin/index.html", context)

    if request.user != context['bulletin'].author and not request.user.is_staff:
        context['errors'].append("Vous n'avez pas l'authorisation de modifier ce bulletin.")
        return render(request, "static_content/admin/index.html", context)

    if request.POST:
        try:
            context['title'] = request.POST['title']
        except MultiValueDictKeyError:
            context['errors'].append("Le champ titre est manquant ou non renseigné.")

        try:
            context['extension'] = ExtensionFile.objects.get(extension__exact=request.POST['extension'])
        except MultiValueDictKeyError:
            context['errors'].append("Le champ extension est manquant ou non reseigné.")
        except ExtensionFile.DoesNotExist:
            context['errors'].append("Le champ extension est invalide. Clé introuvable.")

        if request.POST.get('url', ''):
            context['url'] = request.POST['url']
        else:
            try:
                context['file'] = request.FILES['file']
            except MultiValueDictKeyError:
                context['errors'].append("Fichier manquant ou introuvable.")

        if len(context['errors']):
            return render(request, "static_content/add/add-bulletin-file.html", context)

        add_unsecured_file(request, context, "bulletin")
        return render(request, "static_content/admin/message_template.html", context)

    context['extensions'] = ExtensionFile.objects.all().order_by('type')
    context['list_extension'] = create_list_extension()

    return render(request, "static_content/add/add-bulletin-file.html", context)


def update_bulletin_file(request, pk):
    context = {
        'errors': [],
        'next': request.GET.get('next', ''),
    }
    try:
        context['file'] = UnsecureFile.objects.get(pk=pk)
    except UnsecureFile.DoesNotExist:
        context['errors'].appand("Le fichier demandé est introuvable. La clé primaire n'existe pas.")
    try:
        context['bulletin'] = Bulletin.objects.get(pk=context['file'].bulletin.pk)
    except Bulletin.DoesNotExist:
        context['errors'].append("Le bulletin demandé est introuvable. La clé primaire n'existe pas.")

    if request.POST:
        try:
            context['url'] = request.POST['url']
            context['type'] = "url"
        except MultiValueDictKeyError:
            context['type'] = "file"

        if context['type'] == "file" and context['file'].filename != request.POST['file_name']:
            try:
                context['file_post'] = request.FILES['file']
            except MultiValueDictKeyError:
                context['errors'].append("Vous devez soit entrer une URL soit uploader un fichier.")

        elif context['file'].filename == request.POST['file_name']:
            context['type'] = None

        try:
            context['extension'] = ExtensionFile.objects.get(pk=request.POST['extension'])
        except MultiValueDictKeyError:
            context['errors'].append("Champ d'extension manquant.")
        except ExtensionFile.DoesNotExist:
            context['errors'].append("L'extension demandée est introuvable. La clé primaire n'existe pas.")

        update_unsecure_file(context)
        return render(request, "static_content/admin/message_template.html", context)

    context['extensions'] = ExtensionFile.objects.exclude(pk=context['file'].extension)
    context['list_extension'] = create_list_extension()
    file = {
        'name': context['file'].name,
        'extension': context['file'].extension,
    }
    if context['file'].extension.extension == "url":
        file['url'] = context['file'].url
        file['filename'] = None
    else:
        file['filename'] = context['file'].filename
        file['url'] = None

    return render(request, "static_content/change/change-unsecured-file.html", context)
