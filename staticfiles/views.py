from django.http import HttpResponse
from django_sendfile import sendfile


# Create your views here.


def static_index(request):
    return HttpResponse(status=404)


def serve_static(request, static):
    return sendfile(request, "/home/static_HA" + static)
