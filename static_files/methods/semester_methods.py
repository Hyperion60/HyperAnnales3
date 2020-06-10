from static_files.models import SemesterFile


def create_semester(semester):
    if semester < 0 or semester > 10:
        return None
    test_s = SemesterFile.objects.filter(semester=semester)
    if not len(test_s):
        new_semester = SemesterFile(semester=semester)
        new_semester.save(using='pdf_ref')
        return new_semester
    return test_s[0]


def get_semester(semester):
    test_s = SemesterFile.objects.filter(semester__exact=semester)
    if len(test_s):
        return test_s[0]
    return None
