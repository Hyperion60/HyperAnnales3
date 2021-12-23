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
    path('admin/', admin_views.static_admin, name="contribution"),
    path('add/category/', category_views.CreateCategoryView, name="create-category"),
    path('add/information/file/<int:pk>/', bulletin_file_views.add_file_bulletin, name="create-bulletin-file"),
    path('add/information/<str:school>/<int:year>/', bulletin_views.CreateInformation, name="create-bulletin-year"),
    path('add/information/<str:school>/', bulletin_views.CreateInformation, name="create-bulletin-school"),
    path('add/file/', file_views.init_addfile_view, name="create-file"),
    path('add/semester/', semester_views.CreateSemesterView, name="create-semester"),
    path('add/subject/', subject_views.CreateSubjectView, name="create-subject"),
    path('add/year/', year_views.CreateYearView, name="create-year"),
    path('change/year/<int:year>/', year_views.SetSemesterYearView, name="change-year"),
    path('change/<int:rndkey>/', file_views.UpdateFileView, name="change-secured-file"),
    path('change/unsecure_file/<int:pk>/', bulletin_file_views.update_bulletin_file, name="change-unsecured-file"),
    path('change/category/<int:pk>/', category_views.ChangeCategory, name="change-category"),
    path('change/bulletin/<int:pk>/', bulletin_views.UpdateInformation, name="change-bulletin"),
    path('change/subject/<int:pk>/', subject_views.UpdateSubjectView, name="change-subject"),
    path('del/bulletin/<int:pk>/', bulletin_views.DeleteInformation, name="del-bulletin"),
    path('del/subject/<int:pk>/', subject_views.DeleteSubjectView, name="del-subject"),
    path('del/unsecure_file/<int:pk>/', bulletin_file_views.delete_bulletin_file, name="del-unsecured-file"),
    path('get/<int:key>/', file_views.GetFile, name="get-token-file"),
    path('test/<int:year>', base_template.test_template),
    path('protected/<str:token>/', file_views.SendFile, name="get-secured-file"),
    path('<int:year>/<int:id>/', file_views.CreateFileView),
]
