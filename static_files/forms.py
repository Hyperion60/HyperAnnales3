from django import forms
from django.forms import ModelForm, ModelChoiceField
from static_files.models import StaticContent, YearFile

SEMESTER = (
    (1, "Semestre 1"),
    (2, "Semestre 2"),
    (3, "Semestre 3"),
    (4, "Semestre 4"),
    (5, "Semestre 5"),
    (6, "Semestre 6"),
    (7, "Semestre 7"),
    (8, "Semestre 8"),
    (9, "Semestre 9"),
    (10, "Semestre 10"),
)

YEAR = (
    (2022, "2022"),
    (2023, "2023"),
    (2024, "2024"),
    (2025, "2025"),
)


class CreateYearForm(forms.Form):
    year = forms.ChoiceField(choices=YEAR)
    active_semester = forms.ChoiceField(choices=SEMESTER)


class CreatePDForm(ModelForm):
    year = forms.ModelMultipleChoiceField(queryset=YearFile.objects.all())
    class Meta:
        model = StaticContent
        fields = ['year', 'semester', 'subject', 'name']
