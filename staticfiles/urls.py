from django.urls import path

from . import views

urlpattern = [
    path('<path:static>', views.serve_static),
]
