from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from static_files.methods.semester_methods import create_semester


@login_required(login_url="/login/")
def CreateSemesterView(request):
    if not request.user.is_staff:
        raise PermissionDenied
    context = {}
    error = False
    if request.POST:
        semester = 0
        try:
            semester = int(request.POST['semester'])
        except KeyError:
            context['error'] = "Entrez un numéro de semestre"
            error = True
        if not error:
            if 0 > semester < 11:
                create_semester(semester)
                return render(request, "static_content/admin/message-template.html",
                              {'message': "Le semestre a bien été créé"})
            else:
                error = True
                context['error'] = "Numéro de semestre invalide"
    if not error:
        context['error'] = None
    return render(request, "static_content/add/add-semester.html", context)
