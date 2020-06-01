from django.urls import path
from static_files import views


urlpatterns = [
    path('admin/', views.static_admin),
    path('add/year/', views.set_year_semester),
]
