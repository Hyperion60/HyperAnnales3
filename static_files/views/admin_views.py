from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from static_files.models import YearFile, SubjectFile, StaticContent

# Create your views here.


@login_required(login_url="/login/")
def static_admin(request):
    if not request.user.is_contributor:
        raise PermissionDenied
    context = {}
    context['years'] = None
    context['subjects'] = None
    context['contribution'] = None
    if request.user.is_staff:
        if request.user.is_admin:
            context['years'] = YearFile.objects.all().order_by('year')
            context['subjects'] = SubjectFile.objects.all().order_by('subject')
            context['contribution'] = StaticContent.objects.filter(file__author=request.user).order_by('name')
        else:
            context['years'] = YearFile.objects.filter(school_school__exact=(request.user.school)).order_by('year')
            context['subjects'] = SubjectFile.objects.filter(school_school__exact=(request.user.school)).order_by('subject')
            context['contribution'] = StaticContent.objects.filter(file__author=request.user).order_by('name')
    return render(request, "static_content/admin/index.html", context)

