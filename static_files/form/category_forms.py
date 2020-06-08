from django import forms
from static_files.models import SubjectFile, SemesterFile, YearFile


class CreateCategoryForm(forms.Form):
    LIST_CAT = (
        ('blue', 'TD'),
        ('green', 'Documents'),
        ('red', 'Contrôles'),
        ('blue', 'QCM'),
        ('green', 'Aide/Cours'),
    )

    title = forms.CharField(max_length=150)
    subject = forms.ModelChoiceField(queryset=SubjectFile.objects.all().order_by('subject'), empty_label="Matière")
    semester = forms.ModelChoiceField(queryset=SemesterFile.objects.all().order_by('semester'), empty_label="Semestre")
    year = forms.ModelChoiceField(queryset=YearFile.objects.all().order_by('year'), empty_label="Année")
    category = forms.ChoiceField(choices=LIST_CAT)


class SetPlaceCategoryForm(forms.Form):
    place = forms.IntegerField(min_value=1)
