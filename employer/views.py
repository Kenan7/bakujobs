from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import CreateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.utils.http import is_safe_url
from authtools import views as authviews
from django.urls import reverse_lazy
from .models import Employer

class EmployerJobList(LoginRequiredMixin, ListView):
    template_name = 'employer/job_list.html'
    def get_queryset(self, *args, **kwargs):
        slug = self.request.user.slug
        qs = get_object_or_404(Employer, slug=slug)
        return qs.job_set.all()


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'bakujobs/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    context_object_name = 'form'
    template_name = 'bakujobs/register.html'
    success_url = '/login/'


class LogOutView(authviews.LogoutView):
    url = reverse_lazy('home')

