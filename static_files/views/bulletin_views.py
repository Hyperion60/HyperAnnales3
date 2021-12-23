from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from static_files.methods.bulletin_methods import create_information, update_information, delete_information
from static_files.models import Bulletin, YearFile


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

        if update_information(request, context):
            context['message'] = "Modification effectuée avec succès."
            return render(request, "static_content/admin/message_template.html", context)
        return render(request, "static_content/admin/message_template.html", context)

    context['date'] = context['bulletin'].date_expiry.strftime("%d/%m/%Y")
    context['years'] = YearFile.objects.all()
    if context['bulletin'].year:
        context['years'] = context['years'].exclude(pk=context['bulletin'].year.pk)
    return render(request, "static_content/change/change-bulletin.html", context)


def DeleteInformation(request, pk):
    context = {
        'errors': [],
        'next': request.GET.get('next', '')
    }

    if request.user != context['bulletin'].author and not request.user.is_staff:
        context['errors'].append("Vous n'avez pas l'authorisation de modifier cette instance.")
        return render(request, "static_content/admin/message_template.html", context)

    try:
        context['bulletin'] = Bulletin.objects.get(pk=pk)
    except Bulletin.DoesNotExist:
        context['errors'].append("Le bulletin d'information demandée est introuvable, la clé primaire n'existe pas.")
        return render(request, "static_content/admin/message_template.html", context)

    if request.POST:
        if request.POST.get('cancel', None):
            return redirect(context['next'])
        if delete_information(request, context):
            context['message'] = "Suppression effectuée avec succès."
        else:
            context['errors'].append("Echec de la suppression du bulletin.")
        return render(request, "static_content/admin/message_template.html", context)

    return render(request, "static_content/del/del-bulletin.html", context)
