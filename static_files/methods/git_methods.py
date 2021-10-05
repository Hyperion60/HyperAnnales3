from apscheduler.schedulers.blocking import BlockingScheduler
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from HyperAnnales.settings import TIME_ZONE

sched = BlockingScheduler(timezone=TIME_ZONE)


# Git push
@sched.scheduled_job('interval', minutes=3)
def push_git(root_git, name_git, commit_msg="Add file"):
    path = "{}{}/.git".format(root_git, name_git)
    try:
        repo = Repo(path)
        repo.git.add(update=True)
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print("Error during push")


# Git push
def pull_git(root_git, name_git):
    path = "{}{}/.git".format(root_git, name_git)
    try:
        repo = Repo(path)
        origin = repo.remote(name='origin')
        origin.pull()
    except InvalidGitRepositoryError:
        print("Invalid Git Repository")
        return 1
    except NoSuchPathError:
        print("Invalid Git Repository Path")
        return 1
    return 0


def commit_file(root_git, name_git, path_file, commit_msg):
    """Add file, create commit and push it
    :param root_git: (string) Path to the folder with all git repositories (ft. DockerFile)
    :param name_git: (string) Name of the git repository
    :param path_file: (string) Path to the file to add into git
    :param commit_msg: (string) Message for the commit
    :return: 0 if OK, 1 else"""

    path_git = "{}{}/.git".format(root_git, name_git)
    try:
        repo = Repo(path_git)
        repo.index.add(path_file)
        repo.index.commit(commit_msg)
        repo.remote(name='origin').push()
    except InvalidGitRepositoryError:
        print("Invalid Git Repository")
        return 1
    except NoSuchPathError:
        print("Invalid Git Repository Path")
        return 1
    except ValueError:
        print("Invalid Remote Git Branch")
        return 1
    except OSError:
        print("Invalid Path File to add")
        return 1
    return 0


def delete_git_file(root_git, name_git, path_file):
    path_git = "{}{}/.git".format(root_git, name_git)
    try:
        repo = Repo(path_git)
        repo.index.remove(path_file, working_tree=True)
        repo.index.commit("Delete file")
        repo.remote(name='origin').push()
    except InvalidGitRepositoryError:
        print("Invalid Git Repository")
        return 1
    except NoSuchPathError:
        print("Invalid Git Repository Path")
        return 1
    except ValueError:
        print("Invalid Remote Git Branch")
        return 1
    except OSError:
        print("Invalid Path File to add")
        return 1
    return 0