from static_files.models import *
from static_files.methods.annexe_methods import create_random_key
from static_files.methods.subject_methods import CreateSubject
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


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
    if request.POST.get('filename', default=None):
        context['filename'] = request.POST['filename']
        context['key'] = create_random_key()
        context['path'] = build_path(context)
        if url != '':
            context['name'] = str(context['filename']) + '-' + str(context['key'])
        else:
            context['fileextension'] = (request.FILES['file'].name).split('.')[1]
            context['name'] = str(context['filename']) + '-' + str(context['key']) + '.' + str(context['fileextension'])
            context['raw_path'] = context['path'] + context['name']
            new_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(context['raw_path'], new_file)
            upload_file_url = fs.url(filename)
        # Create instance Static Content
        create_file(context, request)
        print(upload_file_url)
    return render(request, "static_content/add/add-file.html", context)


def __create_category(request, context):
    place = len(CategoryFile.objects.filter(subject=context['subject']))
    new_cat = CategoryFile.objects.filter(subject=context['subject'],\
                                          title=request.POST['new_category'])
    if not len(new_cat):
        new_cat = CategoryFile(subject=context['subject'],\
                               title=request.POST['new_category'],\
                               category=request.POST['list_category'],\
                               place=place)
        new_cat.save()
        context['category'] = new_cat
    else:
        context['category'] = new_cat[0]
    return new_cat


def file_select(request, context):
    context['subject'] = SubjectFile.objects.get(pk=request.POST['subject'])
    context['year'] = YearFile.objects.get(pk=request.POST['year'])
    context['semester'] = SemesterFile.objects.get(pk=request.POST['semester'])
    if not int(request.POST['category']):
        context['category'] = __create_category(request, context)
    else:
        context['category'] = CategoryFile.objects.get(pk=request.POST['category'])
    context['extensions'] = ExtensionFile.objects.all().order_by('type')
    context['step'] = 4
    return render(request, "static_content/add/add-file.html", context)


def category_select(request, context):
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    semester_obj = SemesterFile.objects.get(pk=request.POST['semester'])
    print(request.POST)
    if not int(request.POST['subject']):
        context = CreateSubject(context, request.POST['new_subject'], semester_obj.pk, year_obj.pk, School.objects.filter(school__exact=request.user.school)[0])
        subject_obj = context['new_subject_obj']
    else:
        subject_obj = SubjectFile.objects.get(pk=request.POST['subject'])
    context['year'] = year_obj
    context['semester'] = semester_obj
    context['step'] = 3
    context['subject'] = subject_obj
    context['categories'] = CategoryFile.objects.filter(subject=subject_obj).order_by('title')
    context['type'] = ['TD', 'Documents', 'Controles', 'QCM', 'Aide/Cours']
    return render(request, "static_content/add/add-file.html", context)


def subject_select(request, context):
    context['step'] = 2
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    semester_obj = SemesterFile.objects.get(pk=request.POST['semester'])
    school_obj = School.objects.filter(school__exact=request.user.school)[0]
    context['year'] = year_obj
    context['semester'] = semester_obj
    context['subjects'] = SubjectFile.objects.filter(year=year_obj, semester=semester_obj,  location=school_obj).order_by('subject')
    return render(request, "static_content/add/add-file.html", context)


def semester_select(request, context):
    context['step'] = 1
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    context['year'] = year_obj
    context['semesters'] = SemesterFile.objects.filter(semester__lte=year_obj.active_semester.semester).order_by('semester')
    return render(request, "static_content/add/add-file.html", context)


# Dispatch
def init_view(request):
    context = {}
    if request.POST:
        if request.POST.get('filename', default=None) or\
           request.POST.get('link', default=None):
            return create_instance(request, context)
        elif request.POST.get('category', default=None):
            return file_select(request, context)
        elif request.POST.get('subject', default=None):
            return category_select(request, context)
        elif request.POST.get('semester',default=None):
            return subject_select(request, context)
        elif request.POST.get('year', default=None):
            return semester_select(request, context)
    context['years'] = YearFile.objects.all().order_by('year')
    context['step'] = 0
    return render(request, "static_content/add/add-file.html", context)
