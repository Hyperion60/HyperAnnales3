from django.urls import path
from static_files import views


urlpatterns = [
    path('admin/', views.static_admin),
]
