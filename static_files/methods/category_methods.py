from static_files.models import CategoryFile, YearFile, SemesterFile, SubjectFile, School


def CreateCategory(context, school, year, semester, subject, title, category):
    error = False
    try:
        year_obj = YearFile.objects.get(pk=year)
        semester_obj = SemesterFile.objects.get(pk=semester)
        subject_obj = SubjectFile.objects.get(pk=subject)
        school_obj = School.objects.get(pk=school)
    except (YearFile.DoesNotExist, SemesterFile.DoesNotExist, SubjectFile.DoesNotExist):
        context['error'] = "Information invalide"
        error = True
    if not error:
        place = CategoryFile.objects.filter(year=year_obj, semester=semester_obj, subject=subject_obj).order_by('place')
        if not len(place):
            place_new = 1
        else:
            place_new = len(place)
        new_cat = CategoryFile(category=category, title=title, subject=subject_obj, semester=semester_obj,
                               year=year_obj, place=place_new, school=school)
        new_cat.save()
        context['message'] = "Nouvelle catégorie créée"
    return context
