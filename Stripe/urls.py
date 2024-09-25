from django.urls import path
from .views import CreatePaymentIntentView, ConfirmPaymentView, PreviousPaymentDetailsView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('confirm-payment/<str:payment_intent_id>/', ConfirmPaymentView.as_view(), name='confirm-payment'),
    path('previous-payment/', PreviousPaymentDetailsView.as_view(), name='previous-payment'),
]
