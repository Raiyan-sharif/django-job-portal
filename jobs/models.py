from django.conf import settings
from django.db import models

from accounts.models import Skill


class Job(models.Model):
    CATEGORY_CHOICES = [
        ('software', 'Software & IT'),
        ('data', 'Data & Analytics'),
        ('design', 'Design & Creative'),
        ('marketing', 'Marketing & Sales'),
        ('finance', 'Finance & Accounting'),
        ('hr', 'Human Resources'),
        ('engineering', 'Engineering'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]

    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=150)
    number_of_openings = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, related_name='jobs')
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def skill_names(self):
        return [skill.name for skill in self.skills.all()]

    @property
    def company(self):
        profile = getattr(self.recruiter, 'recruiter_profile', None)
        return profile.company_name if profile else self.recruiter.display_name

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']
        constraints = [
            models.UniqueConstraint(fields=['job', 'applicant'], name='one_application_per_job'),
        ]

    def __str__(self):
        return f'{self.applicant} applied to {self.job}'