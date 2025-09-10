from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.core.models import BaseModel
from apps.account.models import PatientModel, User
from apps.teeth.models import ToothModel
from apps.catalog.models import ServiceModel, MaterialModel, OptionModel

from .enums import CaseStatusEnum, CaseItemStatusEnum, MirrorCopyTypeEnum, CaseAttachmentEnum


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
    value = models.JSONField(
        _('Value'),
        default=dict,
        help_text=_("The selected value is typed (e.g. bool / int / float / list / str)")
    )

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


class CaseAttachment(BaseModel):
    FILE_TYPES = CaseAttachmentEnum

    case = models.ForeignKey(
        CaseModel,
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name=_('Case')
    )
    linked_item = models.ForeignKey(
        CaseItemModel,
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name=_('Linked Item')
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Uploaded By')
    )
    file = models.FileField(_('ّFile'), upload_to="cases/%Y/%m/%d/")
    file_type = models.CharField(_('ّFile Type'), max_length=20, choices=FILE_TYPES, default=FILE_TYPES.OTHER)
    description = models.TextField(_('Description'), blank=True)
    is_private = models.BooleanField(_('Is Private'), default=True, help_text=_('If True, the download link requires authentication'))

    class Meta:
        verbose_name = _('Case Attachment')
        verbose_name_plural = _('Case Attachments')
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["case", "linked_item"]),
        ]

    def str(self):
        return f"Attachment {self.pk} for Case {self.case_id}"