from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('officer_panel/', views.officer_panel, name='officer_panel'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
