"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from django.urls import path, include
from django.shortcuts import redirect
from votings.views import AuthAPI, activate
from django.contrib import admin

urlpatterns = [
    path('', lambda req: redirect('votings:index')),
    path('admin/', admin.site.urls),
    path('votings/', include('votings.urls')),
    path('api-auth/', AuthAPI.as_view(), name='api_auth'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('favicon.ico', RedirectView.as_view(
        url='/static/images/favicon.ico'), name='favicon'),
]
