from .models import User
from django.core.exceptions import ValidationError

class EmailAuthBackend:
    def authenticate(self, request, username, password):
        try:
            user = User.users.get(email=username)
            success = user.check_password(password)
            if success:
                return user
            else:
                raise ValidationError('Wrong Password')

        except User.MultipleObjectsReturned:
            user = User.users.filter(email=username).order_by('id').first()
        except User.DoesNotExist:
            raise ValidationError('User doesn\'t exists')


        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None

    def get_user(self, uid):
        try:
            return User.users.get(pk=uid)
        except:
            return None
