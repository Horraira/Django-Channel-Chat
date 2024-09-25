from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PaymentIntent, Customer, PaymentHistory
from rest_framework.views import APIView
from .serializer import PaymentIntentSerializer, PaymentHistorySerializer, CardInformationSerializer
import stripe


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
