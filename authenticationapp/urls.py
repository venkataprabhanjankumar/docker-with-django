from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('create/', views.userCreation),
    path('sample', views.sample),
    path('login/', views.userLogin, name='login'),
    path('', views.default_url),
    path('sampledemo', views.sample_demo),
    path('dashboard', views.dashboard),
    path('logout', views.user_logout),
    path('updateprofile', views.ProfileView.as_view(), name='profile'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('track', views.track_changes, name='track_changes')
]
