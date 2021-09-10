from django.shortcuts import render

from static_files.views.annexe_functions import get_color
from static_files.models import YearFile, School, SubjectFile, CategoryFile, StaticContent, ContentColor, CategoryColor, \
    Bulletin
from static_files.views.base_template import sidenav


def school(request, school):
    context = {}
    years = {}
    list_year = YearFile.objects.all().order_by('year')
    for year in list_year:
        number = StaticContent.objects.filter(category__subject__year__year__exact=year.year)
        years[year.year] = len(number)
    bulletins_list = Bulletin.objects.filter(year=None,
                                             location__school__exact=school)
    if len(bulletins_list):
        context['bulletins'] = bulletins_list
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
    list_bulletins = Bulletin.objects.filter(location=school_obj, year=year_obj)
    if len(list_bulletins):
        context['bulletins'] = list_bulletins
    sidenav(context, school_obj, year_obj)
    return render(request, 'navigation/year.html', context)


def subject(request, school, year, semester, subject):
    context = {}
    context['school'] = school
    context['year'] = year
    context['semester'] = semester
    context['subject'] = subject
    context['contents'] = {}
    try:
        context['contents']['category'] = []
        context['contents']['files'] = []
        subject_obj = SubjectFile.objects.filter(location__school__exact=school,
                                                 year__year__exact=year,
                                                 semester__semester__exact=semester,
                                                 subject__exact=subject)[0]
        for category in CategoryFile.objects.filter(subject=subject_obj).order_by('place'):
            context['contents']['category'].append(category)
            files = []
            for staticcontent in StaticContent.objects.filter(category=category).order_by('place'):
                files.append({
                    'obj': staticcontent,
                    'link': "#"
                })
            context['contents']['files'].append(files)
        content = {}
        for key, corp in zip(context['contents']['category'], context['contents']['files']):
            content[key] = []
            if key.classe is None:
                try:
                    CategoryColor.objects.get(pk=1)
                except CategoryColor.DoesNotExist:
                    CategoryColor().save()
                key.classe = CategoryColor.objects.get(pk=1)
                key.save()
            for file in corp:
                # Try if ColorContent exist for the start up
                try:
                    ContentColor.objects.get(pk=1)
                except ContentColor.DoesNotExist:
                    ContentColor().save()
                if file['obj'].classe is None:
                    file['obj'].classe = ContentColor.objects.get(pk=1)
                    file['obj'].save()
                content[key].append((file['obj'], file['link'], file['obj'].color()))
        context['contents'] = content
    except CategoryFile.DoesNotExist:
        context['contents'] = None
    school_obj = School.objects.get(school__exact=school)
    year_obj = YearFile.objects.get(year__exact=year)
    sidenav(context, school_obj, year_obj)
    return render(request, "navigation/subject.html", context)
