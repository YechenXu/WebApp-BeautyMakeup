from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    #item list view
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name="profile"),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('edit-profile/<str:username>', views.edit_profile, name='edit-profile'),
    path('submit-profile-edit/<str:username>', views.submit_profile_edit, name='submit-profile-edit'),
    path('change-password', views.change_password, name='change-password'),
]