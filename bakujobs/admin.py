from django.contrib.auth import get_user_model
from django.contrib import admin
from bakujobs.models import (
    Job,
    Description,
    Category,
    Type,
)

class EmployerAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Job',
            {
                'fields':
                    ['name', 'password',
                     'email', 'location', 'website', 'phone']
            }
        )
    ]

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
        # ('Company',
        #  {'fields':
        #       ['company_name', 'location', 'email', 'website', 'phone']
        #   }
        #  ),
        ('Additional',
         {'fields':
              ['owner', 'slug', 'status']
          }
         )
    ]
    list_filter = ('job_type', 'created_at')

admin.site.register(Job, JobAdmin)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Description)
