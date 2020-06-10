from static_files.models import YearFile
from static_files.methods.semester_methods import create_semester, get_semester


def create_year(year, semester=1):
    test_y = YearFile.objects.filter(year__exact=year)
    test_s = create_semester(semester)
    if not len(test_y):
        new_promo = YearFile(year=year, active_semester=test_s)
        new_promo.save(using='pdf_ref')
        return new_promo
    return test_y[0]


def get_year(year):
    test_y = YearFile.objects.filter(year__exact=year)
    if len(test_y):
        return test_y[0]
    return None


def set_year(year, semester):
    change = get_year(year)
    if change is None:
        return False
    change.active_semester = get_semester(semester)
    return True
