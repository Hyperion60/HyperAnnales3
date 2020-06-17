from django.db import models
from accounts.models import Account

import os
from datetime import datetime
from random import randint
from shutil import copyfile
# Create your models here.

STATIC_PATH = "/home/static_HA/epita/"


class SemesterFile(models.Model):
    semester = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.semester)


class YearFile(models.Model):
    year = models.IntegerField(unique=True)
    active_semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)

    def __str__(self):
        return str(self.year)


class SubjectFile(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)
    year = models.ForeignKey(YearFile, models.CASCADE, default=None)

    def __str__(self):
        return self.subject


class CategoryFile(models.Model):
    LIST_CAT = (
        ('TD', 'blue'),
        ('Documents', 'green'),
        ('Controles', 'red'),
        ('QCM', 'blue'),
        ('Aide/Cours', 'green'),
    )
    category = models.CharField(max_length=10, choices=LIST_CAT, default=None)
    title = models.CharField(max_length=150)
    place = models.IntegerField()
    subject = models.ForeignKey(SubjectFile, models.CASCADE, default=None)
    semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)
    year = models.ForeignKey(YearFile, models.CASCADE, default=None)


class ExtensionFile(models.Model):
    extension = models.CharField(max_length=5, unique=True)
    type = models.CharField(max_length=50)


class StaticContent(models.Model):
    year = models.ForeignKey(YearFile, models.CASCADE, default=None)
    semester = models.ForeignKey(SemesterFile, models.CASCADE, default=None)
    subject = models.ForeignKey(SubjectFile, models.CASCADE, default=None)
    category = models.ForeignKey(CategoryFile, models.CASCADE, default=None)
    name = models.CharField(max_length=255, default=None)
    path = models.CharField(max_length=255, default=None)
    date = models.DateField()
    weight = models.IntegerField()
    author = models.ForeignKey(Account, models.CASCADE, default=None)
    random_key = models.IntegerField(unique=True)
    extension = models.ForeignKey(ExtensionFile, models.CASCADE, default=None)

    def __str__(self):
        return self.name


def create_subject(request):
    subject = request.POST['subject']
    subject_s = SubjectFile.objects.filter(subject__exact=subject)
    if not len(subject_s):
        new_subject = SubjectFile(subject=subject)
        new_subject.save(using='pdf_ref')


def create_file(request, raw_path):
    year = request.POST['year']
    semester = request.POST['semester']
    subject = request.POST['subject']
    name = request.POST['name']
    date = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    weight = round(os.stat(raw_path).st_size / 1024)
    author = request.user
    key = 0
    while key == 0 and len(StaticContent.objects.filter(random_key__exact=key)):
        key = randint(1, 999999)
    path = STATIC_PATH + str(year) + "/" + str(semester) + "/" + str(subject) + "/" + str(name) + "-" + str(key) + ".pdf"
    file = StaticContent(year=year,
                         semester=semester,
                         subject=subject,
                         name=name,
                         date=date,
                         weight=weight,
                         author=author,
                         ramdom_key=key)
    file.save(using='pdf_ref')
    copyfile(raw_path, path)
    os.remove(raw_path)
