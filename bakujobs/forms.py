from django import forms
from bakujobs.models import *
from froala_editor.widgets import FroalaEditor

class CreateJob(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('job_title', 'company_name', 'category', 'job_description', 'job_type', 'location', 'description', 'website', 'email', 'phone', 'min_salary', 'max_salary', 'gender')

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user')
        super(CreateJob, self).__init__(*args, **kwargs)
        self.fields['job_description'].queryset = Description.objects.none()

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['job_description'].queryset = Description.objects.filter(category_name_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['job_description'].queryset = self.instance.category.description_set.order_by('name')
