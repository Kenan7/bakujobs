from employer.views import LoginView, RegisterView
from django.urls import path, re_path, include
from employer import views as employer_views
from bakujobs import views as bakujobs_views
from employer.models import Employer
from django.views.generic import (
    View,
    TemplateView,
    CreateView,
    ListView,
    DetailView
)
import debug_toolbar

urlpatterns = [
    path('', bakujobs_views.Home.as_view(), name='home'),
    # authentication stuff
    path('login/', employer_views.LoginView.as_view(), name='login'),
    path('logout/', employer_views.LogOutView.as_view(), name='logout'),
    path('register/', employer_views.RegisterView.as_view(), name='register'),


    # job stuff
    path('jobs/<slug:slug>/', bakujobs_views.JobDetail.as_view(), name='jobdetail'),
    path('create/', bakujobs_views.JobCreate.as_view(), name='jobcreate'),
    path('update/', bakujobs_views.JobUpdate.as_view(), name='jobupdate'),
    path('sorted/', bakujobs_views.GetDateAndFilter.as_view()),
    path('ajax/load-items/', bakujobs_views.GetCategoryDescriptionAjaxView.as_view(), name='ajax_load_items'),

    # employer stuff
    path('employer/', employer_views.EmployerJobList.as_view(), name='employer_job_list'),

    # additional
    path('search/', bakujobs_views.SearchView.as_view(), name='query'),
    path('__debug__/', include(debug_toolbar.urls)),
]
