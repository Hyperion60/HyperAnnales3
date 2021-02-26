from django.shortcuts import render
from static_files.models import *
from static_files.views.base_template import sidenav


def school(request, school):
    context = {}
    years = {}
    list_year = YearFile.objects.all().order_by('year')
    for year in list_year:
        number = StaticContent.objects.filter(category__subject__year__year__exact=year.year)
        years[year.year] = len(number)
    context['voyelle'] = (school[0] in ('aeiouy'))
    context['years'] = years
    context['school'] = school
    context['infos'] = None
    return render(request, 'navigation/school.html', context)


def year(request, school, year):
    context = {}
    context['school'] = school
    context['year'] = year
    context['infos'] = None
    school_obj = School.objects.get(school__exact=school)
    year_obj = YearFile.objects.get(year__exact=year)
    sidenav(school_obj, year_obj)
    return render(request, 'navigation/year.html', context)
