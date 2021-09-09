from django.shortcuts import render

from static_files.models import Information, School, YearFile


def CreateInformation(request, school, year=None):
    context = {'errors': []}
    if request.POST:
        try:
            context['school'] = School.objects.get(school__exact=school)
        except School.DoesNotExist:
            context['errors'].append("L'école demandée n'existe pas.")

        if year:
            try:
                context['year'] = YearFile.objects.get(year__exact=year)
            except YearFile.DoesNotExist:
                context['errors'].append("L'année demandée n'existe pas.")
        print(poof)
    context['school'] = school
    context['year'] = year
    return render(request, "static_content/add/add-information.html", context)
