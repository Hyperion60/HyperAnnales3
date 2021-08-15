from django_sendfile import sendfile
import tokenlib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from HyperAnnales.settings import KEY_TOKEN
from static_files.methods.extension_methods import template_choice
from static_files.models import StaticContent, CategoryFile, ExtensionFile
from static_files.views.base_template import queryset_template
from static_files.methods.file_methods import init_view


def init_addfile_view(request):
    return init_view(request)


def FileFormView(request):
    pass


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
    file = StaticContent.objects.get(pk=data['id'])
    return sendfile.sendfile(request, file.path, attachment=False, attachment_filename=file.name)


@login_required(login_url="/login/")
def UpdateFileView(request, randomkey):
    context = {}
    try:
        context['file'] = StaticContent.objects.get(file__randomkey__exact=randomkey)
    except StaticContent.DoesNotExist:
        context['error'] = "La clé renseignée n'existe pas."
    if request.POST:
        # Defaut values
        name = context['file'].name
        place = context['file'].place
        extension = context['file'].file.extension
        classe = context['file'].classe
        category = context['file'].category
        category_title = context['file'].category.title

        # Set value
        if len(request.POST['name']):
            name = request.POST['name']
        if 0 < int(request.POST['place']) < len(StaticContent.objects.filter(category=context['file'].category)):
            place = int(request.POST['place'])
        try:
            extension = ExtensionFile.objects.get(extension=request.POST['extension'])
        except ExtensionFile.DoesNotExist:
            pass
        if request.POST['extension'] in StaticContent.LIST_CLASS:
            classe = request.POST['classe']
        if request.POST['category'] in CategoryFile.objects.filter(subject=context['file'].category.subject):
            category = request.POST['category']
        if request.user.is_staff and len(request.POST['title']):
            category_title = request.POST['title']
        context['file'].name = name
        context['file'].place = place
        context['file'].file.extension = extension
        context['file'].classe = classe
        context['file'].category = category
        context['file'].category.title = category_title
        context['file'].save()
        context['message'] = "Le fichier a bien été modifié."
        return render(request, "static_content/admin/message_template.html", context)
    return render(request, "static_content/change/change-file.html", context)
