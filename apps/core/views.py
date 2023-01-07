from django.shortcuts import redirect, render
from helpers.decorators import customer_level_required


def home(request):
    return render(request, 'core/home.html')

