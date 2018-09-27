from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

class Employer(AbstractBaseUser):
    name            = models.CharField(max_length=50)
    email           = models.CharField(max_length=10)
    location        = models.CharField(max_length=50)
    website         = models.URLField(blank=True)
    phone           = models.CharField(max_length=15, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at     = models.DateTimeField(auto_now=True, editable=False)
    slug            = models.SlugField(blank=True, null=True, unique=True)

    USERNAME_FIELD = 'name'

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'