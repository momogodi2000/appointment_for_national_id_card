from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from booking import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('auth/', include('social_django.urls', namespace='social')),




    
    path("api/login/", api.LoginView.as_view(), name="api_login"),
    path("api/register/", api.RegistrationView.as_view(), name="api_register"),
    path("api/appointments/get-add/", api.AppointmentView.as_view(), name="get_post_appointment"),
    path("api/appointments/edit-delete/<int:appointmentId>/", api.AppointmentView.as_view(), name="edit-delete-appointment"),
    path("api/user/get-add/", api.UserView.as_view(), name="get_add_user"),
    path("api/user/edit-delete/<int:id>/", api.UserView.as_view(), name="Edit_delete_user"),
    path("api/missing-cards/", api.MissingCardView.as_view(), name="Get post missing card(s)"),
    path("api/card-status/<int:appointment_id>/", api.CardStatusView.as_view(), name="Get_update_card_avalilability"),
    path("api/contact-us/", api.ContactUsView.as_view(), name="Contact us messages"),
    path("api/notification/<int:id>/", api.NotificationsView.as_view(), name="Get notifications"),
    path("api/communications/", api.CommunicationsView.as_view(), name="Add_get_communications"),
    path("api/communications/<int:id>/", api.CommunicationsView.as_view(), name="Edit_delete_communications"),
    path("api/payments/", api.PaymentView.as_view(), name="make_payment"),
    path("api/documents/", api.DocumentView.as_view(), name="add_get_document"),
    path("api/documents/<int:document_id>/", api.DocumentView.as_view(), name="delete_document")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
