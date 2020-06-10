from django import forms

from static_files.models import SemesterFile


class SetYearSemester(forms.Form):
    active_semester = forms.ModelChoiceField(queryset=SemesterFile.objects.all().order_by('semester'))
