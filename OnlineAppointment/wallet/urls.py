from django.urls import path
from django.shortcuts import render
from .views import payment_view, cancel_reservation
urlpatterns = [
    path('payment/', payment_view, name='payment'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('reservation_canceled/', lambda request: render(request, 'reservation_canceled.html'), name='reservation_canceled'),
]