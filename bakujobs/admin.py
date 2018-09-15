from django.contrib import admin
from bakujobs.models import (
    Job,
    Description,
    Category,
    Type
)


class JobAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'job_description', 'job_title', 'job_type']
    fieldsets = [
        ('Job',
         {'fields':
              ['job_title',
               'category', 'job_description', 'job_type',
               'min_salary', 'max_salary', 'gender',
               'description'
               ]
          }
         ),
        ('Company',
         {'fields':
              ['company_name', 'location', 'email', 'website', 'phone']
          }
         ),
        ('Additional',
         {'fields':
              ['owner', 'slug', 'status']
          }
         )
    ]

admin.site.register(Job, JobAdmin)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Description)
