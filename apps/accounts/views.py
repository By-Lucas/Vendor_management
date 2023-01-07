from datetime import datetime
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import message
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from vendor.forms import VendorForm
from accounts.forms import UserForm
from accounts.models import User
from accounts.others_models.model_profile import UserProfile

from django.contrib import messages, auth
from helpers.utils import detectUser, send_verification_email

from helpers import commons

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied
from vendor.model.vendor_models import Vendor
from django.template.defaultfilters import slugify
#from orders.models import Order
import datetime


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('home')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            # Create the user using the form
            user = form.save(commit=False)
            user.role = commons.USER_COMMOM
            user.save()

            # Create the user using create_user method
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']
            # user = User.objects.create_user(name=name, email=email, username=username, password=password, confirm_password=confirm_password)
            # user.role = commons.USER_COMMOM
            # user.save()

            # Send verification email
            mail_subject = 'Por favor, ative sua conta'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Sua conta foi cadastrada com sucesso, verifique seu email para ativa-la.')
            return redirect('registerUser')
        else:
            print('formulário inválido')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('home') #myAccount
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user = User.objects.create_user(name=name, email=email, username=username, password=password, confirm_password=confirm_password)
            user.role = commons.VENDOR
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            mail_subject = 'Por favor, ative sua conta'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Sua conta foi cadastrada com sucesso! Por favor, aguarde a aprovação.')
            return redirect('registerVendor')
        else:
            print('formulário inválido')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    # Ative o usuário definindo o status is_active como True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active == False:
            user.is_active = True
            user.save()
            messages.success(request, 'Parabéns! Sua conta foi ativada.')
        else:
            messages.success(request, 'Sua já está ativada.')

        return redirect('myAccount')
    else:
        messages.error(request, 'Link de ativação inválido')
        return redirect('myAccount')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('home')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Agora você está logado.')
            return redirect('home')
        else:
            messages.error(request, 'Credenciais inválida')
            return redirect('login')

    return render(request, 'accounts/login.html')