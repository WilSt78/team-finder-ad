from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.index, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/complete/',
        views.toggle_completion, name='toggle_completion'),
    path('<int:project_id>/toggle-participate/',
        views.toggle_participation, name='toggle_participation'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
]
