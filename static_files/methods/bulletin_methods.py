from django.db import IntegrityError
from django.utils import timezone

from static_files.models import Bulletin, UnsecureFile, School, YearFile
from datetime import datetime


def list_bulletin_admin_view(request):
    list_bulletin = Bulletin.objects.filter(author=request.user)
    if not len(list_bulletin):
        return None
    contribution = []
    for bulletin in list_bulletin:
        contrib = {
            'year': bulletin.year,
            'location': bulletin.location,
            'title': bulletin.title,
            'pk': bulletin.pk,
            'files': []
        }
        for file in UnsecureFile.objects.filter(bulletin=bulletin):
            contrib['files'].append(file)
        contribution.append(contrib)
    print(contribution)
    return contribution


def list_bulletin_navigation(school, year=None):
    list_bulletins = Bulletin.objects.filter(year__exact=year, location__school__exact=school)

    if not len(list_bulletins):
        return None

    bulletins = []
    for bulletin in list_bulletins:
        new_bulletin = {
            'title': bulletin.title,
            'body': bulletin.body,
            'files': [],
        }
        for file in UnsecureFile.objects.filter(bulletin=bulletin):
            new_bulletin['files'].append(file)
        bulletins.append(new_bulletin)
    return bulletins


def check_information(school, year=None):
    if year:
        list_infos = Bulletin.objects.filter(location=school, year=year)
    else:
        list_infos = Bulletin.objects.filter(location=school, year__isnull=True)
    for info in list_infos:
        if info.date_expiry < timezone.now():
            info.delete()


def create_information(request, context):
    try:
        school = School.objects.get(school__exact=context['school'])
    except School.DoesNotExist:
        context['errors'].append("L'école demandée n'existe pas.")
        school = None

    year = None
    if context['year']:
        try:
            year = YearFile.objects.get(year__exact=context['year'])
        except YearFile.DoesNotExist:
            context['errors'].append("L'année demandée n'existe pas.")

    try:
        date_expiry = datetime.strptime(request.POST['date'], "%d/%m/%Y")
    except ValueError:
        context['errors'].append("Date d'expiration manquante.")

    if not len(context['errors']):
        new_information = Bulletin(title=request.POST['title'],
                                   body=request.POST['body'],
                                   location=school,
                                   year=year,
                                   date=timezone.now(),
                                   date_expiry=date_expiry,
                                   author=request.user)
        new_information.save()
        context['message'] = "Nouvelle information créée."
        return True
    return False


def update_information(request, context):
    if request.user != context['bulletin'].author and not request.user.is_staff:
        return False
    try:
        context['bulletin'].title = context['title']
        context['bulletin'].body = context['body']
        context['bulletin'].year = context['year']
        context['bulletin'].date_expiry = context['date']
        context['bulletin'].save()
    except:
        context['errors'].append("Echec de la mise a jour du bulletin")
        return False
    return True


def delete_information(request, context):
    if request.user != context['bulletin'].author and not request.user.is_staff:
        return False
    try:
        context['bulletin'].delete()
    except IntegrityError:
        context['errors'].append("Impossible de supprimer la classe ou ses dépendance, problème d'intégrité.")
        return False
    return True
