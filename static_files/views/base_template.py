from django.shortcuts import render

from static_files.models import YearFile, SemesterFile, SubjectFile


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
