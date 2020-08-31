from django_sendfile import sendfile
import tokenlib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from HyperAnnales.settings import KEY_TOKEN
from static_files.methods.extension_methods import template_choice
from static_files.models import StaticContent
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