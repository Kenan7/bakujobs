from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from bakujobs.utils import slug_pre_save_receiver
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.db.models import Q
from django.db import models

class EmployerManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            name=name,
            email = self.normalize_email(email),
        )
        user_obj.set_password(password) # change user password
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, name=None, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, name=None, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Employer(AbstractBaseUser):
    name        = models.CharField(max_length=255)
    email       = models.EmailField(max_length=255, unique=True)
    location    = models.CharField(max_length=255)
    website     = models.URLField(max_length=255)
    phone       = models.CharField(max_length=15, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    slug        = models.SlugField(blank=True, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = EmployerManager()

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'

    def __str__(self):
        return self.name

    def get_name(self):
        if self.name:
            return self.name
        return self.email

    def get_email(self):
        return self.email

    def get_absolute_url(self):
        return reverse('employer', kwargs={'slug': self.slug})

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

pre_save.connect(slug_pre_save_receiver, sender=Employer)
