from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def landing_page(request):
    return render(request, 'index.html')