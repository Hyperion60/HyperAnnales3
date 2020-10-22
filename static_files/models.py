from django.db import models
from accounts.models import Account
from HyperAnnales.settings import MEDIA_ROOT as root_path
from static_files.methods.annexe_methods import *

import os
from datetime import datetime
from random import randint
from shutil import copyfile
# Create your models here.

STATIC_PATH = "/home/static_HA/epita/"


class School(models.Model):
    school = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.school)

    def count(self):
        return school_file_count(self)

class SemesterFile(models.Model):
    semester = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.semester)


class YearFile(models.Model):
    year = models.IntegerField(unique=True)
    active_semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)

    def __str__(self):
        return str(self.year)

    def count(self, school):
        return school_file_count__year(school, self)


class SubjectFile(models.Model):
    subject = models.CharField(max_length=100, unique=False)
    semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)
    year = models.ForeignKey(YearFile, models.CASCADE, default=None)
    location = models.ForeignKey(School, models.CASCADE, default=None)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.subject

    def school(self):
        return self.location


class CategoryFile(models.Model):
    LIST_CAT = (
        ('TD', 'blue'),
        ('Documents', 'green'),
        ('Controles', 'red'),
        ('QCM', 'blue'),
        ('Aide/Cours', 'green'),
    )
    category = models.CharField(max_length=10, choices=LIST_CAT, default=None)
    title = models.CharField(max_length=150, unique=False)
    place = models.IntegerField()
    subject = models.ForeignKey(SubjectFile, models.CASCADE, default=None)


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


class ExtensionFile(models.Model):
    extension = models.CharField(max_length=5, unique=True)
    type = models.CharField(max_length=50)


class StaticFile(models.Model):
    path = models.CharField(max_length=255, default=None)
    date = models.DateField()
    filename = models.CharField(max_length=255, default=None)
    weight = models.IntegerField()
    author = models.ForeignKey(Account, models.CASCADE, default=None)
    randomkey = models.IntegerField(unique=True)
    extension = models.ForeignKey(ExtensionFile, models.CASCADE, default=None)
    content = models.ForeignKey('StaticContent', models.CASCADE, default=None)


class StaticContent(models.Model):
#school = models.ForeignKey(School, models.CASCADE, default=None)
#year = models.ForeignKey(YearFile, models.CASCADE, default=None)
#semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)
#subject = models.ForeignKey(SubjectFile, models.CASCADE, default=None)
    category = models.ForeignKey(CategoryFile, models.CASCADE, default=None)
    name = models.CharField(max_length=255, default=None)
    place = models.IntegerField() # Place into categoryFile
    file = models.ForeignKey(StaticFile, models.CASCADE, default=None)

    def __str__(self):
        return self.name

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


def create_subject(request):
    subject = request.POST['subject']
    subject_s = SubjectFile.objects.filter(subject__exact=subject)
    if not len(subject_s):
        new_subject = SubjectFile(subject=subject)
        new_subject.save()


def create_file(context, request):
    # Check extension (create if necessary)
    context['extensionfile'] = check_extension(context['extension'])
    new_staticFile = StaticFile(path=context['path'],
                                date=datetime.now().strftime("%d-%m-%Y_%H:%M:%S"),
                                filename=context['filename'],
                                weight=round(os.path(root_path + context['raw_path']).st_size / 1024),
                                author=request.user,
                                randomkey=context['key'],
                                extension=ExtensionFile.objects.filter(extension__exact=context['extension'])[0])
    new_staticFile.save()

    new_staticContent = StaticContent(category=context['category'],
                                      name=context['filename'],
                                      place=len(StaticContent.objects.filter(category=context['category'])),
                                      file=new_staticFile)
    new_staticContent.save()
    new_staticFile.content = new_staticContent
    new_staticFile.save()

