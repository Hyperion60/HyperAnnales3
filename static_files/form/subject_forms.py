from django import forms

from static_files.models import YearFile, SemesterFile


class SetSubject(forms.Form):
    semester = forms.ModelChoiceField(queryset=SemesterFile.objects.all().order_by('semester'))
    year = forms.ModelChoiceField(queryset=YearFile.objects.all().order_by('year'))
