from django import forms

from static_files.models import YearFile, SemesterFile


class SetSubject(forms.Form):
    subject = forms.CharField(max_length=100)
    semester = forms.ModelMultipleChoiceField(queryset=SemesterFile.objects.all(), to_field_name="semester")
    year = forms.ModelMultipleChoiceField(queryset=YearFile.objects.all(), to_field_name="year")
