from django.db import models
from accounts.models import Account

import os
from datetime import datetime
from random import randint
from shutil import copyfile
# Create your models here.

STATIC_PATH = "/home/static_HA/epita/"


class YearFile(models.Model):
    year = models.IntegerField()


class SemesterFile(models.Model):
    semester = models.IntegerField()


class SubjectFile(models.Model):
    subject = models.CharField(max_length=100)


class StaticContent(models.Model):
    year = models.ForeignKey(YearFile, models.CASCADE)
    semester = models.ForeignKey(SemesterFile, models.CASCADE)
    subject = models.ForeignKey(SubjectFile, models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    date = models.DateField()
    weight = models.IntegerField()
    author = models.ForeignKey(Account, models.CASCADE)
    random_key = models.IntegerField()


def create_year(request):
    year = int(request.POST['year'])
    # test_y = YearFile.objects.filter(year__exact=year)
    # if not len(test_y):
    new_promo = YearFile(year=year)
    new_promo.save(using='pdf_ref')


def create_semester(request):
    semester = int(request.POST['year'])
    new_semester = SemesterFile(semester=semester)
    new_semester.save(using='pdf_ref')


def create_subject(request):
    subject = request.POST['subject']
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
