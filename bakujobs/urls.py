from employer.views import LoginView, RegisterView
from django.urls import path, re_path, include
from employer.models import Employer
from django.views.generic import *
from bakujobs import views
import debug_toolbar

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    # authentication stuff
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    # job stuff
    path('jobs/<slug:slug>/', views.JobDetail.as_view(), name='jobdetail'),
    path('create/', views.JobCreate.as_view(), name='jobcreate'),
    path('sorted/', views.GetDateAndFilter.as_view()),
    path('ajax/load-items/', views.GetCategoryDescriptionAjaxView.as_view(), name='ajax_load_items'),

    # employer stuff
    path('employer/<slug:slug>/', views.JobDetail.as_view(), name='employer'),

    # additional
    path('__debug__/', include(debug_toolbar.urls)),
]
