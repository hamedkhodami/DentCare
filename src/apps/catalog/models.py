from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

from . import enums


class ServiceCategoryModel(BaseModel):
    name = models.CharField(_('Category Name'), max_length=100)
    icon = models.ImageField(_('Icon'), upload_to='images/catalog/icon/', null=True, blank=True)
    ui_color = models.CharField(_('UI Color'), max_length=12, blank=True)

    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Categories')

    def __str__(self):
        return self.name


class ServiceModel(BaseModel):
    PricingType = enums.ServicePricingTypeEnum
    FormType = enums.ServiceFormTypeEnum

    category = models.ForeignKey(
        ServiceCategoryModel,
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name=_('Category')
    )
    name = models.CharField(_('Service Name'), max_length=120)
    code = models.CharField(_('Service Code'), max_length=50, unique=True)
    pricing_type = models.CharField(
        _('Pricing Type'),
        max_length=20,
        choices=PricingType.choices,
        default=PricingType.FIXED
    )
    fixed_price = models.DecimalField(
        _('Fixed Price'),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    form_type = models.CharField(
        _('Form Type'),
        max_length=20,
        choices=FormType.choices,
        default=FormType.SIMPLE
    )
    is_per_tooth = models.BooleanField(_('Per Tooth'), default=True)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.name} ({self.code})"


class MaterialModel(BaseModel):
    MaterialType = enums.MaterialTypeEnum
    type = models.CharField(
        _('Material Type'),
        max_length=20,
        choices=MaterialType.choices,
        default=MaterialType.ZIRCONIA
    )
    name = models.CharField(_('Material Name'), max_length=100)
    code = models.CharField(_('Material Code'), max_length=50, unique=True)
    description = models.TextField(_('Description'), blank=True)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materials')

    def __str__(self):
        return f"{self.name} ({self.code})"


class ServiceMaterialModel(BaseModel):
    service = models.ForeignKey(
        ServiceModel,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name=_('Service')
    )
    material = models.ForeignKey(
        MaterialModel,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_('Material')
    )
    is_default = models.BooleanField(
        _('Default Material'),
        default=False,
        help_text=_('Used as default material in forms')
    )

    class Meta:
        verbose_name = _('Service Material Compatibility')
        verbose_name_plural = _('Service Material Compatibilities')
        unique_together = ('service', 'material')

    def __str__(self):
        return f"{self.service.name} ↔ {self.material.name}"


class OptionGroupModel(BaseModel):
    name = models.CharField(_('Group Name'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Option Group')
        verbose_name_plural = _('Option Groups')

    def __str__(self):
        return self.name


class OptionModel(BaseModel):
    OptionInputType = enums.OptionInputTypeEnum
    OptionLevel = enums.OptionLevelEnum

    group = models.ForeignKey(
        OptionGroupModel,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('Option Group')
    )
    label = models.CharField(_('Label'), max_length=100)
    input_type = models.CharField(
        _('Input Type'),
        max_length=20,
        choices=OptionInputType.choices,
        default=OptionInputType.CHOICE
    )
    level = models.CharField(
        _('Option Level'),
        max_length=20,
        choices=OptionLevel.choices,
        default=OptionLevel.BASE
    )
    required = models.BooleanField(_('Required'), default=False)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.label
