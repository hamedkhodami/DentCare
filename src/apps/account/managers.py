from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .enums import UserRoleEnum


class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, role=UserRoleEnum.DOCTOR):
        user = self.model(email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=UserRoleEnum.ADMIN):
        if not email:
            raise ValueError(_('Users must have an email!'))

        user = self.create_user(email=email, password=password, role=role)
        user.is_admin = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)

        return user
