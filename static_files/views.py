from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from static_files.models import YearFile, SemesterFile,SubjectFile, StaticContent
from static_files.forms import CreateYearForm

# Create your views here.


@login_required(login_url="/login/")
def static_admin(request):
    if not request.user.is_contributor:
        raise PermissionDenied
    context = {}
    if request.user.is_staff:
        context['years'] = YearFile.objects.all()
        context['subjects'] = SubjectFile.objects.all()
    context['contribution'] = StaticContent.objects.filter(author=request.user).order_by('name')
    if not len(context['years']):
        context['years'] = None
    if not len(context['subjects']):
        context['subjects'] = None
    if not len(context['contribution']):
        context['contribution'] = None
    return render(request, "static_content/admin/index.html", context)


def __search_create_semester(semester):
    test_s = SemesterFile.objects.filter(semester__exact=semester)
    if not len(test_s):
        new_semester = SemesterFile.objects.filter(semester=semester)
        new_semester.save()
        return new_semester
    return test_s[0]


def __create_class_year(year, active_semester):
    test_s = __search_create_semester(active_semester)
    test_y = YearFile.objects.filter(year__exact=year)
    if not len(test_y):
        new_promo = YearFile(year=year, active_semester=test_s)
        new_promo.save()


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
            __create_class_year(year, semester)
            context['message'] = "Le semestre actuel a bien été actualisé."
            return render(request, "static_content/admin/index.html", context)
    else:
        context['form'] = CreateYearForm()
    return render(request, "static_content/add/year.html", context)
