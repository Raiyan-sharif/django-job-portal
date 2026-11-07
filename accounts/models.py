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

    def __str__(self):
        return self.display_name or self.username