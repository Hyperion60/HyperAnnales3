from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from static_files.methods.bulletin_methods import create_information
from static_files.models import Bulletin, School, YearFile


@login_required(login_url="/login/")
def CreateInformation(request, school, year=None):
    context = {
        'errors': [],
        'school': school,
        'year': year
    }
    if request.POST:
        if create_information(request, context):
            context['next'] = "/{}/".format(school)
            if year:
                context['next'] = "/{}/{}/".format(school, year)
            return render(request, "static_content/admin/message_template.html", context)
    try:
        context['body'] = request.POST['body']
        context['title'] = request.POST['title']
    except MultiValueDictKeyError:
        pass
    return render(request, "static_content/add/add-information.html", context)


@login_required(login_url="/login/")
def UpdateInformation(request, pk):
    context = {
        'errors': [],
        'next': request.GET.get('next', '')
    }
    try:
        context['bulletin'] = Bulletin.objects.get(pk=pk)
    except Bulletin.DoesNotExist:
        context['errors'].append("La clé demandée n'existe pas.")
        return render(request, "static_content/admin/message_template.html", context)

    if request.user != context['bulletin'].author and not request.user.is_staff:
        context['errors'].append("Vous n'avez pas l'authorisation de modifier cette instance.")
        return render(request, "static_content/admin/message_template.html", context)

    if request.POST:
        try:
            context['title'] = request.POST['title']
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'titre' manquant.")
        try:
            context['body'] = request.POST['body']
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'body' manquant.")
        try:
            context['school'] = School.objects.get(pk=request.POST['school'])
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'school' manquant.")
        except School.DoesNotExist:
            context['errors'].append("L'école demandée n'existe pas. Clé primaire introuvable")
        try:
            if request.POST['year']:
                context['year'] = YearFile.objects.get(pk=request.POST['year'])
            else:
                context['year'] = None
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'year' manquant.")
        except YearFile.DoesNotExist:
            context['errors'].append("L'année demandée n'existe pas. Clé primaire introuvable")
        try:
            context['date'] = datetime.strptime(request.POST['date'], "%d/%m/%Y")
        except MultiValueDictKeyError:
            context['errors'].append("Champ 'date' manquant.")
        except ValueError:
            context['errors'].append("Erreur dans la date.")

        if len(context['errors']):
            return render(request, "static_content/change/change-bulletin.html", context)

        if create_information(request, context):
            return render(request, "static_content/admin/message_template.html", context)
        return render(request, "static_content/admin/message_template.html", context)

    context['date'] = context['bulletin'].date_expiry.strftime("%d/%m/%Y")
    return render(request, "static_content/change/change-bulletin.html", context)

