from static_files.models import SubjectFile, SemesterFile, YearFile, CategoryFile, StaticContent, School


# context(dict), subject(str), semester(pk), year(pk), school(pk)
def CreateSubject(context, subject, semester, year, school):
    try:
        year_obj = YearFile.objects.get(pk=year)
        semester_obj = SemesterFile.objects.get(pk=semester)
        school_obj = School.objects.get(pk=school)
    except (YearFile.DoesNotExist, SemesterFile.DoesNotExist):
        context['errors'].append("Information invalide")
        return

    if year_obj.active_semester.semester < semester_obj.semester:
        context['errors'].append("Vous ne pouvez pas ajouter de matière à un semestre futur")
    else:
        list_subj = SubjectFile.objects.filter(location=school_obj,
                                               year=year_obj,
                                               semester=semester_obj,
                                               subject__exact=subject)
        if not len(list_subj):
            new_subject = SubjectFile(subject=subject, semester=semester_obj, year=year_obj, location=school_obj)
            new_subject.save()
            context['new_subject_obj'] = new_subject
            context['message'] = "Nouvelle matière créée"
        else:
            context['new_subject_obj'] = list_subj[0]
            context['errors'].append("La matière existe déjà")


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

