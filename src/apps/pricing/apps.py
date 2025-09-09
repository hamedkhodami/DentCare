from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PricingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pricing'
    verbose_name = _("Pricing")
