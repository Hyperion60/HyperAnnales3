from static_files.models import *
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def __build_path(context):
    path = "/" + context['school'] + "/"
    path += context['year'] + "/"
    path += context['semester'] + "/"
    path += context['subject'] + "/"
    return path
    
def __create_key():
    key = 0
    while not key and len(StaticContent.objects.filter(random_key__exact=key)):
        key = randint(1, 999999)
    return key


def __create_new_extension(request):
    is_exist = request.POST['new_extension']
    list_extension = None
    if is_exist:
        list_extension = ExtensionFile.objects.filter(extension__exact=request.POST['new_extension'])
    if not is_exist or not len(list_extension):
        new_extend = ExtensionFile(extension=request.POST['new_extension'],
                                   type=request.POST['proc_type'])
        new_extend.save()
        return new_extend
    return list_extension[0]


def create_instance(request, context):
    context['school'] = SchoolFile.objects.filter(school__exact=request.user.school)
    context['year'] = YearFile.objects.get(pk=request.POST['year'])
    context['semester'] = SemesterFile.objects.get(pk=request.POST['semester'])
    context['subject'] = SubjectFile.objects.get(pk=request.POST['subject'])
    context['category'] = CategoryFile.objects.get(pk=request.POST['category'])
    context['title'] = str(request.POST['title'])
    if request.POST['new_extension']:
        context['extension'] = __create_new_extension(request)
    else:
        context['extension'] = ExtensionFile.objects.get(pk=request.POST['extension'])
    if request.POST.get('filename', default=None):
        key = __create_key()
        print(request.FILES)
        new_file = request.FILES['file']
        fs = FileSystemStorage()
        file_name = (context['title'] + "-" + str(key) + "." + context['extension'])
        filename = fs.save(__build_path() + file_name, new_file)
        upload_file_url = fs.url(filename)
        # Create instance File Content
        new_staticfile = StaticFile(path=build_path(context),
                                    date=datetime.now().strftime("%d-%m-%Y_%H:%M:%S"),
                                    filename=context['title'],
                                    weight=new_file._size,
                                    author=request.user,
                                    random_key=key,
                                    extension=context['extension'])
        new_staticfile.save()
        # Create instance Static Content
        new_content = StaticContent(school=context['school'],
                                    year=context['year'],
                                    semester=context['semester'],
                                    subject=context['subject'],
                                    category=context['category'],
                                    name=context['title'],
                                    file=new_staticfile)
        new_content.save()
        new_staticfile.content = new_content
        new_staticfile.save()
        print(upload_file_url)
    return render(request, "static_content/add/add-file.html", context)


def __create_category(request, context):
    place = len(CategoryFile.objects.filter(year=context['year'],\
                                            semester=context['semester'],\
                                            subject=context['subject']))
    new_cat = CategoryFile.objects.filter(year=context['year'],\
                                            semester=context['semester'],\
                                            subject=context['subject'],\
                                            title=request.POST['new_category'])
    if not len(new_cat):
        new_cat = CategoryFile(year=context['year'],\
                               semester=context['semester'],\
                               subject=context['subject'],\
                               title=request.POST['new_category'],\
                               category=request.POST['list_category'],\
                               place=place)
        new_cat.save()
        context['category'] = new_cat
    else:
        context['category'] = new_cat[0]
    return new_cat

# Add select extension
def file_select(request, context):
    context['subject'] = SubjectFile.objects.get(pk=request.POST['subject'])
    context['year'] = YearFile.objects.get(pk=request.POST['year'])
    context['semester'] = SemesterFile.objects.get(pk=request.POST['semester'])
    if not int(request.POST['category']):
        context['category'] = __create_category(request, context)
    else:
        context['category'] = CategoryFile.objects.get(pk=request.POST['category'])
    context['extension'] = ExtensionFile.objects.all().order_by('extension')
    context['type'] = Extension.objets.distinct('type').order_by('type')
    context['step'] = 4
    return render(request, "static_content/add/add-file.html", context)


def __create_subject(request, context, year_obj, semester_obj):
    new_sub = SubjectFile.objects.filter(year=year_obj, semester=semester_obj,\
                                          subject=request.POST['new_subject'])
    if not len(new_sub):
        new_sub = SubjectFile(year=year_obj, semester=semester_obj,\
                              subject=request.POST['new_subject'])
        new_sub.save()
        context['subject'] = new_sub
    else:
        context['subject'] = new_sub[0]
    return new_sub


def category_select(request, context):
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    semester_obj = SemesterFile.objects.get(pk=request.POST['semester'])
    print(request.POST)
    if not int(request.POST['subject']):
        subject_obj = __create_subject(request, context, year_obj, semester_obj)
    else:
        subject_obj = SubjectFile.objects.get(pk=request.POST['subject'])
    context['year'] = year_obj
    context['semester'] = semester_obj
    context['step'] = 3
    context['subject'] = subject_obj
    context['categories'] = CategoryFile.objects.filter(year=year_obj, semester=semester_obj, subject=subject_obj).order_by('title')
    context['type'] = ['TD', 'Documents', 'Controles', 'QCM', 'Aide/Cours']
    return render(request, "static_content/add/add-file.html", context)


def subject_select(request, context):
    context['step'] = 2
    year_obj = YearFile.objects.get(pk=request.POST['year'])
    semester_obj = SemesterFile.objects.get(pk=request.POST['semester'])
    context['year'] = year_obj
    context['semester'] = semester_obj
    context['subjects'] = SubjectFile.objects.filter(year=year_obj,\
                          semester=semester_obj).order_by('subject')
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
