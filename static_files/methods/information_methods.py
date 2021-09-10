from django.shortcuts import render

from static_files.models import Informations, UnsecureFile, School, YearFile
from datetime import datetime


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
        new_information = Informations(title=context['title'],
                                       body=context['body'],
                                       location=school,
                                       year=year,
                                       date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       date_expiry=date_expiry,
                                       author=request.user)
        new_information.save()
        context['message'] = "Nouvelle information créée."
        return True
    return False
