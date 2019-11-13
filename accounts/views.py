import uuid

from django.core.mail import send_mail
from django.shortcuts import render

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)

    url = request.build_absolute_uri(f"/accounts/login?uid={uid}")
    send_mail(
        'Your login link for To-Do Lists',
        f'Use this link to log in:\n\n{url}',
        'noreply@todolists',
        [email],
    )
    return render(request, 'login_email_sent.html')
