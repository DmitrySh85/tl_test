from django.urls import path

from .views import DepartmentTreeView


app_name = 'company'


urlpatterns = [
    path(
        '',
        DepartmentTreeView.as_view(),
    )
]