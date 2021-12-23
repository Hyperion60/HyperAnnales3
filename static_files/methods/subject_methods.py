from static_files.models import SubjectFile, SemesterFile, YearFile, CategoryFile, StaticContent, StaticFile


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
            list_subj = SubjectFile.objects.filter(year=YearFile.objects.get(pk=year), semester=SemesterFile.objects.get(pk=semester), subject__exact=subject)
            if not len(list_subj):
                new_subject = SubjectFile(subject=subject, semester=semester_obj, year=year_obj, location=school)
                new_subject.save()
                context['new_subject_obj'] = new_subject
                context['message'] = "Nouvelle matière créée"
            else:
                context['new_subject_obj'] = list_subj[0]
                context['error'] = "La matière existe deja"
    return context


def UpdateSubject(request, context):
    if not request.user.is_staff:
        return False

    try:
        context['subject'].subject = context['title']
        context['subject'].semester = context['semester']
        context['subject'].year = context['year']
        context['subject'].location = context['school']
        context['subject'].save()
    except:
        context['errors'].append("Echec de la mise à jour du bulletin")
        return False
    return True


def DeleteSubject(request, context):
    if not request.user.is_staff:
        return False

    try:
        for category in CategoryFile.objects.filter(subject_id__exact=context['subject'].pk):
            for static in StaticContent.objects.filter(category_id__exact=category.pk):
                static.file.delete()
                static.delete()
            category.delete()
        context['subject'].delete()
    except:
        context['errors'].append("Impossible de supprimer la matière ou ses dépendances.")
        return False
    return True


def CleanSubject():
    for subject in SubjectFile.objects.all():
        list_subject = SubjectFile.objects.filter(year=subject.year, semester=subject.semester, subject__exact=subject.subject)
        if len(list_subject) > 1:
            for i in range(1, len(list_subject)):
                list_subject[i].delete()

