from django.urls import path
from .views import CreatePaymentIntentView, ConfirmPaymentView, PreviousPaymentDetailsView
from . import views

app_name = 'Stripe'

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('confirm-payment/<str:payment_intent_id>/', ConfirmPaymentView.as_view(), name='confirm-payment'),
    path('previous-payment/', PreviousPaymentDetailsView.as_view(), name='previous-payment'),

    path('create/<int:amount>/', views.create_payment, name='create_payment'),
    path('confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
    path('process/<int:payment_id>/', views.process_payment, name='process_payment'),
]
