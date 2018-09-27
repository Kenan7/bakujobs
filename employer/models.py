from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from bakujobs.utils import slug_pre_save_receiver
from django.db.models.signals import pre_save
from django.db import models

class EmployerManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email adress")
        if not password:
            raise ValueError("Users must have a password")
        employer = self.model(
            email = self.normalize_email(email)
        )
        employer.set_password(password)
        employer.save(using=self._db)
        return employer

    def create_staff(self, email, name, password=None):
        employer = self.create_user(
            email=email,
            name=name,
            password=password,
            is_staff=True
        )

    def create_superuser(self, email, name, password=None):
        employer = self.create_user(
            email=email,
            name=name,
            password=password,
            is_staff=True,
            is_admin=True
        )


class Employer(AbstractBaseUser):
    name            = models.CharField(max_length=50)
    email           = models.EmailField(max_length=255, unique=True)
    location        = models.CharField(max_length=50)
    website         = models.URLField(blank=True)
    phone           = models.CharField(max_length=15, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at     = models.DateTimeField(auto_now=True, editable=False)
    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False)
    slug            = models.SlugField(blank=True, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = EmployerManager()

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'

pre_save.connect(slug_pre_save_receiver, sender=Employer)