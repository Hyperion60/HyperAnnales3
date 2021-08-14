from django.shortcuts import render

from static_files.models import YearFile, SemesterFile, SubjectFile


def sidenav(context, school, year):
    semesters = {}
    counts = {}
    list_semester = SemesterFile.objects.filter(semester__lte=year.active_semester.semester).order_by('semester')
    for semester in list_semester:
        semesters[semester.semester] = SubjectFile.objects.filter(location__exact=school, year__exact=year, semester__exact=semester).order_by('subject')
    for semester in semesters:
        c = 0
        for subject in semesters[semester]:
            c += subject.count
        counts[semester] = c
    context['semesters'] = semesters
    context['counts'] = counts


def queryset_template(year, context):
    year_obj = YearFile.objects.filter(year=year)[0]
    list_semester = SemesterFile.objects.filter(semester__lte=year_obj.active_semester.semester).order_by('semester')
    subjects = {}
    for semester in list_semester:
        subject = SubjectFile.objects.filter(year=year_obj, semester=semester).order_by('subject')
        if not len(subject):
            subjects[semester.semester] = None
        else:
            subjects[semester.semester] = subject
    context['semesters'] = subjects
    return context


def test_template(request, year):
    context = {}
    context = queryset_template(year, context)
    return render(request, "static_content/base-test.html", context)
