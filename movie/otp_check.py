from .models import User
from datetime import datetime
from kavenegar import KavenegarAPI
from django.utils.translation import gettext_lazy as _



def sms_send(phone, otp):
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {                    
            'sender':'number_get_of_kavenegar',
            'receptor':phone,
            'message':_(f'password for verify in site FREE-FILM:{otp}')
    }
    api.sms_send(params)



def check_time(phone):
    try:
        user = User.objects.get(phone_number=phone)
        otp_time = user.otp_create_time
        now = datetime.now()
        diff_time = now - otp_time
        if diff_time.seconds > 120:
            return False
        return True

    except:
        return False
