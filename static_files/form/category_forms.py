from django import forms
from static_files.models import SubjectFile, SemesterFile, YearFile


class CreateCategoryForm(forms.Form):
    LIST_CAT = (
        ('TD', 'blue'),
        ('Documents', 'green'),
        ('Controles', 'red'),
        ('QCM', 'blue'),
        ('Aide/Cours', 'green'),
    )

    title = forms.CharField(max_length=150)
    subject = forms.ModelMultipleChoiceField(queryset=SubjectFile.objects.all(), to_field_name="subject")
    semester = forms.ModelMultipleChoiceField(queryset=SemesterFile.objects.all(), to_field_name="semester")
    year = forms.ModelMultipleChoiceField(queryset=YearFile.objects.all(), to_field_name="year")
    category = forms.ChoiceField(choices=LIST_CAT)


class SetPlaceCategoryForm(forms.Form):
    place = forms.IntegerField(min_value=1)
