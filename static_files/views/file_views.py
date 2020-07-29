from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from HyperAnnales.settings import KEY_TOKEN
from static_files.views.base_template import queryset_template
from static_files.models import StaticContent
from static_files.methods.extension_methods import template_choice

import time
import tokenlib
from django_sendfile import sendfile


@cache_page(4 * 60)
@login_required(login_url="/login/")
def CreateFileView(request, method, year, id):
    context = {}
    context = queryset_template(year, context)
    context['token'] = tokenlib.make_token({"id": id}, secret=KEY_TOKEN)
    context['title'] = StaticContent.objects.get(pk=id).name
    return render(request, template_choice(method), context)


@cache_page(4 * 60)
@login_required(login_url="/login/")
def SendFile(request, token):
    try:
        data = tokenlib.parse_token(token, secret=KEY_TOKEN)
    except ValueError:
        return HttpResponse("Token expiré")
    file = StaticContent.objects.get(pk=data['id'])
    return sendfile.sendfile(request, file.path, attachment=False, attachment_filename=file.name)
