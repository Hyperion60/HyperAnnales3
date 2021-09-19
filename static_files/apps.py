from django.apps import AppConfig


class StaticFilesConfig(AppConfig):
    name = 'static_files'

    def ready(self):
        from static_files.models import School, YearFile, SemesterFile, ContentColor, CategoryColor, StaticContent, \
                                        ExtensionFile
        from static_files.methods.year_methods import create_year
        from static_files.methods.category_methods import COLOR_CATEGORY
        from static_files.methods.file_methods import COLOR_FILE, EXTENSION_FILE
        try:
            School.objects.get(school__exact="EPITA")
        except School.DoesNotExist:
            School(school="EPITA").save()
        try:
            School.objects.get(school__exact="ESIEE")
        except School.DoesNotExist:
            School(school="ESIEE").save()

        for semester in range(1, 11):
            try:
                SemesterFile.objects.get(semester__exact=semester)
            except SemesterFile.DoesNotExist:
                SemesterFile(semester=semester).save()

        active_semester = 9
        for year in range(2022, 2027):
            try:
                YearFile.objects.get(year__exact=year)
            except YearFile.DoesNotExist:
                create_year(year, active_semester)
            active_semester -= 2

        for (type, color) in COLOR_FILE:
            try:
                ContentColor.objects.get(type__exact=type)
            except ContentColor.DoesNotExist:
                ContentColor(type=type, color=color).save()

        for (type, color) in COLOR_CATEGORY:
            try:
                CategoryColor.objects.get(type__exact=type)
            except CategoryColor.DoesNotExist:
                CategoryColor(type=type, color=color).save()

        for (type, extension) in EXTENSION_FILE:
            try:
                ExtensionFile.objects.get(extension__exact=extension)
            except ExtensionFile.DoesNotExist:
                ExtensionFile(type=type, extension=extension).save()

        for location in School.objects.all():
            location.count = len(StaticContent.objects.filter(category__subject__location=location))
            location.save()
