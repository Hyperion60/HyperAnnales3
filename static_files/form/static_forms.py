from django import forms
from static_files.models import StaticContent, StaticFile, YearFile,\
    SemesterFile, SubjectFile, CategoryFile


class StaticContentForm(forms.ModelForm):
    class Meta:
        model = StaticContent
        fields = ('year', 'semester', 'subject', 'category', 'name', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester'].queryset = SemesterFile.objects.none()
        self.fields['subject'].queryset = SubjectFile.objects.none()
        self.fields['category'].queryset = CategoryFile.objects.none()
        self.fields['file'].queryset = StaticFile.objects.none()

    if 'year' in self.data:
        try:
            year_id = int(self.data.get('year'))
            self.fields['semester'].queryset = SemesterFile.objects.filter(semester__lte=year_obj.active_semester.semester).order_by('semester')

