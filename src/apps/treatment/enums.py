from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CaseStatusEnum(TextChoices):
    DRAFT = 'draft', _('Draft')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
    COMPLETED = 'completed', _('Completed')


class MirrorCopyTypeEnum(TextChoices):
    ADJACENT = 'adjacent', _('Adjacent Tooth')
    ANTAGONIST = 'antagonist', _('Antagonist Tooth')


class CaseItemStatusEnum(TextChoices):
    PLANNED = 'planned', _('Planned')
    IN_PROGRESS = 'in_progress', _('In Progress')
    DONE = 'done', _('Done')
    CANCELLED = 'cancelled', _('Cancelled')


class CaseAttachmentEnum(TextChoices):
    IMAGE = "image", _('Image')
    STL = "stl", _('STL')
    PDF = "pdf", _('PDF')
    OTHER = "other", _('Other')