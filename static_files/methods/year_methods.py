from static_files.models import YearFile, SemesterFile
from static_files.methods.semester_methods import create_semester, get_semester


# year(int), semester(pk)
def create_year(year, semester):
    semester_obj = SemesterFile.objects.get(pk=semester)
    new_year = YearFile(year=year, semester=semester_obj)
    new_year.save()


def get_year(year):
    test_y = YearFile.objects.filter(year__exact=year)
    if len(test_y):
        return test_y[0]
    return None


# year(pk), semester(pk)
def set_year(year, semester):
    year_obj = YearFile.objects.get(pk=year)
    year_obj.semester = SemesterFile.objects.get(pk=semester)
    year_obj.save()
