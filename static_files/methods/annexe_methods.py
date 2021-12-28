from apscheduler.schedulers.blocking import BlockingScheduler
from git import Repo
from static_files.models import *
from pytz import utc

sched = BlockingScheduler(timezone=utc)


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


def update_git_direct(file_path, root, commit=None, log=None):
    if log is None:
        log = {}
    PATH = root + ".git"
    COMMIT_MESSAGE = "Add file"
    try:
        repo = Repo(PATH)
        repo.git.add(file_path)
        if not commit:
            repo.index.commit(COMMIT_MESSAGE)
        else:
            repo.index.commit(commit)
        origin = repo.remote(name='origin')
        origin.push()
        log['message'] += "\nAjout du fichier dans le répertoire de sauvegarde réalisé avec succès"
    except:
        log['error'] += "Echec de l'ajout du fichier dans le répertoire de sauvegarde"


def school_file_count(school):
    list_subject = SubjectFile.objects.filter(location_school__exact=school.school)
    file_sum = 0
    for subj in list_subject:
        file_sum += subj.count
    return file_sum


def school_file_count__year(school, year):
    list_subject = SubjectFile.objects.filter(location_school__exact=school.school,
                                              year_year__exact=year.year)
    file_sum = 0
    for subj in list_subject:
        file_sum += subj.count
    return file_sum
