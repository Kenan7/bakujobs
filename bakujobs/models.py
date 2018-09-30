from .utils import slug_pre_save_receiver, email_post_save_receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from froala_editor import fields
from django.urls import reverse
from django.db import models

Employer = get_user_model()

GENDER_CHOICES = (
    ('All', 'All'),
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class Category(models.Model):
    name            = models.CharField(max_length=50)
    slug            = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Description(models.Model):
    name            = models.CharField(max_length=50)
    category_name   = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug            = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name            = models.CharField(max_length=20)
    slug            = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    class Meta:
        ordering = ['-modified_at']

    owner           = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title       = models.CharField(
        max_length=50,
        help_text="Please write job title carefully, avoid grammatic mistakes"
    )
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    job_description = models.ForeignKey(Description, on_delete=models.CASCADE)
    job_type        = models.ForeignKey(Type, on_delete=models.CASCADE)
    description     = fields.FroalaField()
    min_salary      = models.IntegerField(default=0)
    max_salary      = models.IntegerField(default=0)
    gender          = models.CharField(max_length=8, choices=GENDER_CHOICES, default="All")
    created_at      = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at     = models.DateTimeField(auto_now=True, editable=False)
    status          = models.BooleanField(default=1)
    slug            = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.job_title

    @property
    def name(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse('jobdetail', kwargs={'slug': self.slug})

# Signal stuff

#post_save.connect(email_post_save_receiver, sender=Job)
pre_save.connect(slug_pre_save_receiver, sender=Category)
pre_save.connect(slug_pre_save_receiver, sender=Description)
pre_save.connect(slug_pre_save_receiver, sender=Type)
pre_save.connect(slug_pre_save_receiver, sender=Job)
