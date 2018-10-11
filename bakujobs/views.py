from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.http import JsonResponse
from employer.models import Employer
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    TemplateView
)
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from bakujobs.models import (
    Job,
    Type,
    Description,
    Category
)
from django.utils import timezone
from datetime import timedelta
from .forms import JobCreate
from itertools import chain
import pytz


class Home(ListView):
    model = Job
    template_name = "bakujobs/job_list.html"

class JobCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = JobCreate
    template_name = 'bakujobs/job_create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        print(instance.owner)
        response = super(JobCreate, self).form_valid(form)
        form.save()
        return response

    # def get_form_kwargs(self):
    #     kwargs = super(JobCreate, self).get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

class JobDetail(DetailView):
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
    ajax_template = "bakujobs/job_posts.html"
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

# class Search(TemplateView):
#     template_name = 'bakujobs/search.html'

class SearchView(ListView):
    template_name = 'bakujobs/search.html'
    count = 0

    def get(self, request, *args, **kwargs):
        # print("Request method is GET")
        if request.is_ajax():
            # print("Request is ajax")
            query = request.GET.get('q', None)
            context = {}
            # print("Here is a query", query)
            if query != "":
                # print("Query is not none")
                job_results = Job.objects.search(query)
                count = job_results.count()
                context['count'] = count
                context['query'] = query
                # print("job result is", job_results)
                context['search_result'] = job_results
            else:
                context["error"] = True
                job_results = Job.objects.none()
            return render(request, self.template_name, context)

        else:
            return HttpResponse("it is not just ajax request")

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['count'] = self.count or 0
    #     context['query'] = self.request.GET.get('q')
    #     context['result'] = True
    #     return context
    #
    # def get_queryset(self):
    #     request = self.request
    #     query = request.GET.get('q', None)
    #
    #     if query is not None:
    #         job_results         = Job.objects.search(query)
    #
    #         # combine querysets
    #         queryset_chain = chain(
    #             job_results,
    #         )
    #         qs = sorted(queryset_chain,
    #                     key=lambda instance: instance.pk,
    #                     reverse=True)
    #         self.count = len(qs) # since qs is actually a list
    #         return qs
    #     return Job.objects.none() # just an empty queryset as default