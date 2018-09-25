from django.urls import path, re_path, include
from django.views.generic import *
from bakujobs import views
import debug_toolbar

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('sorted/', views.GetDateAndFilter.as_view()),
    path('create/', views.JobCreate.as_view(), name='jobcreate'),
    path('jobs/<slug:slug>/', views.JobDetail.as_view(), name='jobdetail'),
    path('ajax/load-items/', views.GetCategoryDescriptionAjaxView.as_view(), name='ajax_load_items'),
    path('__debug__/', include(debug_toolbar.urls)),
]
