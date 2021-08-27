from apscheduler.schedulers.blocking import BlockingScheduler
from git import Repo
from static_files.models import StaticContent, SubjectFile, StaticFile
from random import randint

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


def update_git_direct(file_path, commit=None, log={}):
    PATH = "/media/static_HA/.git"
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
    list_subject = SubjectFile.objects.filter(location_school__exact=school.school,\
                                              year_year__exact=year.year)
    file_sum = 0
    for subj in list_subject:
        file_sum += subj.count
    return file_sum


def create_random_key():
    n = 0
    while n == 0 and len(StaticFile.objects.filter(randomkey__exact=n)):
        n = randint(1, 999999)
    return n


def get_color(static_content):
    if not type(static_content) is StaticContent:
        return None
    return str(static_content.classe)[1:-1].split(',')[1][2:-1]
