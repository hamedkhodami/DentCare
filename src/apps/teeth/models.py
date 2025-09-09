from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.account.models import PatientModel

from .enums import ToothStatusEnum, ToothRelationEnum, ToothPositionEnum


class ToothChartModel(BaseModel):
    patient = models.OneToOneField(
        PatientModel,
        on_delete=models.CASCADE,
        related_name='tooth_chart',
        verbose_name=_('Patient')
    )

    class Meta:
        verbose_name = _('Tooth Chart')
        verbose_name_plural = _('Tooth Charts')

    def __str__(self):
        return f"Tooth Chart for {self.patient.full_name}"


class ToothModel(BaseModel):
    Status = ToothStatusEnum
    Position = ToothPositionEnum

    chart = models.ForeignKey(
        ToothChartModel,
        on_delete=models.CASCADE,
        related_name='teeth',
        verbose_name=_('Tooth Chart')
    )
    number = models.IntegerField(_('Tooth Number'))
    status = models.CharField(
        _('Status'),
        max_length=30,
        choices=Status.choices,
        default=Status.HEALTHY
    )
    position = models.CharField(
        _('Quadrant'),
        max_length=2,
        choices=Position.choices,
        help_text=_('Tooth quadrant for UI layout')
    )
    color_code = models.CharField(
        _('Color Code'),
        max_length=12,
        blank=True,
        help_text=_('Used for UI coloring')
    )

    class Meta:
        verbose_name = _('Tooth')
        verbose_name_plural = _('Teeth')
        unique_together = ('chart', 'number')

    def __str__(self):
        return f"Tooth {self.number} ({self.get_status_display()})"


class OcclusionLinkModel(BaseModel):
    Relation = ToothRelationEnum

    chart = models.ForeignKey(
        ToothChartModel,
        on_delete=models.CASCADE,
        related_name='occlusion_links',
        verbose_name=_('Tooth Chart')
    )
    source_tooth = models.ForeignKey(
        ToothModel,
        on_delete=models.CASCADE,
        related_name='links_from',
        verbose_name=_('Source Tooth')
    )
    target_tooth = models.ForeignKey(
        ToothModel,
        on_delete=models.CASCADE,
        related_name='links_to',
        verbose_name=_('Target Tooth')
    )
    relation = models.CharField(
        _('Relation Type'),
        max_length=20,
        choices=Relation.choices,
        default=Relation.ADJACENT
    )

    class Meta:
        verbose_name = _('Occlusion Link')
        verbose_name_plural = _('Occlusion Links')
        unique_together = ('source_tooth', 'target_tooth', 'relation')

    def __str__(self):
        return f"{self.source_tooth.number} → {self.target_tooth.number} ({self.get_relation_display()})"

