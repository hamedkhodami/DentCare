from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.account.models import PatientModel, User
from apps.teeth.models import ToothModel
from apps.catalog.models import ServiceModel, MaterialModel, OptionModel

from .enums import CaseStatusEnum, CaseItemStatusEnum, MirrorCopyTypeEnum


class CaseModel(BaseModel):
    Status = CaseStatusEnum

    patient = models.ForeignKey(
        PatientModel,
        on_delete=models.CASCADE,
        related_name='cases',
        verbose_name=_('Patient')
    )
    title = models.CharField(_('Title'), max_length=150)
    description = models.TextField(_('Description'), blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    class Meta:
        verbose_name = _('Treatment Case')
        verbose_name_plural = _('Treatment Cases')

    def __str__(self):
        return f"Case: {self.title} ({self.patient.full_name})"


class CaseToothModel(BaseModel):
    case = models.ForeignKey(
        CaseModel,
        on_delete=models.CASCADE,
        related_name='case_teeth',
        verbose_name=_('Case')
    )
    tooth = models.ForeignKey(
        ToothModel,
        on_delete=models.PROTECT,
        related_name='case_usages',
        verbose_name=_('Tooth')
    )

    class Meta:
        verbose_name = _('Case Tooth')
        verbose_name_plural = _('Case Teeth')
        unique_together = ('case', 'tooth')

    def __str__(self):
        return f"{self.tooth.number} in {self.case.title}"


class CaseItemModel(BaseModel):
    Status = CaseItemStatusEnum

    case_tooth = models.ForeignKey(
        CaseToothModel,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Case Tooth')
    )
    service = models.ForeignKey(
        ServiceModel,
        on_delete=models.PROTECT,
        related_name='case_items',
        verbose_name=_('Service')
    )
    material = models.ForeignKey(
        MaterialModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='case_items',
        verbose_name=_('Material')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED
    )
    price = models.DecimalField(
        _('Price'),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    note = models.TextField(_('Note'), blank=True)

    class Meta:
        verbose_name = _('Case Item')
        verbose_name_plural = _('Case Items')

    def __str__(self):
        return f"{self.service.name} for Tooth {self.case_tooth.tooth.number}"


class CaseItemOptionModel(BaseModel):
    case_item = models.ForeignKey(
        CaseItemModel,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('Case Item')
    )
    option = models.ForeignKey(
        OptionModel,
        on_delete=models.PROTECT,
        related_name='case_usages',
        verbose_name=_('Option')
    )
    value = models.CharField(_('Value'), max_length=255)

    class Meta:
        verbose_name = _('Case Item Option')
        verbose_name_plural = _('Case Item Options')
        unique_together = ('case_item', 'option')

    def __str__(self):
        return f"{self.option.label}: {self.value}"


class MirrorCopyModel(BaseModel):

    case = models.ForeignKey(
        CaseModel,
        on_delete=models.CASCADE,
        related_name='mirror_copies',
        verbose_name=_('Case')
    )
    source_tooth = models.ForeignKey(
        CaseToothModel,
        on_delete=models.CASCADE,
        related_name='copied_from',
        verbose_name=_('Source Tooth')
    )
    target_tooth = models.ForeignKey(
        CaseToothModel,
        on_delete=models.CASCADE,
        related_name='copied_to',
        verbose_name=_('Target Tooth')
    )
    copy_type = models.CharField(
        _('Copy Type'),
        max_length=20,
        choices=MirrorCopyTypeEnum.choices,
        default=MirrorCopyTypeEnum.ADJACENT
    )

    class Meta:
        verbose_name = _('Mirror Copy')
        verbose_name_plural = _('Mirror Copies')
        unique_together = ('source_tooth', 'target_tooth', 'copy_type')

    def __str__(self):
        return f"{self.source_tooth.tooth.number} → {self.target_tooth.tooth.number} ({self.get_copy_type_display()})"