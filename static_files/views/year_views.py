from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.models import School
from static_files.form.year_forms import SetYearSemester
from static_files.methods.year_methods import create_year, set_year

from datetime import datetime


@login_required(login_url="/login/")
def CreateYearView(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    error = False
    if request.POST:
        year, semester = None, None
        try:
            year = int(request.POST['year'])
            semester = request.POST['active_semester']
        except KeyError:
            context['error'] = "Champ introuvable"
            error = True
        if not error:
            if 2013 < year < datetime.now().year + 6:
                create_year(year, semester)
                return render(request, "static_content/admin/message_template.html",
                              {'message': "L'année a bien été créée"})
            context['error'] = "Année entrée invalide"
    form = SetYearSemester()
    context['active_semester'] = form['active_semester']
    return render(request, "static_content/add/add-year.html", context)


@login_required(login_url="/login")
def SetSemesterYearView(request, year):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    error = False
    if request.POST:
        semester = None
        try:
            semester = request.POST['active_semester']
        except KeyError:
            context['error'] = "Champ semestre introuvable"
            error = True
        list_school = School.objects.filter(school=request.user.school)
        school = None
        if len(list_school):
            school = list_school[0]
        else:
            if len(context['error']):
                context['error'] += "\n"
            context['error'] += "Ecole de l'utilisateur introuvable"
            error = True
        if not error:
            if not set_year(year, semester, school):
                return render(request, "static_content/admin/message_template.html",
                              {'message': "Le semestre actif a bien été modifié"})
            if len(context['error']):
                context['error'] += "\n"
            context['error'] += "Champ(s) manquant(s)"
    form = SetYearSemester()
    context['active_semester'] = form['active_semester']
    return render(request, "static_content/change/change-year.html", context)
