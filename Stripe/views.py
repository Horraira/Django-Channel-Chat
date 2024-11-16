import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

import stripe
from ChatPrj import settings

from .models import Customer, Payment, PaymentHistory, PaymentIntent
from .serializer import PaymentHistorySerializer, PaymentIntentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount', 500)
        currency = request.data.get('currency', 'usd')
        # Check if the user has a Stripe customer ID
        customer, created = Customer.objects.get_or_create(user=user)
        if not customer.stripe_customer_id:
            # Create a new customer in Stripe
            stripe_customer = stripe.Customer.create(email=user.email)
            customer.stripe_customer_id = stripe_customer['id']
            customer.save()

        # Create a payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Convert to cents
            currency=currency,
            customer=customer.stripe_customer_id,
            automatic_payment_methods={'enabled': True},
        )

        # Save the payment intent in the database
        payment = PaymentIntent.objects.create(
            user=user,
            stripe_payment_intent_id=payment_intent['id'],
            amount=amount,
            currency=currency,
            status=payment_intent['status']
        )

        serializer = PaymentIntentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfirmPaymentView(generics.GenericAPIView):
    def post(self, request):
        amount = request.data.get('payment_id')
        amount = int(float(amount) * 100)  # Convert to cents
        intent = stripe.PaymentIntent.create(
            amount= amount,
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )

        return Response({'clientSecret': intent['client_secret'],
                        'dpmCheckerLink': f"https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={intent['id']}"}, 
                        status=status.HTTP_200_OK)


class PreviousPaymentDetailsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer

    def get(self, request):
        # Get the previous payment of the user
        payment_history = PaymentHistory.objects.filter(user=request.user).last()
        if payment_history:
            serializer = self.serializer_class(payment_history)
            return Response(serializer.data)
        return Response({"detail": "No previous payments found."}, status=status.HTTP_404_NOT_FOUND)

def create_payment(request, amount):

    payment = Payment.objects.create(
        amount=amount,
        stripe_payment_intent_id= "pi_1JQ5ZvKXr6c3oJ9Z6Z6Z6Z6Z",
    )
    # Generate QR code with payment link
    payment_url = f"{request.build_absolute_uri('/stripe/payment/')}{payment.id}"
    qr = qrcode.make(payment_url)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response

@csrf_exempt
def confirm_payment(request, payment_id):
    return render(request, 'payment/checkout.html', {'payment_id': payment_id})

def payment_page(request):
    return render(request, 'payment/complete.html')


# mahep54368@rinseart.com
# t8_4%XN2q7LV_qA