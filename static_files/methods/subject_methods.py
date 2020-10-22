from static_files.models import SubjectFile, SemesterFile, YearFile


# context(dict), subject(str), semester(pk), year(pk), school(pk)
def CreateSubject(context, subject, semester, year, school):
    error = False
    try:
        year_obj = YearFile.objects.get(pk=year)
        semester_obj = SemesterFile.objects.get(pk=semester)
    except (YearFile.DoesNotExist, SemesterFile.DoesNotExist):
        context['error'] = "Information invalide"
        error = True
    if not error:
        if year_obj.active_semester.semester < semester_obj.semester:
            context['error'] = "Vous ne pouvez pas ajouter de matière à un semestre futur"
        else:
            if not len(SubjectFile.objects.filter(year=YearFile.objects.get(pk=year), semester=SemesterFile.objects.get(pk=semester), subject__exact=subject)):
                new_subject = SubjectFile(subject=subject, semester=semester_obj, year=year_obj, location=school)
                new_subject.save()
                context['message'] = "Nouvelle matière créée"
            else:
                context['error'] = "La matière existe deja"
    return context


def CleanSubject():
    for subject in SubjectFile.objects.all():
        list_subject = SubjectFile.objects.filter(year=subject.year, semester=subject.semester, subject__exact=subject.subject)
        if len(list_subject) > 1:
            for i in range(1, len(list_subject)):
                list_subject[i].delete()

