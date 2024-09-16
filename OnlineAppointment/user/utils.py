import pyotp
from datetime import datetime, timedelta
from django.shortcuts import redirect

def send_otp(request):
    if request.method == 'POST':
        totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
        otp = totp.now()
        request.session['otp_secret_key'] = totp.secret
        valid_date = datetime.now() + timedelta(minutes=1)
        request.session['otp_valid_date'] = str(valid_date)

    print(f'your one time password is {otp}')
    return redirect ('otp_view')
