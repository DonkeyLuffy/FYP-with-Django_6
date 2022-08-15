from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('register', views.register_page, name='register_page'),
    path('login/',  views.login_page, name='login_page'),
    path('profile_create/', views.profile_create_page, name='profile_create'),

    path('', views.home_page, name='home_page'),
    path('logout/', views.logoutUser, name="logout"),

    path('profile/', views.profile_page, name='profiles'),
    path('profile/<int:pk>', views.profile_detail, name='profile_detail'),
    path('update/<int:pk>', views.profile_update_page, name='profile_update'),

    path('account/', views.account_page, name='account_page'),
    path('account_update/', views.account_update, name='account_update'),
    path('password_change/', views.change_password, name='change_password'),

    path('device/', views.device_page, name='device_page'),
    path('data/', views.data_page, name='data'),
    path('admin_data/', views.admin_data, name='admin_data'),
    path('admin_data/<int:pk>', views.admin_data_detail, name='admin_data_detail'),
]