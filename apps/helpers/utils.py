from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages

from helpers import commons
from django.conf import settings

from helpers.commons import *


def detectUser(request):
    print(request.user.role)
    if request.user.role == commons.VENDOR:
        redirectUrl = 'user_profile'
        return redirectUrl
    elif request.user.is_superuser:
        redirectUrl = '/admin'
        return redirectUrl
    elif request.user.role == commons.ADMIN_SISTEM:
        redirectUrl = 'user_profile'
        return redirectUrl
    elif request.user.role == commons.USER_COMMOM:
        redirectUrl = 'user_profile'
        return redirectUrl
    #else:
    #    redirectUrl = 'home'
    #    messages.error(request, 'Você não tem um nivel de permissão para acessar')
    #   return redirectUrl

    
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()
