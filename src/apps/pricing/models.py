from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.catalog.models import ServiceModel, MaterialModel
from apps.treatment.models import CaseModel

from .enums import SurchargeTypeEnum, PriceScopeEnum, QuoteStatusEnum


class SurchargeModel(BaseModel):
    Type = SurchargeTypeEnum

    name = models.CharField(_('Surcharge Name'), max_length=100)
    type = models.CharField(
        _('Surcharge Type'),
        max_length=20,
        choices=Type.choices,
        default=Type.CUSTOM
    )
    amount = models.DecimalField(
        _('Amount'),
        max_digits=10,
        decimal_places=2
    )
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Surcharge')
        verbose_name_plural = _('Surcharges')

    def __str__(self):
        return f"{self.name} ({self.amount})"


class PriceListModel(BaseModel):
    name = models.CharField(_('Price List Name'), max_length=100)
    is_active = models.BooleanField(_('Active'), default=True)
    valid_from = models.DateField(_('Valid From'), null=True, blank=True)
    valid_until = models.DateField(_('Valid Until'), null=True, blank=True)

    class Meta:
        verbose_name = _('Price List')
        verbose_name_plural = _('Price Lists')

    def __str__(self):
        return self.name


class ServicePriceModel(BaseModel):
    Scope = PriceScopeEnum

    price_list = models.ForeignKey(
        PriceListModel,
        on_delete=models.CASCADE,
        related_name='service_prices',
        verbose_name=_('Price List')
    )
    service = models.ForeignKey(
        ServiceModel,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name=_('Service'),
        null=True,
        blank=True
    )
    material = models.ForeignKey(
        MaterialModel,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name=_('Material'),
        null=True,
        blank=True
    )
    scope = models.CharField(
        _('Scope'),
        max_length=20,
        choices=Scope.choices,
        default=Scope.COMBO
    )
    amount = models.DecimalField(
        _('Amount'),
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('Service Price')
        verbose_name_plural = _('Service Prices')
        unique_together = ('price_list', 'service', 'material')

    def __str__(self):
        return f"{self.service} + {self.material} → {self.amount}"


class QuoteRequestModel(BaseModel):
    Status = QuoteStatusEnum

    case = models.ForeignKey(
        CaseModel,
        on_delete=models.CASCADE,
        related_name='quote_requests',
        verbose_name=_('Case')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    comment = models.TextField(_('Comment'), blank=True)

    class Meta:
        verbose_name = _('Quote Request')
        verbose_name_plural = _('Quote Requests')

    def __str__(self):
        return f"Quote for {self.case.title} ({self.get_status_display()})"


class QuoteItemModel(BaseModel):
    quote = models.ForeignKey(
        QuoteRequestModel,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Quote Request')
    )
    service = models.ForeignKey(
        ServiceModel,
        on_delete=models.PROTECT,
        related_name='quote_items',
        verbose_name=_('Service')
    )
    material = models.ForeignKey(
        MaterialModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quote_items',
        verbose_name=_('Material')
    )
    suggested_price = models.DecimalField(
        _('Suggested Price'),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    note = models.TextField(_('Note'), blank=True)

    class Meta:
        verbose_name = _('Quote Item')
        verbose_name_plural = _('Quote Items')

    def __str__(self):
        return f"{self.service.name} → {self.suggested_price or '—'}"


class CaseSurchargeModel(BaseModel):
    case = models.ForeignKey(
        CaseModel,
        on_delete=models.CASCADE,
        related_name='surcharges',
        verbose_name=_('Case')
    )
    surcharge = models.ForeignKey(
        SurchargeModel,
        on_delete=models.PROTECT,
        related_name='case_links',
        verbose_name=_('Surcharge')
    )
    amount = models.DecimalField(
        _('Amount'),
        max_digits=10,
        decimal_places=2
    )
    note = models.TextField(_('Note'), blank=True)

    class Meta:
        verbose_name = _('Case Surcharge')
        verbose_name_plural = _('Case Surcharges')
        unique_together = ('case', 'surcharge')

    def __str__(self):
        return f"{self.surcharge.name} → {self.amount}"
