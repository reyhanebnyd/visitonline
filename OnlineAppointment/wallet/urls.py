from django.urls import path
from django.shortcuts import render
from .views import payment_view, cancel_reservation, WalletDetailView, add_balance, reservations_page
urlpatterns = [
    path('wallet/', WalletDetailView.as_view(), name='wallet_detail'),
    path('wallet/add/', add_balance, name='add_balance'),
    path('payment/<int:doctor_id>/<str:slot>/', payment_view, name='payment'),
    path('reservations/', reservations_page, name='reservations'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('reservation_canceled/', lambda request: render(request, 'reservation_canceled.html'), name='reservation_canceled'),
]