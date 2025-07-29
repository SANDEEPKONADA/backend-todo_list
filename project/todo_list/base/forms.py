from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    reminder_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'reminder_time']


class TaskMediaForm(forms.Form):
    files = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            # removed 'multiple': True due to Django limitation
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['files'].widget.attrs.update({'multiple': 'multiple'})  # ✅ workaround

    def clean_files(self):
        uploaded_files = self.files.getlist('files')
        for f in uploaded_files:
            if f.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Each file must be under 10MB.")
        return uploaded_files


class PositionForm(forms.Form):
    position = forms.CharField()
