from django.contrib.auth.tokens import default_token_generator
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
import json

from vendor.forms import VendorForm
from accounts.forms import UserForm, UserProfileForm
from accounts.models import User
from accounts.others_models.model_profile import UserProfile

from helpers.decorators import vendor_level_required, customer_level_required, admin_level_required
from helpers.utils import detectUser, send_verification_email
from helpers import commons

from vendor.model.vendor_models import Vendor
from vendor.model.product_value_model import VendorProductValue



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

            mail_subject = 'Por favor, ative sua conta'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Sua conta foi cadastrada com sucesso, verifique seu email para ativa-la.')
            return redirect('home')
        else:
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                    "showMessage": f'Tivemos o seguinte erro ao registrar novo usuário: {form.errors}'
                    })
                }
            ) 
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('home')

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
            if password != confirm_password:
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                        "showMessage": "Sua senha está incorreta, verifique e tente novamente"
                        })
                    }
                ) 

            user = User.objects.create_user(name=name, email=email, username=username, password=password)
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

def logout(request):
    auth.logout(request)
    messages.error(request, 'Você está desconectado.')
    return redirect('login')

@login_required(login_url='login')
@vendor_level_required
def vendorDashboard(request):
    template_name = 'vendor/vendorDashboard.html'
    vendor = Vendor.objects.get(user=request.user)
    products = VendorProductValue.objects.filter(vendor=vendor.id, product__is_available=True)#.order_by('created_at')
    recent_products = products[:10]
    context = {
        'vendor':vendor,
        'products': products,
        'recent_products': recent_products
    }
    return render(request, template_name, context)

@login_required(login_url='login')
@customer_level_required
def user_profile(request):
    template_name = 'accounts/user-profile.html'
    user = User.objects.get(user=request.user.id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        form_profile =  UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
    else:
        form = UserForm(instance=user)
        form_profile =  UserProfileForm(instance=user)
    context = {
        'user': user,
        'form_profile': form_profile,
        'form': form
    }
    return render(request, template_name, context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Redefina sua senha'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'O link de redefinição de senha foi enviado para o seu endereço de e-mail.')
            return redirect('login')
        else:
            messages.error(request, 'Conta não existe')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Redefina sua senha')
        return redirect('reset_password')
    else:
        messages.error(request, 'Este link expirou!')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Redefinição de senha bem-sucedida')
            return redirect('login')
        else:
            messages.error(request, 'Senha não confere!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')