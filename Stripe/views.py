import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_intent_id):
        # Confirm the payment intent
        intent = stripe.PaymentIntent.confirm(payment_intent_id)

        # Update the status in the database
        payment_intent = PaymentIntent.objects.get(stripe_payment_intent_id=payment_intent_id)
        payment_intent.status = intent['status']
        payment_intent.save()

        if intent['status'] == 'succeeded':
            # Save payment history
            PaymentHistory.objects.create(
                user=request.user,
                amount=payment_intent.amount,
                stripe_payment_intent_id=payment_intent.stripe_payment_intent_id
            )

        return Response({'status': intent['status']}, status=status.HTTP_200_OK)


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
    # Create a Stripe PaymentIntent
    payment_intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),  # amount in cents
        currency='usd',
        automatic_payment_methods={
            'enabled': True,
            'allow_redirects': 'never',
            },
    )
    payment = Payment.objects.create(
        amount=amount,
        stripe_payment_intent_id=payment_intent['id']
    )

    # Generate QR code with payment link
    payment_url = f"{request.build_absolute_uri('/payments/confirm/')}{payment.id}"
    qr = qrcode.make(payment_url)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response


@csrf_exempt
def confirm_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payment/confirm_payment.html', {'payment': payment})

@csrf_exempt
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    try:
        # Confirm the payment with the required parameters for automatic payment methods
        stripe.PaymentIntent.confirm(
            payment.stripe_payment_intent_id
        )
        payment.status = 'Completed'
    except stripe.error.CardError:
        payment.status = 'Failed'
    except stripe.error.InvalidRequestError as e:
        # Handle specific Stripe errors
        print(f"Stripe Error: {e}")
        payment.status = 'Failed'
    payment.save()
    return redirect('Stripe:confirm_payment', payment_id=payment_id)



