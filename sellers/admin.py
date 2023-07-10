from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.db.models import F

from .models import Seller, Transaction, Phone


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'credit')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('seller', 'transaction_type', 'amount', 'date')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not change:
            seller = Seller.objects.select_for_update().get(pk=obj.seller_id)
            if obj.transaction_type == 'increase':
                seller.credit = F('credit') + obj.amount
            elif obj.transaction_type == 'decrease':
                new_credit = seller.credit - obj.amount
                if new_credit < 0:
                    messages.error(request, "There is not enough crdit")
                    return
                seller.credit = new_credit
            seller.save()
        super().save_model(request, obj, form, change)


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'charge', 'seller')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not change:
            seller = obj.seller
            new_credit = seller.credit - obj.charge
            if new_credit < 0:
                messages.error(request, "There is not enough crdit")
                return
            seller.credit = new_credit
            seller.save()
            obj.seller = seller
        super().save_model(request, obj, form, change)
