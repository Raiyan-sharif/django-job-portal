from django import forms

from accounts.utils import parse_skills, skills_from_text, skills_to_text

from .models import Application, Job


class JobForm(forms.ModelForm):
    """Title, Number of openings, Category, Job description, Skills set."""

    skills_text = forms.CharField(
        label='Skill set',
        help_text='Skills a candidate needs, separated by commas',
    )

    class Meta:
        model = Job
        fields = ['title', 'number_of_openings', 'category', 'description']
        labels = {'description': 'Job description'}
        widgets = {'description': forms.Textarea(attrs={'rows': 6})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['skills_text'].initial = skills_to_text(self.instance.skills.all())

    def clean_number_of_openings(self):
        number = self.cleaned_data['number_of_openings']
        if number < 1:
            raise forms.ValidationError('There must be at least one opening.')
        return number

    def clean_skills_text(self):
        text = self.cleaned_data['skills_text']
        if not parse_skills(text):
            raise forms.ValidationError('Add at least one required skill.')
        return text

    def save(self, commit=True):
        job = super().save(commit=commit)
        if commit:
            job.skills.set(skills_from_text(self.cleaned_data['skills_text']))
        return job


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        labels = {'cover_letter': 'Cover letter (optional)'}
        widgets = {'cover_letter': forms.Textarea(attrs={'rows': 4})}