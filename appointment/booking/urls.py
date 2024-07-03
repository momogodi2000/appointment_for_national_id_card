from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import
from .views import user_panel, book_appointment, upload_document, MissingIDCardForm, manage_appointments, user_information
from .views import payment_page, AboutUsView
from .views import manage_users, add_user, edit_user, delete_user, manage_appointments, approve_appointment, reject_appointment, manage_documents, delete_document


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
    path('user/book-appointment/', views.book_appointment, name='book_appointment'),
    path('user/upload-document/', upload_document, name='upload_document'),
    path('user/payment/', payment_page, name='payment_page'),
    path('track-application/', views.track_application, name='track_application'),
    path('security-settings/', views.security_settings, name='security_settings'),
    path('insert_missing_id_card/', views.insert_missing_id_card, name='insert_missing_id_card'),
    path('contact-us/', views.contact_us, name='contact_us'),

    path('police/manage-appointments/', views.manage_appointments, name='manage_appointments'),
    path('police/user-information/', views.user_information, name='user_information'),
    path('edit-appointment/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('delete-appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('notifications/', views.notifications, name='notifications'),


    path('admin/manage-users/', manage_users, name='manage_users'),
    path('admin/add-user/', add_user, name='add_user'),
    path('admin/edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('admin/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    # path('admin/manage-appointments/', manage_appointments, name='manage_appointments'),
    path('police/approve-appointment/<int:appointment_id>/', approve_appointment, name='approve_appointment'),
    path('police/reject-appointment/<int:appointment_id>/', reject_appointment, name='reject_appointment'),
    path('admin/manage-documents/', manage_documents, name='manage_documents'),
    path('admin/delete-document/<int:document_id>/', delete_document, name='delete_document'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
   
]
