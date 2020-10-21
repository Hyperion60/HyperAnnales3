from static_files.models import *


def school_file_count(school):
    list_subject = SubjectFile.objects.filter(location_school__exact=school.school)
    file_sum = 0;
    for subj in list_subject:
        file_sum += subj.count
    return file_sum

def school_file_count__year(school, year):
    list_subject = SubjectFile.objects.filter(location_school__exact=school.school,\
                                              year_year__exact=year.year)
    file_sum = 0;
    for subj in list_subject:
        file_sum += subj.count
    return file_sum

def create_random_key():
    n = 0;
    while not n and len(StaticFile.objects.filter(randomkey__exact=n)):
        n = randint(1, 999999)
    return n
