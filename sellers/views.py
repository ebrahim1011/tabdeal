from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F


from .models import Seller, Transaction, Phone


class IncreaseCreditView(APIView):
    @transaction.atomic
    def post(self, request, seller_id):
        try:
            amount = int(request.data.get('amount'))
            seller = Seller.objects.select_for_update().get(id=seller_id)
            seller.credit = F('credit') + amount
            seller.save()
            Transaction.objects.create(seller=seller, transaction_type='increase', amount=amount)
            return Response({'message': 'Credit increased successfully.'})
        except (Seller.DoesNotExist, ValueError):
            return Response({'error': 'Invalid seller ID or amount.'}, status=status.HTTP_400_BAD_REQUEST)


class DecreaseCreditView(APIView):
    @transaction.atomic
    def post(self, request, seller_id):
        try:
            amount = int(request.data.get('amount'))
            seller = Seller.objects.select_for_update().get(id=seller_id)
            if seller.credit >= amount:
                seller.credit = F('credit') - amount
                seller.save()
                Transaction.objects.create(seller=seller, transaction_type='decrease', amount=amount)
                return Response({'message': 'Credit decreased successfully.'})
            else:
                return Response({'error': 'Insufficient credit.'}, status=status.HTTP_400_BAD_REQUEST)
        except (Seller.DoesNotExist, ValueError):
            return Response({'error': 'Invalid seller ID or amount.'}, status=status.HTTP_400_BAD_REQUEST)


class SellChargeView(APIView):
    @transaction.atomic
    def post(self, request, seller_id):
        try:
            phone_number = request.data.get('phone_number')
            amount = int(request.data.get('amount'))
            seller = Seller.objects.select_for_update().get(id=seller_id)
            phone = Phone.objects.select_for_update().get(number=phone_number, seller=seller)

            if phone.charge >= amount:
                phone.charge = F('charge') - amount
                phone.save()
                Transaction.objects.create(seller=seller, transaction_type='decrease', amount=amount)
                return Response({'message': 'Charge sold successfully.'})
            else:
                return Response({'error': 'Insufficient charge on the phone number.'}, status=status.HTTP_400_BAD_REQUEST)
        except (Seller.DoesNotExist, Phone.DoesNotExist, ValueError):
            return Response({'error': 'Invalid seller ID, phone number, or amount.'}, status=status.HTTP_400_BAD_REQUEST)
