from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_jobseeker = models.BooleanField('Is jobseeker', default=False)
    is_recruiter = models.BooleanField('Is recruiter', default=False)
    is_approved = models.BooleanField('Is approved', default=False)
