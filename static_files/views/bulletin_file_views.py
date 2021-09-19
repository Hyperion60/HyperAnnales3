from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from static_files.models import Bulletin, UnsecureFile, ExtensionFile
from static_files.methods.unsecure_file_methods import add_unsecured_file


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
            context['extension'] = ExtensionFile.objects.get(pk=request.POST['extension'])
        except MultiValueDictKeyError:
            context['errors'].append("Le champ extension est manquant ou non reseigné.")
        except ExtensionFile.DoesNotExist:
            context['errors'].append("Le champ extension est invalide. Clé introuvable.")

        if request.POST.get('url', ''):
            context['url'] = request.POST['url']

        if len(context['errors']):
            return render(request, "static_content/admin/index.html", context)

        add_unsecured_file(request, context, "bulletin")