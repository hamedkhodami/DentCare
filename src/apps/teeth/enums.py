from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class ToothStatusEnum(TextChoices):

    HEALTHY = 'healthy', _('Healthy'),
    PLANNED = 'planned', _('Planned'),
    IN_PROGRESS = 'in_progress', _('In Progress'),
    DONE = 'done', _('Done'),
    REMOVED = 'removed', _('Removed'),


class ToothRelationEnum(TextChoices):

    ADJACENT = 'adjacent', _('Adjacent'),
    ANTAGONIST = 'antagonist', _('Antagonist'),


class ToothPositionEnum(TextChoices):
    UPPER_RIGHT = 'UR', _('Upper Right')
    UPPER_LEFT = 'UL', _('Upper Left')
    LOWER_RIGHT = 'LR', _('Lower Right')
    LOWER_LEFT = 'LL', _('Lower Left')
