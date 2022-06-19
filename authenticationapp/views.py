from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.generic import UpdateView

from .forms import UserForm, LoginForm, RegistrationForm, UserForm1
from .models import MyUser


def default_url(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        return redirect('/login')


def userCreation(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = MyUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)
            messages.success(request, _('Account created'))
            return redirect('/dashboard')
    else:
        form = RegistrationForm()
        return render(
            request,
            'create.html',
            {
                'form': form,
                'menu': 'create'
            }
        )


def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                return render(
                    request,
                    'login.html',
                    {
                        'form': form,
                        'menu': 'login',
                        'fail': 'Invalid Username Or Password'
                    }
                )
        else:
            return render(
                request,
                'login.html',
                {
                    'form': form,
                    'menu': 'login',
                    'fail': 'Invalid Data'
                }
            )
    else:
        form = LoginForm()
        return render(
            request,
            'login.html',
            {
                'form': form,
                'menu': 'login'
            }
        )


def sample_demo(request):
    if request.method == 'POST':
        pass
    else:
        form = UserForm()
        return render(
            request,
            'create.html',
            {
                'form': form,
                'menu': 'sampledemo'
            }
        )


@login_required(login_url='/login')
def user_logout(request):
    print(request.user)
    logout(request)
    return render(
        request,
        'logout.html',
    )


@login_required(login_url='/login')
def dashboard(request):
    print(request.user)
    return render(
        request,
        'userdashboard.html',
        {'user': request.user, 'menu': 'profile'}
    )


class ProfileView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = UserForm1
    template_name = 'updateprofile.html'
    template_name_suffix = 'updateprofile'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


def sample(request):
    return render(
        request,
        'sample.html',
        {}
    )


@login_required(login_url='/login')
def track_changes(request):
    user = MyUser.objects.get(username=request.user.username)
    print(user.tracker.previous('zipcode'))
    print(user.tracker.has_changed('zipcode'))
    print(user.tracker.changed())
    print(user.zipcode_tracker.changed())
    return render(
        request,
        'track_changes.html',
        {'user': request.user, 'menu': 'track_changes'}
    )
