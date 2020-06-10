from static_files.models import SubjectFile, SemesterFile, YearFile


def CreateSubject(context, subject, semester, year):
    error = False
    try:
        year_obj = YearFile.objects.get(pk=year)
        semester_obj = SemesterFile.objects.get(pk=semester)
    except (YearFile.DoesNotExist, SemesterFile.DoesNotExist):
        context['error'] = "Information invalide"
        error = True
    if not error:
        if year_obj.semester.semester < semester_obj.semester:
            context['error'] = "Vous ne pouvez pas ajouter de matière à un semestre futur"
        else:
            new_subject = SubjectFile(subject=subject, semester=semester_obj, year=year_obj)
            new_subject.save()
            context['message'] = "Nouvelle matière créée"
    return context
