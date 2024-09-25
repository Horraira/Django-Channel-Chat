from rest_framework import serializers
from .models import PaymentIntent, PaymentHistory

class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = ['id', 'user', 'amount', 'currency', 'status', 'stripe_payment_intent_id']


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'user', 'amount', 'stripe_payment_intent_id', 'payment_date']

