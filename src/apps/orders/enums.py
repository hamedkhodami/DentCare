from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OrderStatusEnum(TextChoices):
    DRAFT = 'draft', _('Draft')
    SUBMITTED = 'submitted', _('Submitted')
    PAID = 'paid', _('Paid')
    CANCELLED = 'cancelled', _('Cancelled')


class PaymentStatusEnum(TextChoices):
    PENDING = 'pending', _('Pending')
    SUCCESS = 'success', _('Success')
    FAILED = 'failed', _('Failed')
    REFUNDED = 'refunded', _('Refunded')


class PaymentMethodEnum(TextChoices):
    PAYPAL = 'paypal', _('PayPal')
