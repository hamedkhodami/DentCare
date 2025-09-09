from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class UserRoleEnum(TextChoices):

    ADMIN = 'admin', _('Admin')
    SECRETARY = 'secretary', _('Secretary')
    DOCTOR = 'doctor', _('Doctor')


class UserGenderEnum(TextChoices):

    MALE = 'm', _('Male')
    FEMALE = 'f', _('Female')
