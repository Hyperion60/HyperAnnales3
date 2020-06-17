from django.urls import path
from static_files.views import admin_views,\
    category_views,\
    subject_views,\
    semester_views,\
    year_views,\
    base_template,\
    file_views


urlpatterns = [
    path('admin/', admin_views.static_admin),
    path('add/category/', category_views.CreateCategoryView),
    path('add/semester/', semester_views.CreateSemesterView),
    path('add/subject/', subject_views.CreateSubjectView),
    path('add/year/', year_views.CreateYearView),
    path('change/year/<int:year>/', year_views.SetSemesterYearView),
    path('test/<int:year>', base_template.test_template),
    path('protected/<str:token>/', file_views.SendFile),
]
