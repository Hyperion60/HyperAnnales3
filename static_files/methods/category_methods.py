from static_files.models import CategoryFile, YearFile, SemesterFile, SubjectFile, School


# context(dict), subject(obj), title(str), category(str)
def CreateCategory(context, subject, title, category):
    error = False
    try:
        subject_obj = SubjectFile.objects.get(pk=subject)
    except (SubjectFile.DoesNotExist):
        context['error'] = "Information invalide"
        error = True
    if not error:
        place = CategoryFile.objects.filter(subject=subject_obj).order_by('place')
        if not len(place):
            place_new = 1
        else:
            place_new = len(place)
        new_cat = CategoryFile(category=category, title=title, subject=subject_obj, place=place_new)
        new_cat.save()
        context['message'] = "Nouvelle catégorie créée"
    return context
