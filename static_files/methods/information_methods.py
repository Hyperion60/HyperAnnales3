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

    if not len(context['errors']):
        new_information = Informations(title=context['title'],
                                       body=context['body'],
                                       school=school,
                                       year=year,
                                       date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       date_expiry=date_end,
                                       author=request.user)
        new_information.save()
