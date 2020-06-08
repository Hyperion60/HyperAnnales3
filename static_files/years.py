from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


from static_files.methods.year_methods import create_year, get_year, set_year
from static_files.forms import CreateYearForm, SetYearSemester


# Create all years classes and all semester classes (init function for begin website
@login_required(login_url="/login/")
def create_all_years(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    if request.POST:
        begin = int(request.POST['begin'])
        end = int(request.POST['end'])
        if 2025 > end >= begin > 2014:
            for i in range(begin, end + 1):
                create_year(i)
            context['message'] = "Toutes les années ont été créees"
            return render(request, "static_content/admin/message_template.html", context)
        else:
            context['error'] = "Paramètres invalides"
    return render(request, "static_content/add/all-years.html", context())


# Create manually, unique year class
@login_required(login_url="/login/")
def set_year_semester(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    if request.POST:
        form = CreateYearForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['active_semester']
            year = form.cleaned_data['year']
            create_year(year, semester)
            context['message'] = "Le semestre actuel a bien été actualisé."
            return render(request, "static_content/admin/message-template.html", context)
    else:
        context['form'] = CreateYearForm()
    return render(request, "static_content/add/year.html", context)


# Set active_semester (when all semester and year already exist)
@login_required(login_url="/login/")
def set_semester(request, year):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    test_y = get_year(year)
    if test_y is None:
        context['error'] = "L'année selectionnée n'existe pas dans la base de données."
    if request.POST:
        form = SetYearSemester(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['active_semester']
            if set_year(test_y, semester):
                context['message'] = "Le semestre actuel a bien été actualisé."
            else:
                context['error'] = "Une erreur s'est produite, veuillez réessayer. Si l'erreur perdure, veuillez " \
                                   "contacter un administrateur"
            return render(request, "static_content/admin/message-template.html", context)
    else:
        context['form'] = SetYearSemester()
    return render(request, "static_content/set/year.html", context)
