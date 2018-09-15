from django.shortcuts import render, reverse
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import pytz
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView
)
from bakujobs.models import (
    Job,
    Type,
    Description,
    Category
)
from .forms import CreateJob

class Index(ListView):
    model = Job
    template_name = "bakujobs/job_list.html"

class CreateJob(CreateView):
    form_class = CreateJob
    template_name = 'bakujobs/job_create.html'
    success_url = ''

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        response = super(CreateJob, self).form_valid(form)
        form.save()
        return response

    # def get_form_kwargs(self):
    #     kwargs = super(CreateJob, self).get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

class DetailJob(DetailView):
    context_object_name = "job"
    queryset = Job.objects.all()
    template_name = 'bakujobs/job_detail.html'

class GetCategoryDescriptionAjaxView(View):
    ajax_template = "bakujobs/select.html"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            category_id = request.GET.get("category")
            job_description = Description.objects.filter(category_name_id=category_id).order_by('name')
            context = {}
            context["description_list"] = job_description
            return render(request, self.ajax_template, context)
        else:
            return self.not_found_message()

    def not_found_message(self):
        return JsonResponse({
            "message": "We can't find what you are looking for."
        }, status=404)

class GetDateAndFilter(View):
    ajax_template = "bakujobs/posts.html"
    date = {
        "last-one-hour" : timedelta(hours=1),
        "last-one-day" : timedelta(days=1),
        "last-seven-day" : timedelta(days=7),
        "last-fourteen-day" : timedelta(days=14),
        "last-thirty day" : timedelta(days=30),
        "all" : timedelta(weeks=10000)
    }
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            post_date = request.GET.get('date')
            post_date = self.date.get(post_date, timedelta(weeks=10000))
            date_from = timezone.now() - post_date
            queryset = Job.objects.filter(created_at__gte=date_from)
            context = {}
            context["object_list"] = queryset
            return render(request, self.ajax_template, context)