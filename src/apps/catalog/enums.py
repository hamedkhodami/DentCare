from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ServicePricingTypeEnum(TextChoices):
    FIXED = 'fixed', _('Fixed Price')
    CUSTOM = 'custom', _('Custom Price')


class ServiceFormTypeEnum(TextChoices):
    SIMPLE = 'simple', _('Simple Form')
    ADVANCED = 'advanced', _('Advanced Form')


class MaterialTypeEnum(TextChoices):
    ZIRCONIA = 'zirconia', _('Zirconia')
    METAL = 'metal', _('Non-Precious Metal')
    HYBRID = 'hybrid', _('Hybrid Ceramic')
    RESIN = 'resin', _('Resin')


class OptionInputTypeEnum(TextChoices):
    BOOLEAN = 'bool', _('Yes / No')
    INTEGER = 'int', _('Integer')
    FLOAT = 'float', _('Decimal')
    CHOICE = 'choice', _('Single Choice')
    MULTICHOICE = 'multichoice', _('Multiple Choice')
    TEXT = 'text', _('Text Input')


class OptionLevelEnum(TextChoices):
    BASE = 'base', _('Base Form')
    DETAIL = 'detail', _('Detail Options')
    EXTENDED = 'extended', _('Extended Layer')