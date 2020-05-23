from django.shortcuts import render
from django.db.backends.postgresql import base
from accounts.models import *
import django


def index(request):
    return render(request, 'index.html')


def __postgres_version():
    tuple_version = base.psycopg2_version()
    return str(tuple_version[0]) + "." + str(tuple_version[1]) + "." + str(tuple_version[2])


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
