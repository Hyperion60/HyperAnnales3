from django.db import models, IntegrityError
from accounts.models import Account
from HyperAnnales.settings import BASE_MEDIA_ROOT

import os
from datetime import datetime
from static_files.methods.annexe_methods import school_file_count__year
from static_files.methods.extension_methods import template_choice, open_file

STATIC_PATH = "/home/static_HA/epita/"


class School(models.Model):
    school = models.CharField(max_length=30, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.school)


class SemesterFile(models.Model):
    semester = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.semester)


class YearFile(models.Model):
    year = models.IntegerField(unique=True)
    active_semester = models.ForeignKey(SemesterFile, models.CASCADE, default=1)

    def __str__(self):
        return str(self.year)

    def count(self, school):
        return school_file_count__year(school, self)


class SubjectFile(models.Model):
    subject = models.CharField(max_length=100, unique=False)
    semester = models.ForeignKey(SemesterFile, models.CASCADE, default=1)
    year = models.ForeignKey(YearFile, models.CASCADE, default=1)
    location = models.ForeignKey(School, models.CASCADE, default=1)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.subject

    def school(self):
        return self.location


class CategoryColor(models.Model):
    color = models.CharField(max_length=15, unique=False, default="blue")
    type = models.CharField(max_length=45, unique=True, default="default_type")


class CategoryFile(models.Model):
    title = models.CharField(max_length=150, unique=False)
    place = models.IntegerField()
    subject = models.ForeignKey(SubjectFile, models.CASCADE, default=0)
    classe = models.ForeignKey(CategoryColor, models.CASCADE, default=None)

    def semester_obj(self):
        return self.subject.semester

    def semester(self):
        return self.subject.semester.semester

    def year_obj(self):
        return self.subject.year

    def year(self):
        return self.subject.year.year

    def school_obj(self):
        return self.subject.location

    def school(self):
        return self.subject.location.school

    def __str__(self):
        return self.title


class ExtensionFile(models.Model):
    extension = models.CharField(max_length=10, unique=True)  # Name
    type = models.CharField(max_length=50)
    mobile_comp = models.BooleanField(default=True)

    def __str__(self):
        return self.type

    def template(self, token, static_file):
        return template_choice(self, token, static_file)

    def token(self):
        return open_file(self.pk)


class StaticFile(models.Model):
    url = models.CharField(max_length=1024, default='')
    path = models.CharField(max_length=1024, default='')
    date = models.DateTimeField()
    filename = models.CharField(max_length=255, default='')
    weight = models.IntegerField(default=0)
    author = models.ForeignKey(Account, models.CASCADE, default=1)
    randomkey = models.IntegerField(unique=True)
    extension = models.ForeignKey(ExtensionFile, models.CASCADE, default=1)
    content = models.ForeignKey('StaticContent', models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.filename


class ContentColor(models.Model):
    color = models.CharField(max_length=20, default="blue")
    type = models.CharField(max_length=45, default="default_type")

    def __str__(self):
        return self.type


class StaticContent(models.Model):
    category = models.ForeignKey(CategoryFile, models.CASCADE, default=0)
    classe = models.ForeignKey(ContentColor, models.CASCADE, null=False, default=None)
    name = models.CharField(max_length=255, default='Default Name')
    place = models.IntegerField(default=0)  # Place into categoryFile
    file = models.ForeignKey(StaticFile, models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def key(self):
        if self.file:
            return self.file.randomkey
        return None

    def color(self):
        return self.classe.color

    def subject(self):
        return self.category.subject

    def semester_obj(self):
        return self.category.semester_obj()

    def semester(self):
        return self.category.semester()

    def year_obj(self):
        return self.category.year_obj()

    def year(self):
        return self.category.year()


class Bulletin(models.Model):
    title = models.CharField(max_length=250, default='default_title')
    body = models.TextField(default='default body')
    location = models.ForeignKey(School, models.CASCADE, null=False, blank=False)
    year = models.ForeignKey(YearFile, models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    date_expiry = models.DateTimeField()
    author = models.ForeignKey(Account, models.CASCADE, default=1)

    def __str__(self):
        return "School({}): {} => {}".format(self.year, self.location, self.title)


class UnsecureFile(models.Model):
    title = models.CharField(max_length=120, default='default_title')
    url = models.CharField(max_length=1024, default='')
    filename = models.CharField(max_length=255, unique=True, default='')
    author = models.ForeignKey(Account, models.CASCADE, default=1)
    bulletin = models.ForeignKey(Bulletin, models.CASCADE, null=True, blank=True)
    extension = models.ForeignKey(ExtensionFile, models.CASCADE, default=1)

    def __str__(self):
        return self.title


def create_subject(request):
    subject = request.POST['subject']
    subject_s = SubjectFile.objects.filter(subject__exact=subject)
    if not len(subject_s):
        new_subject = SubjectFile(subject=subject)
        new_subject.save()


def check_extension(context):
    if context['url']:
        try:
            context['extension'] = ExtensionFile.objects.get(extension__exact="url")
        except ExtensionFile.DoesNotExist:
            context['errors'].append("Extension du fichier non supportée (instance extension non trouvée)")
            return False
    else:
        try:
            context['extension'] = ExtensionFile.objects.get(extension__exact=context['fileextension'])
        except ExtensionFile.DoesNotExist:
            context['errors'].append("Extension du fichier ({}) non supportée "
                                     "(instance extension non trouvée)".format(context['fileextension']))
            return False
    return True


def create_file(context, request):
    # Check extension
    if not check_extension(context):
        return
    if context['extension'].extension == "url":
        new_static_file = StaticFile(url=context['url'],
                                     date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     filename=context['filename'],
                                     author=request.user,
                                     randomkey=context['key'],
                                     extension=context['extension'])
    else:
        new_static_file = StaticFile(path=context['path'],
                                     date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     filename=context['filename'],
                                     weight=round(os.stat(BASE_MEDIA_ROOT + context['raw_path']).st_size / 1024),
                                     author=request.user,
                                     randomkey=context['key'],
                                     extension=context['extension'])
    try:
        new_static_file.save()
    except IntegrityError:
        context['errors'].append("Echec de la sauvegarde de l'instance (StaticFile).")

    new_static_content = StaticContent(category=context['category'],
                                       classe=context['color'],
                                       name=context['filename'],
                                       place=len(StaticContent.objects.filter(category=context['category'])),
                                       file=new_static_file)
    try:
        new_static_content.save()
        new_static_file.content = new_static_content
        new_static_file.save()
        new_static_content.category.subject.location.count += 1
        new_static_content.category.subject.location.save()
    except IntegrityError:
        context['errors'].append("Echec de la sauvegarde de l'instance (StaticContent).")
