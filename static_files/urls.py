from django.urls import path
from static_files.views import admin_views,\
    category_views,\
    subject_views,\
    semester_views,\
    year_views,\
    base_template,\
    file_views, \
    bulletin_file_views, \
    bulletin_views


urlpatterns = [
    path('admin/', admin_views.static_admin),
    path('add/category/', category_views.CreateCategoryView),
    path('add/information/<str:school>/<int:year>/', bulletin_views.CreateInformation),
    path('add/information/<str:school>/', bulletin_views.CreateInformation),
    path('add/information/file/<int:pk>/', bulletin_file_views.add_file_bulletin),
    path('add/file/', file_views.init_addfile_view),
    path('add/semester/', semester_views.CreateSemesterView),
    path('add/subject/', subject_views.CreateSubjectView),
    path('add/year/', year_views.CreateYearView),
    path('change/year/<int:year>/', year_views.SetSemesterYearView),
    path('change/<int:rndkey>/', file_views.UpdateFileView),
    path('change/category/<int:pk>/', category_views.ChangeCategory),
    path('change/bulletin/<int:pk>/', bulletin_views.UpdateInformation),
    path('del/bulletin/<int:pk>/', bulletin_views.DeleteInformation),
    path('test/<int:year>', base_template.test_template),
    path('protected/<str:token>/', file_views.SendFile),
    path('<int:year>/<int:id>/', file_views.CreateFileView),
]
