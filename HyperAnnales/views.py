from django.shortcuts import render
from django.db import connections
from accounts.models import *
from static_files.models import School
import django


def index(request):
    context = {}
    context['schools'] = School.objects.all()
    return render(request, 'index.html', context)


def __postgres_version():
    brut = str(connections['user_ref'].cursor().connection.server_version)
    str_version = ""
    is_point = True
    is_OK = True
    for letter in brut:
        if letter == '0':
            if is_point:
                str_version += '.'
                is_point = False
            else:
                str_version += letter
                is_point = True
            is_OK = False
        if is_OK:
            str_version += letter
        is_OK = True
    return str_version


def __staff_members():
    staff_user = Account.object.filter(is_active=True, is_staff=True)
    output = staff_user[0].username
    i = 1
    while i < len(staff_user):
        output = output + ", " + str(staff_user[i].username)
        i = i + 1
    return output


def about(request):
    context = {}
    context['HA_version'] = "beta"
    context['date'] = "21-05-2020"
    context['django_version'] = django.get_version()
    context['angular_version'] = "9"
    context['postgresql_version'] = __postgres_version()
    context['docker_version'] = "19.03"
    context['kube_version'] = "N/A"
    context['staff'] = __staff_members()
    return render(request, 'about.html', context)
