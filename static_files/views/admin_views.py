from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.methods.bulletin_methods import list_bulletin_admin_view
from static_files.models import YearFile, SubjectFile, StaticContent, SemesterFile, Bulletin

# Create your views here.


@login_required(login_url="/login/")
def static_admin(request):
    if not request.user.is_contributor:
        raise PermissionDenied
    context = {
        'years': None,
        'subjects': None,
        'contribution': None,
        'bulletins': None
    }
    if request.user.is_staff:
        context['years'] = YearFile.objects.all().order_by('year')
        context['semesters'] = SemesterFile.objects.all().order_by('semester')
        context['subjects'] = SubjectFile.objects.all().order_by('subject')
        context['bulletins'] = Bulletin.objects.all().order_by('title')

    context['bulletins'] = list_bulletin_admin_view(request)
    context['contribution'] = StaticContent.objects.filter(file__author=request.user).order_by('name')
    return render(request, "static_content/admin/index.html", context)

