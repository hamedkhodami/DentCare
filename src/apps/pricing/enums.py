from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SurchargeTypeEnum(TextChoices):
    URGENCY = 'urgency', _('Urgency')
    COLOR = 'color', _('Special Color')
    COMPLEXITY = 'complexity', _('Complexity')
    CUSTOM = 'custom', _('Custom Surcharge')


class PriceScopeEnum(TextChoices):
    SERVICE = 'service', _('Service Only')
    MATERIAL = 'material', _('Material Only')
    COMBO = 'combo', _('Service + Material')


class QuoteStatusEnum(TextChoices):
    DRAFT = 'draft', _('Draft')
    SENT = 'sent', _('Sent')
    RESPONDED = 'responded', _('Responded')
    REJECTED = 'rejected', _('Rejected')