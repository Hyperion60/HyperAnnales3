from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.datastructures import MultiValueDictKeyError

from static_files.models import School, YearFile, SemesterFile, SubjectFile
from static_files.form.subject_forms import SetSubject
from static_files.methods.subject_methods import CreateSubject, UpdateSubject, DeleteSubject


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
def UpdateSubjectView(request, pk):
    context = {
        'errors': [],
        'next': request.GET.get('next', '')
    }

    try:
        context['subject'] = SubjectFile.objects.get(pk=pk)
    except SubjectFile.DoesNotExist:
        context['errors'].append("La clé demandée n'existe pas.")
        return render(request, "static_content/admin/message_template.html", context)

    if not request.user.is_staff:
        context['errors'].append("Vous n'avez pas l'authorisation de modifier cette instance.")
        return render(request, "static_content/admin/message_template.html", context)

    context['years'] = YearFile.objects.all().order_by("year")
    context['semesters'] = SemesterFile.objects.all().order_by("semester")
    context['schools'] = School.objects.all().order_by("school")

    if request.POST:
        try:
            context['title'] = request.POST['title']
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'titre' manquant.")

        try:
            context['school'] = School.objects.get(pk=request.POST['school'])
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'école' manquant.")
        except School.DoesNotExist:
            context['errors'].append("L'école demandée n'existe pas. Clé primaire introuvable.")

        try:
            context['year'] = YearFile.objects.get(pk=request.POST['year'])
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'année' manquant.")
        except YearFile.DoesNotExist:
            context['errors'].append("L'année demandée n'existe pas. Clé primaire introuvable.")

        try:
            context['semester'] = SemesterFile.objects.get(pk=request.POST['semester'])
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'semestre' manquant.")
        except SemesterFile.DoesNotExist:
            context['errors'].append("Le semestre demandé n'existe pas. Clé primaire introuvable.")

        if not len(context['subject']):
            context['errors'].append("Le titre de la matière ne peut être vide.")

        if len(context['errors']):
            return render(request, "static_content/change/change-subject.html", context)

        if UpdateSubject(request, context):
            context['message'] = "Modification effectuée avec succès."
            return render(request, "static_content/admin/message_template.html", context)
        return render(request, "static_content/change/change-subject.html", context)
    return render(request, "static_content/change/change-subject.html", context)


@login_required(login_url="/login/")
def DeleteSubjectView(request, pk):
    context = {
        'errors': [],
        'next': request.GET.get('next', '')
    }

    if not request.user.is_staff:
        context['errors'].append("Vous n'avez l'authorisation de supprimer cette instance.")
        return render(request, "static_content/admin/message_template.html", context)

    try:
        context['subject'] = SubjectFile.objects.get(pk=pk)
    except SubjectFile.DoesNotExist:
        context['errors'].append("La matière demandée n'existe pas. Clé primaire introuvable.")
        return render(request, "static_content/admin/message_template.html", context)

    if request.POST:
        if request.POST.get('cancel', None):
            return redirect(context['next'])
        if DeleteSubject(request, context):
            context['message'] = "Suppression effectuée avec succès."
        else:
            context['errors'].append("Echec de la suppression de la matière.")
        return render(request, "static_content/admin/message_template.html", context)

    return render(request, "static_content/del/del-subject.html", context)
