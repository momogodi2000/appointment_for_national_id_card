from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import
from .views import user_panel, book_appointment, upload_document, MissingIDCardForm, manage_appointments, user_information
from .views import payment_page, AboutUsView
from .views import history, about, center, manage_contact
from django.contrib.auth.decorators import login_required
from .views import manage_users, add_user, edit_user, delete_user, manage_appointments, approve_appointment, reject_appointment, manage_documents, delete_document, appointment_history, download_receipt
from .views import view_detail_admin


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path("auth/activation_code_email", views.activation_code_email, name="activation_code_email"),


## user url
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

    path('history/', login_required(history), name='history'),
    path('about/', about, name='about'),
    path('support_discussion/', views.support_discussion, name='support_discussion'),
    path('get-bot-response/', views.get_bot_response, name='get_bot_response'),
    path('security-grade/', views.security_grade, name='security_grade'),
    path('view_detail/<str:grade>/', views.view_detail, name='view_detail'),
    path('center/', center, name='center'),

    path('appointment/history/', appointment_history, name='appointment_history'),
    path('receipt/<int:appointment_id>/', download_receipt, name='download_receipt'),
    path('admin/view/<str:model_name>/', view_detail_admin, name='view_detail_admin'),

    path('profile_user/', views.profile_user, name='profile_user'),


## police url
    # path('generated-pdf/'),

    path('police/manage-appointments/', views.manage_appointments, name='manage_appointments'),
    path('panel/admin/manage-appointments/', views.admin_manage_appointments, name='admin_manage_appointments'),
    path('police/user-information/', views.user_information, name='user_information'),
    path('view-docs/<int:id>/', views.get_documents, name='view_docs'),
    path('edit-appointment/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('approve-appointment/<int:pk>/', views.approve_appointment, name='approve_appointment'),
    path('delete-appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('notifications/', views.notifications, name='notifications'),

    path('card_status/', views.card_status, name="card_status"),
    path('edit_card_status/<int:id>/', views.edit_card_status, name="edit_card_status"),
 
    path('manage_contact/', views.manage_contact, name='manage_contact'),
    path('reply_contact/', views.reply_contact, name='reply_contact'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('manage_id/', views.manage_id, name='manage_id'),
    path('add_missing_id_card/', views.add_missing_id_card, name='add_missing_id_card'),
    path('delete_id_card/<int:id_card_id>/', views.delete_id_card, name='delete_id_card'),

    path('setting_police/', views.setting_police, name='setting_police'),
    path('profile_police/', views.profile_police, name='profile_police'),

## admin url

    path('panel/admin/manage-users/', manage_users, name='manage_users'),
    path('panel/admin/add-user/', add_user, name='add_user'),
    path('panel/admin/edit-user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('panel/admin/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('police/approve-appointment/<int:appointment_id>/', approve_appointment, name='approve_appointment'),
    path('police/reject-appointment/<int:appointment_id>/', reject_appointment, name='reject_appointment'),
    path('panel/admin/manage-documents/', manage_documents, name='manage_documents'),
    path('panel/admin/delete-document/<int:document_id>/', delete_document, name='delete_document'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),   
    path('contact-messages/', views.contact_messages, name='contact_messages'),   
    path('admin-communications/', views.admin_communications, name='admin_communications'),
    path('map/', views.map_view, name='map'),
    path('analyse/', views.analyse_view, name='analyse'),

   

    path('post/', views.post_communication, name='post_communication'),
    path('view/', views.view_communications, name='view_communications'),
    path('edit/<int:pk>/', views.edit_communication, name='edit_communication'),
    path('delete/<int:pk>/', views.delete_communication, name='delete_communication'),

    path('communications/', views.communication_list, name='communication_list'),
    path('download/<int:communication_id>/', views.download_communication, name='download_communication'),
    path('communication/<int:communication_id>/', views.communication_detail, name='communication_detail'),


    path('statistic/', views.statistic, name='statistic'),


]
