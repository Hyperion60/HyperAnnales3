from tokenlib.errors import MalformedTokenError, InvalidSignatureError, ExpiredTokenError
from HyperAnnales.settings import BASE_MEDIA_ROOT, KEY_TOKEN
from static_files.models import *
from static_files.methods.annexe_methods import update_git_direct
from static_files.methods.subject_methods import CreateSubject
from static_files.views.annexe_functions import create_random_key
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tokenlib

COLOR_FILE = [
    ('Fichier local', 'green'),
    ('Lien URL', 'blue'),
    ('Fichier distant', 'red'),
]


EXTENSION_FILE = [
    ('Document OpenOffice', 'doc'),
    ('Document Word', 'docx'),
    ('Document PDF', 'pdf'),
    ('Présentation OpenOffice', 'ppt'),
    ('Présentation PowerPoint', 'pptx'),
    ('Image PNG', 'png'),
    ('Image JPEG', 'jpeg'),
    ('Lien URL', 'url'),
]

manager = tokenlib.TokenManager(secret=KEY_TOKEN, timeout=3 * 60 * 60)


def build_path(context):
    path = str(context['school'].school) + "/"
    path += str(context['year'].year) + "/"
    path += str(context['semester'].semester) + "/"
    path += str(context['subject'].subject) + "/"
    return path


def create_instance(request, context):
    context['school'] = School.objects.get(school=request.user.school)
    context['year'] = YearFile.objects.get(pk=request.POST['year'])
    context['semester'] = SemesterFile.objects.get(pk=request.POST['semester'])
    context['subject'] = SubjectFile.objects.get(pk=request.POST['subject'])
    context['category'] = CategoryFile.objects.get(pk=request.POST['category'])
    context['url'] = request.POST['url']
    if request.POST.get('filename', default=None) or request.POST.get('url', default=None):
        context['filename'] = request.POST['filename']
        context['key'] = create_random_key()
        context['path'] = build_path(context)
        if request.user.is_superuser and request.POST['new_extension_type'] and request.POST['new_extension_extension']:
            context['extension'] = ExtensionFile(extension=request.POST['new_extension_extension'],
                                                 type=request.POST['new_extension_type']).save()
        try:
            if int(request.POST.get('color', '0')):
                try:
                    context['color'] = ContentColor.objects.get(pk=request.POST['color'])
                except ContentColor.DoesNotExist:
                    context['errors'].append("La classe de fichier demandée n'est pas disponible. "
                                             "La clé primaire n'existe pas.")
            else:
                if request.user.is_superuser:
                    context['color'] = ContentColor(type=request.POST['new_color_type'],
                                                    color=request.POST['new_color_color']).save()
                else:
                    context['errors'].append("Classe de fichier : champ non-renseigné")
        except KeyError:
            context['errors'].append("Classe de fichier : cas non-géré")
        except ValueError:
            context['errors'].append("Classe de fichier : Entrée invalide")

        if request.user.is_superuser and (not request.POST['color'] or not int(request.POST['color'])):
            context['color'] = ContentColor(type=request.POST['new_color_type'],
                                            color=request.POST['new_color_color']).save()
        if request.POST['color'] and int(request.POST['color']):
            try:
                context['color'] = ContentColor.objects.get(pk=request.POST['color'])
            except ContentColor.DoesNotExist:
                print("[LOG] Tentative de récupérer un ContentColor inexistant")
        if context['url'] != '':
            context['name'] = str(context['filename']) + '-' + str(context['key'])
            try:
                context['extension'] = ExtensionFile.objects.get(extension__exact="url")
            except ExtensionFile.DoesNotExist:
                if request.user.is_superuser:
                    context['extension'] = ExtensionFile(extension="url", type="Lien URL").save()
                else:
                    context['errors'].append("Les liens URL ne sont pas encore supportés.")

        else:
            context['fileextension'] = request.FILES['file'].name.split('.')[1]
            context['name'] = str(context['filename']) + '-' + str(context['key']) + '.' + str(context['fileextension'])
            context['raw_path'] = context['path'] + context['name']
            if not len(context['errors']):
                new_file = request.FILES['file']
                fs = FileSystemStorage()
                fs.save(root_path + context['raw_path'], new_file)
        create_file(context, request)
        if not len(context['errors']):
            context['message'] = "Fichier ajouté avec succès"
            if not context['url']:
                commit = "File({}): {}\nAuteur: {}".format(context['fileextension'], context['raw_path'], request.user)
                update_git_direct(context['raw_path'], BASE_MEDIA_ROOT, commit, context)
            return render(request, "static_content/admin/message_template.html", context)
    return render(request, "static_content/add/add-file.html", context)


def __create_category(request, context):
    place = int(request.POST['new_category_place'])
    if place <= 0:
        context['errors'].append(
            "Nouvelle catégorie : Place invalide, la place doit être un entier strictement positif")
        return None
    list_category = CategoryFile.objects.filter(subject=context['subject'])
    for category in list_category.order_by('place'):
        if category.place >= place:
            category.place += 1
            category.save()
    if place > len(list_category):
        place = len(list_category)

    title = request.POST['new_category_title']
    if len(title) > 150:
        context['errors'].append("Nouvelle catégorie : Le titre de la catégorie ne doit pas dépasser 150 charactères")
    for category in list_category:
        if title == category.title:
            context['errors'].append("Nouvelle catégorie : Une catégorie existe déjà avec ce titre.")
            return None

    if not int(request.POST['new_category_type']):
        try:
            color = CategoryColor(color=request.POST['new_type_color'], type=request.POST['new_type_type'])
            color.save()
        except ValueError:
            context['errors'].append("Nouveau type de catégorie: Champs invalides ou manquants.")
            return None
    else:
        try:
            color = CategoryColor.objects.get(pk=request.POST['new_category_type'])
        except CategoryColor.DoesNotExist:
            context['errors'].append("Nouvelle catégorie : Le type sélectionné est invalide.")
            return None

    new_cat = CategoryFile(subject=context['subject'], title=title, place=place, classe=color)
    new_cat.save()
    return new_cat


def file_select(request, context):
    context['subject'] = SubjectFile.objects.get(pk=request.POST['subject'])
    context['year'] = YearFile.objects.get(pk=request.POST['year'])
    context['semester'] = SemesterFile.objects.get(pk=request.POST['semester'])
    if not int(request.POST['category']) and request.user.is_staff:
        context['category'] = __create_category(request, context)
    else:
        context['category'] = CategoryFile.objects.get(pk=request.POST['category'])
    if not context['category']:
        context['step'] = 3
        context['categories'] = CategoryFile.objects.filter(subject=context['subject']).order_by('title')
        if request.user.is_staff:
            context['max'] = len(context['categories']) + 1
            context['colors'] = CategoryColor.objects.all().order_by('type')
        return render(request, "static_content/add/add-file.html", context)
    context['extensions'] = ExtensionFile.objects.all().order_by('type')
    context['colors'] = ContentColor.objects.all().order_by('type')
    context['step'] = 4
    return render(request, "static_content/add/add-file.html", context)


def category_select(request, context):
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    semester_obj = SemesterFile.objects.get(pk=request.POST['semester'])
    if request.user.is_superuser and not int(request.POST['subject']):
        context = CreateSubject(context, request.POST['new_subject'], semester_obj.pk, year_obj.pk,
                                School.objects.filter(school__exact=request.user.school)[0])
        subject_obj = context['new_subject_obj']
    else:
        subject_obj = SubjectFile.objects.get(pk=request.POST['subject'])
    context['year'] = year_obj
    context['semester'] = semester_obj
    context['step'] = 3
    context['subject'] = subject_obj
    context['categories'] = CategoryFile.objects.filter(subject=subject_obj).order_by('title')
    if request.user.is_staff:
        context['max'] = len(context['categories']) + 1
        context['types'] = CategoryColor.objects.all().order_by('type')
    return render(request, "static_content/add/add-file.html", context)


def subject_select(request, context):
    context['step'] = 2
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    semester_obj = SemesterFile.objects.get(pk=request.POST['semester'])
    school_obj = School.objects.filter(school__exact=request.user.school)[0]
    context['year'] = year_obj
    context['semester'] = semester_obj
    context['subjects'] = SubjectFile.objects.filter(year=year_obj, semester=semester_obj,
                                                     location=school_obj).order_by('subject')
    return render(request, "static_content/add/add-file.html", context)


def semester_select(request, context):
    context['step'] = 1
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    context['year'] = year_obj
    context['semesters'] = SemesterFile.objects.filter(semester__lte=year_obj.active_semester.semester).order_by(
        'semester')
    return render(request, "static_content/add/add-file.html", context)


# Dispatch
def init_view(request):
    context = {'errors': []}
    if request.POST:
        if request.POST.get('filename', default=None) or \
                request.POST.get('url', default=None):
            return create_instance(request, context)
        elif request.POST.get('category', default=None):
            return file_select(request, context)
        elif request.POST.get('subject', default=None):
            return category_select(request, context)
        elif request.POST.get('semester', default=None):
            return subject_select(request, context)
        elif request.POST.get('year', default=None):
            return semester_select(request, context)
    context['years'] = YearFile.objects.all().order_by('year')
    context['step'] = 0
    return render(request, "static_content/add/add-file.html", context)


def get_token(user, random_key):
    return manager.make_token({'user': user.pk, 'key': random_key})


def verify_token(context, user, token):
    try:
        context = manager.parse_token(token)
    except (MalformedTokenError, InvalidSignatureError):
        context['errors'].append("Token invalide.")
        return False
    except ExpiredTokenError:
        context['errors'].append("Token expiré, veuillez raffraichir la page.")
        return False
    if context['user'] != user.pk:
        context['errors'].append("L'utilisateur ne correspond pas au token utilisé.")
        return False
    return True
