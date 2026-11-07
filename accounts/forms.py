import os

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import JobSeekerProfile, RecruiterProfile, User
from .utils import parse_skills, skills_from_text, skills_to_text


class RegistrationForm(UserCreationForm):
    """Username, Display name, Email, Password, Confirm Password, User type."""

    display_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = ['username', 'display_name', 'email',
                  'password1', 'password2', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm password'

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class LoginForm(AuthenticationForm):
    """Username and Password."""


class RecruiterProfileForm(forms.ModelForm):
    """Company information."""

    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'industry', 'company_website',
                  'company_address', 'phone', 'about_company']
        widgets = {'about_company': forms.Textarea(attrs={'rows': 4})}


class JobSeekerProfileForm(forms.ModelForm):
    """Skill set and resume upload."""

    skills_text = forms.CharField(
        label='Skill set',
        help_text='Separate skills with commas, e.g. Python, Django, SQL',
    )

    class Meta:
        model = JobSeekerProfile
        fields = ['headline', 'domain', 'experience_years', 'phone', 'resume']

    field_order = ['headline', 'domain', 'experience_years', 'phone', 'skills_text', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].help_text = 'PDF, DOC or DOCX, up to 5 MB'
        if self.instance.pk:
            self.fields['skills_text'].initial = skills_to_text(self.instance.skills.all())

    def clean_skills_text(self):
        text = self.cleaned_data['skills_text']
        if not parse_skills(text):
            raise forms.ValidationError('Add at least one skill.')
        return text

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and hasattr(resume, 'size'):
            extension = os.path.splitext(resume.name)[1].lower()
            if extension not in ('.pdf', '.doc', '.docx'):
                raise forms.ValidationError('Upload a PDF, DOC or DOCX file.')
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('The resume must be 5 MB or smaller.')
        return resume

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            profile.skills.set(skills_from_text(self.cleaned_data['skills_text']))
        return profile