from django import forms
from static_files.models import YearFile, SemesterFile, SubjectFile, CategoryFile, StaticContent


class CreateFileForm(forms.Form):
    class Meta:
        model = StaticContent
        fields = ('year', 'semester', 'subject', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester'].queryset = SemesterFile.objects.none()

        if 'year' in self.data:
            try:
                year_id = int(self.data.get('year'))
                self.fields['semester'].queryset = SemesterFile.objects.filter(semester__lte=year_obj.active_semester.semester).order_by('semester')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['semester'].queryset = self.instance.YearFile.