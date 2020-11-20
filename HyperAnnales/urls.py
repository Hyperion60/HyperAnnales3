"""HyperAnnales URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

from accounts.views import (
    registration_view,
    change_password,
    reset_password,
    logout_view,
    login_view,
    activate,
)

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    # Gestion utilisateur
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('register/', registration_view, name="register"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-\']+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name="activate"),
    path('reset_password/', reset_password, name="reset"),
    url(r'^change_password/(?P<uidb64>[0-9A-Za-z_\-\']+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', change_password, name="change"),
    # Static content
    path('static_content/', include('static_files.urls')),
    # Accueil
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
]
