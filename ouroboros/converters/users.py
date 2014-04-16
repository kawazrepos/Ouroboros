from .base import BaseConverter

class UserConverter(BaseConverter):

    def convert(self):
        s = self.src_obj
        return self.Dst(
            id=s.id,
            username=s.username,
            first_name=s.first_name,
            last_name=s.last_name,
            email=s.email,
            password=s.password,
            is_staff=s.is_staff,
            is_active=s.is_active,
            is_superuser=s.is_superuser,
            last_login=s.last_login,
            date_joined=s.date_joined,
            nickname=s.username,
            gender='man'
        )
