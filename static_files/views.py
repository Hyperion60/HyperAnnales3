from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from static_files.models import YearFile, SubjectFile, StaticContent
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


@login_required(login_url="/login/")
def create_year(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    if request.POST:
        form = CreateYearForm(request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            print(form)
    else:
        context['form'] = CreateYearForm()
    return render(request, "static_content/add/year.html", context)
