from apscheduler.schedulers.blocking import BlockingScheduler
from git import Repo
from static_files.models import *


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def update_git():
    PATH = "/media/static_HA/.git"
    COMMIT_MESSAGE = "Add file"
    try:
        repo = Repo(PATH)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print("Error during push")
    return


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
