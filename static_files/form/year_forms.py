from django import forms

from static_files.models import YearFile, SemesterFile

from datetime import datetime


class CreateYearForm(forms.Form):
    year = forms.IntegerField(min_value=2014, max_value=datetime.now().year + 5)
    active_semester = forms.ModelMultipleChoiceField(queryset=SemesterFile.objects.all(), empty_label="(Vide)")


class SetYearSemester(forms.Form):
    active_semester = forms.ModelMultipleChoiceField(queryset=SemesterFile.objects.all())
