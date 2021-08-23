from django.conf import settings
from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            phone_number = int('09032627632')
            password = 'admin'
            print('Creating account for %s (%s)' % (phone_number))
            admin = User.objects.create_superuser(phone_number=phone_number, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')