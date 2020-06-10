from django.urls import path
from static_files.views import admin_views, category_views, subject_views


urlpatterns = [
    path('admin/', admin_views.static_admin),
    path('add/category/', category_views.CreateCategoryView),
    path('add/subject/', subject_views.CreateSubjectView),
]
