from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    RECRUITER = 'recruiter'
    JOBSEEKER = 'jobseeker'
    USER_TYPE_CHOICES = [
        (RECRUITER, 'Recruiter'),
        (JOBSEEKER, 'Job seeker'),
    ]

    display_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    @property
    def is_recruiter(self):
        return self.user_type == self.RECRUITER

    @property
    def is_jobseeker(self):
        return self.user_type == self.JOBSEEKER

    def has_profile(self):
        if self.is_recruiter:
            return hasattr(self, 'recruiter_profile')
        return hasattr(self, 'jobseeker_profile')

    def __str__(self):
        return self.display_name or self.username


class Skill(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RecruiterProfile(models.Model):
    """Company information for a recruiter."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=150)
    industry = models.CharField(max_length=100)
    company_website = models.URLField(blank=True)
    company_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    about_company = models.TextField(blank=True)

    def __str__(self):
        return self.company_name


class JobSeekerProfile(models.Model):
    """Skill set and resume for a job seeker."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    headline = models.CharField(max_length=150, help_text='e.g. Junior Python developer')
    domain = models.CharField(max_length=100, help_text='e.g. Software, Marketing, Finance')
    experience_years = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=30, blank=True)
    skills = models.ManyToManyField(Skill, related_name='jobseekers', blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)

    def skill_names(self):
        return [skill.name for skill in self.skills.all()]

    def __str__(self):
        return f'{self.user} ({self.headline})'