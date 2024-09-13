
from django.shortcuts import render, redirect
from django.http import HttpResponse
from doctor.models import Doctor , Fulltimes
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

#@login_required  # Ensure the user is logged in
def payment_view(request):
    if request.method == 'GET':
        slot = request.GET.get('slot')
        doctor_id = request.GET.get('doctor_id')
        try:
            existing_reservation = Fulltimes.objects.get(id_U=request.user.appuser, id_D_id=doctor_id)
            return render(request, 'already_reserved.html', {'reservation': existing_reservation})
        except ObjectDoesNotExist:
            return render(request, 'payment.html', {'slot': slot, 'doctor_id': doctor_id})

    if request.method == 'POST':
        slot = request.POST.get('slot')
        doctor_id = request.POST.get('doctor_id')
        Fulltimes.objects.create(
            id_U=request.user.appuser,
            id_D_id=doctor_id,
            accessdate=slot,
            paid=False
        )
        return redirect('success_page')