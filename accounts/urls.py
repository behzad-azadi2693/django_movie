from django.urls import path
from .views import signout, sms, phone

app_name = 'accounts'

urlpatterns = {
    path('logout/',signout , name='logout'),
    path('sms/',sms , name='sms'),
    path('phone/',phone , name='phone'),
}