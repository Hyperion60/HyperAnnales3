from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.models import School, CategoryFile, StaticContent
from static_files.form.subject_forms import SetSubject
from static_files.methods.subject_methods import CreateSubject


@login_required(login_url="/login/")
def CreateSubjectView(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    error = False
    if request.POST:
        year, semester, title = None, None, None
        try:
            year = request.POST['year']
            semester = request.POST['semester']
            title = request.POST['title']
            school = School.objects.filter(school__exact=request.user.school)
        except KeyError:
            if year is None or semester is None or title is None:
                context['error'] = "Un ou plusieurs champs sont introuvables"
                error = True
        if not error:
            context = CreateSubject(context, title, semester, year, school[0])
            try:
                if context['error'] is not None:
                    error = True
            except KeyError:
                if context['message'] is not None:
                    return render(request, "static_content/admin/message_template.html",
                                  {'message': context['message']})
    form = SetSubject()
    context['year'] = form['year']
    context['semester'] = form['semester']
    if not error:
        context['error'] = None
    return render(request, "static_content/add/add-subject.html", context)


@login_required(login_url="/login/")
def GetSubjectView(request, school, year, semester, subject):
    context = {}
    context['school'] = school
    context['year'] = year
    context['semester'] = semester
    context['subject'] = subject
    context['contents'] = {}
    try:
        context['contents']['category'] = []
        context['contents']['files'] = []
        for category in CategoryFile.objects.filter(subject__exact=subject):
            context['contents']['category'].append(category)
            file = {
                'obj': StaticContent.objects.filter(category=category),
                'link': None
            }
            context['contents']['files'].append(file)
        content = {}
        for key, corp in zip(context['contents']['category'], context['contents']['files']):
            content[key] = (corp['obj'], corp['link'], corp['obj'].classe[1])
        context['contents'] = content
    except CategoryFile.DoesNotExist:
        context['contents'] = None
    return render(request, "templates/navigation/subject.html", context)
