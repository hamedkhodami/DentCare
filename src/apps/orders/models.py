from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.account.models import User
from apps.treatment.models import CaseItemModel

from .enums import OrderStatusEnum, PaymentStatusEnum


class CartModel(BaseModel):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name=_('Doctor')
    )
    is_submitted = models.BooleanField(_('Submitted'), default=False)
    submitted_at = models.DateTimeField(_('Submitted At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"Cart by Dr. {self.doctor.full_name}"


class CartItemModel(BaseModel):
    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Cart')
    )
    case_item = models.ForeignKey(
        CaseItemModel,
        on_delete=models.CASCADE,
        related_name='cart_links',
        verbose_name=_('Case Item')
    )
    price = models.DecimalField(
        _('Price'),
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ('cart', 'case_item')

    def __str__(self):
        return f"{self.case_item.service.name} → {self.price}"


class OrderModel(BaseModel):
    Status = OrderStatusEnum

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Doctor')
    )
    cart = models.OneToOneField(
        'CartModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order',
        verbose_name=_('Cart')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    total_price = models.DecimalField(
        _('Total Price'),
        max_digits=12,
        decimal_places=2,
        default=0
    )
    submitted_at = models.DateTimeField(_('Submitted At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"Order #{self.id} by Dr. {self.doctor.full_name}"


class OrderItemModel(BaseModel):
    order = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order')
    )
    case_item = models.ForeignKey(
        CaseItemModel,
        on_delete=models.PROTECT,
        related_name='order_links',
        verbose_name=_('Case Item')
    )
    price = models.DecimalField(
        _('Price'),
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        unique_together = ('order', 'case_item')

    def __str__(self):
        return f"{self.case_item.service.name} → {self.price}"


class PaymentModel(BaseModel):
    Status = PaymentStatusEnum

    order = models.OneToOneField(
        OrderModel,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name=_('Order')
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Doctor')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    paypal_transaction_id = models.CharField(
        _('PayPal Transaction ID'),
        max_length=100,
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        _('Amount'),
        max_digits=12,
        decimal_places=2
    )
    paid_at = models.DateTimeField(_('Paid At'), null=True, blank=True)
    note = models.TextField(_('Note'), blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return f"Payment for Order #{self.order.id} → {self.amount} ({self.get_status_display()})"