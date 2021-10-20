from django_sendfile import sendfile
import tokenlib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from HyperAnnales.settings import KEY_TOKEN, BASE_MEDIA_ROOT
from static_files.methods.extension_methods import template_choice
from static_files.models import StaticContent, CategoryFile, ExtensionFile, ContentColor, StaticFile
from static_files.views.base_template import queryset_template, sidenav
from static_files.methods.file_methods import init_view, get_token
from static_files.methods.open_file.switch_extension import get_file


def init_addfile_view(request):
    return init_view(request)


# Website views
@cache_page(4 * 60)
@login_required(login_url="/login/")
def CreateFileView(request, method, year, id):
    context = {}
    context = queryset_template(year, context)
    context['token'] = tokenlib.make_token({"id": id}, secret=KEY_TOKEN)
    file = StaticContent.objects.get(pk=id)
    context['title'] = file.name
    context['semester'] = file.semester.semester
    context['year'] = file.year.year
    context['subject'] = file.subject.subject
    context['school'] = request.user.school
    return render(request, template_choice(file.extension.type), context)


@cache_page(4 * 60)
@login_required(login_url="/login/")
def SendFile(request, token):
    try:
        data = tokenlib.parse_token(token, secret=KEY_TOKEN)
    except ValueError:
        return HttpResponse("Token expiré")
    file = StaticContent.objects.get(file__randomkey__exact=data['key'])
    path = "{}{}{}-{}".format(BASE_MEDIA_ROOT, file.file.path, file.name, file.file.randomkey)
    try:
        fs = open(path, "r")
    except OSError:
        print("Chemin d'accès invalide.")
    return sendfile(request, path, attachment=False, attachment_filename=file.name)


@login_required(login_url="/login/")
def UpdateFileView(request, rndkey):
    context = {'errors': []}
    try:
        context['file'] = StaticContent.objects.get(file__randomkey__exact=rndkey)
        context['max'] = len(StaticContent.objects.filter(category__exact=context['file'].category))
        context['extensions'] = ExtensionFile.objects.exclude(extension__exact=context['file'].file.extension.extension)
        context['categories'] = CategoryFile.objects.exclude(id=context['file'].category.id).filter(
            subject__exact=context['file'].category.subject)
        context['colors'] = ContentColor.objects.exclude(pk=context['file'].classe.pk).order_by('type')
    except StaticContent.DoesNotExist:
        context['errors'].append("La clé renseignée n'existe pas.")
    if request.POST:
        # Defaut values
        name = context['file'].name
        place = context['file'].place
        extension = context['file'].file.extension
        classe = context['file'].classe
        category = context['file'].category

        # Name
        if len(request.POST['content_name']):
            name = request.POST['content_name']

        # Place
        list_file = StaticContent.objects.filter(category=context['file'].category)
        place = int(request.POST['content_place'])
        if 0 < place < len(list_file) + 1:
            for file in list_file.exclude(pk=context['file'].pk):
                if place > context['file'].place:
                    if place >= file.place > context['file'].place:
                        file.place -= 1
                        file.save()
                else:
                    if context['file'].place > file.place >= place:
                        file.place += 1
                        file.save()
            place = int(request.POST['content_place'])

        # Extension
        try:
            extension = ExtensionFile.objects.get(pk=request.POST['content_extension'])
        except ExtensionFile.DoesNotExist:
            context['errors'].append("Cette extension n'existe pas.")

        # Classe
        try:
            color = ContentColor.objects.get(pk=request.POST['content_color'])
        except ContentColor.DoesNotExist:
            context['errors'].append("Classe de fichier invalide.")

        # Category
        if request.user.is_staff and request.POST['new_category_title']:
            new_category = CategoryFile(title=str(request.POST['new_category_title']),
                                        place=len(
                                            CategoryFile.objects.filter(subject=context['file'].category.subject)),
                                        subject=context['file'].category.subject)
            new_category.save()
            category = new_category
        else:
            try:
                if CategoryFile.objects.get(pk=request.POST['content_category']) in CategoryFile.objects.filter(
                        subject=context['file'].category.subject):
                    category = CategoryFile.objects.get(pk=request.POST['content_category'])
            except CategoryFile.DoesNotExist:
                if context['error']:
                    context['error'] += "\n"
                context['error'] += "Catégorie non permise pour ce fichier."

        # Save
        context['file'].name = name
        context['file'].place = place
        context['file'].file.extension = extension
        context['file'].classe = color
        context['file'].category = category
        context['file'].save()
        context['message'] = "Le fichier a bien été modifié."
        return render(request, "static_content/admin/message_template.html", context)
    return render(request, "static_content/change/change-file.html", context)


@login_required(login_url="/login/")
def GetFile(request, key):
    context = {
        'errors': [],
    }
    try:
        context['file'] = StaticFile.objects.get(randomkey__exact=key)
    except StaticFile.DoesNotExist:
        context['errors'].append("Le fichier demandé n'existe pas.")

    """
    # Pour gérer les fichiers désactivés/supprimés
    if not context['errors'] and not context['file'].enable:
        context['errors'].append("Le fichier demandé n'est plus disponible")
    """

    if context['errors']:
        return redirect("navigation/subject.html")
        # return navigation.subject(errors), surcharge de la fonction à ajouter ou wrapper

    if context['errors']:
        return redirect("navigation/subject.html")
        # return navigation.subject(errors), surcharge de la fonction à ajouter ou wrapper

    context['year'] = context['file'].content.category.year_obj()
    context['school'] = context['file'].content.category.school_obj()
    context['semester'] = context['file'].content.category.semester_obj()
    context['subject'] = context['file'].content.category.subject
    context['category'] = context['file'].content.category
    context['token'] = get_token(request.user, key)
    sidenav(context, context['school'], context['year'])
    context['next'] = "/{}/{}/{}/{}/".format(context['school'].school,
                                             context['year'].year,
                                             context['semester'].semester,
                                             context['subject'].subject)

    if not context['file'].extension.extension == 'pdf':
        context['errors'].append("Extension non supportée pour le moment. Réessayez plus tard")
        return render(request, "static_content/admin/message_template.html", context)
    return render(request, "static_content/get/pdf_model.html", context)
