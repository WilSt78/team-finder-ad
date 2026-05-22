from django.urls import path

from . import views
from . import skills_views

app_name= 'users'

urlpatterns = [
    path('list/', views.get_users, name='users_list'),
    path('<int:user_id>/', views.user_detail, name='user_details'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:user_id>/skills/add/',
        skills_views.add_skill,name='add_skill'),
    path('<int:user_id>/skills/<int:skill_id>/remove/',
        skills_views.remove_skill, name='remove_skill'),
]
